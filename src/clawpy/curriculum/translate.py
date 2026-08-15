"""Translation layer with persistent cache.

Translates questions/text using the LLM, caches results in a JSON file
so we never re-translate the same content.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import logging

logger = logging.getLogger(__name__)

CACHE_DIR = os.environ.get("DIKKHA_TRANSLATION_CACHE", "/tmp/dikkha_translations")
os.makedirs(CACHE_DIR, exist_ok=True)


def _cache_path(lang: str) -> str:
    return os.path.join(CACHE_DIR, f"translations_{lang}.json")


def _load_cache(lang: str) -> dict[str, str]:
    path = _cache_path(lang)
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_cache(lang: str, cache: dict[str, str]) -> None:
    path = _cache_path(lang)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=0)


def _text_key(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def get_cached(text: str, lang: str) -> str | None:
    cache = _load_cache(lang)
    return cache.get(_text_key(text))


def set_cached(text: str, lang: str, translation: str) -> None:
    cache = _load_cache(lang)
    cache[_text_key(text)] = translation
    _save_cache(lang, cache)


async def translate_text(text: str, target_lang: str, source_lang: str = "bn") -> str:
    if target_lang == source_lang:
        return text

    cached = get_cached(text, target_lang)
    if cached:
        return cached

    from .regions import LANGUAGES
    lang_info = LANGUAGES.get(target_lang, {})
    lang_name = lang_info.get("name", target_lang)

    prompt = (
        f"Translate the following text to {lang_name}. "
        f"Keep mathematical notation, formulas, and option labels (A, B, C, D) unchanged. "
        f"Return ONLY the translation, nothing else.\n\n{text}"
    )

    try:
        from clawpy.server import _get_server_config, _create_provider
        from clawpy.provider.base import Request as ProviderRequest
        from clawpy.types import Role, text_message

        cfg = _get_server_config()
        provider = _create_provider(cfg)
        messages = [text_message(Role.USER, prompt)]
        req = ProviderRequest(
            model=cfg.model, system="You are a translator. Translate accurately.", messages=messages,
            tools=[], max_tokens=4096, temperature=0.1,
        )
        response = await provider.send(req)
        from clawpy.types import ContentType
        result = ""
        for block in response.content:
            if block.type == ContentType.TEXT:
                result += block.text
        result = result.strip()
        if result:
            set_cached(text, target_lang, result)
            return result
    except Exception as e:
        logger.warning(f"Translation failed: {e}")

    return text


async def translate_question(question: dict, target_lang: str, source_lang: str = "bn") -> dict:
    """Translate an MCQ's stem and every option into `target_lang`.

    The stem and each option are translated as separate units, concurrently.

    The previous approach concatenated stem + options into one blob and split the
    reply on newlines. That silently failed whenever the model did not return exactly
    one line per item -- a wrapped stem, a dropped blank line or an added preamble
    shifted every index, and the options fell back to the source language while the
    stem appeared translated. A student then saw an English question with Bangla
    answers, which is worse than no translation at all because it looks deliberate.

    Per-unit translation also caches far better: option texts like "উত্তল"/"অবতল"
    recur across hundreds of physics questions, so after a short warm-up most options
    are cache hits and cost nothing.
    """
    if target_lang == source_lang:
        return question

    q = dict(question)
    q_text = q.get("question", "")
    # Copy each option dict; otherwise we mutate the caller's objects in place.
    options = [dict(o) for o in q.get("options", [])]
    q["options"] = options

    results = await asyncio.gather(
        translate_text(q_text, target_lang, source_lang),
        *(translate_text(o.get("text", ""), target_lang, source_lang) for o in options),
        return_exceptions=True,
    )

    def _ok(value, fallback: str) -> str:
        # translate_text already returns the source text on failure; this guards the
        # gather-level exception case so one bad option cannot fail the whole question.
        if isinstance(value, BaseException) or not value:
            return fallback
        return value

    q["question_translated"] = _ok(results[0], q_text)
    q["target_lang"] = target_lang

    for opt, res in zip(options, results[1:]):
        opt["text_translated"] = _ok(res, opt.get("text", ""))

    return q


def get_cache_stats() -> dict:
    stats = {}
    if os.path.exists(CACHE_DIR):
        for f in os.listdir(CACHE_DIR):
            if f.startswith("translations_") and f.endswith(".json"):
                lang = f.replace("translations_", "").replace(".json", "")
                path = os.path.join(CACHE_DIR, f)
                try:
                    with open(path) as fh:
                        data = json.load(fh)
                    stats[lang] = len(data)
                except Exception:
                    stats[lang] = 0
    return stats
