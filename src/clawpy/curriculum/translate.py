"""Translation layer with persistent cache.

Translates questions/text using the LLM, caches results in a JSON file
so we never re-translate the same content.
"""

from __future__ import annotations

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
    if target_lang == source_lang:
        return question

    q = dict(question)
    q_text = q.get("question", "")
    options = q.get("options", [])

    full_text = q_text
    for opt in options:
        full_text += f"\n{opt['id']}) {opt['text']}"

    translated = await translate_text(full_text, target_lang, source_lang)

    parts = translated.split("\n")
    q["question_translated"] = parts[0] if parts else translated
    q["target_lang"] = target_lang

    for i, opt in enumerate(options):
        opt_line = parts[i + 1] if i + 1 < len(parts) else f"{opt['id']}) {opt['text']}"
        clean = opt_line.lstrip()
        if len(clean) > 2 and clean[1] == ')':
            clean = clean[2:].strip()
        elif len(clean) > 2 and clean[0] in 'ABCD' and clean[1] == ')':
            clean = clean[2:].strip()
        opt["text_translated"] = clean or opt["text"]

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
