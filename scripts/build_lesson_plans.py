"""Build lesson plans for Engineering and Medical paths from the SattAcademy question bank.

Reads satt_academy_admission_questions.jsonl, maps questions to curriculum lessons,
and generates easy-difficulty lesson plan JSONs ready for the app.

Usage:
    uv run python scripts/build_lesson_plans.py
"""

from __future__ import annotations

import json
import os
import re
import sys

# Add project to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

DATA_PATH = os.environ.get(
    "SATT_QUESTIONS_PATH",
    "/home/projects/BanglaDataManager/data-crawling/data/satt_academy_admission/satt_academy_admission_questions.jsonl",
)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "plans")

# ── Subject/topic mapping from Bangla tags to curriculum lesson IDs ──────────

SUBJECT_MAP: dict[str, list[tuple[str, str]]] = {
    # Physics topics → (curriculum_lesson_id, curriculum_unit_id)
    "ভেক্টর": [("phy-mech-02", "phy-mechanics")],
    "গতিবিদ্যা": [("phy-mech-03", "phy-mechanics")],
    "সমতলে বস্তুকণার গতি": [("phy-mech-04", "phy-mechanics")],
    "বল": [("phy-mech-05", "phy-mechanics")],
    "কাজ, শক্তি ও ক্ষমতা": [("phy-mech-06", "phy-mechanics")],
    "মহাকর্ষ ও অভিকর্ষ": [("phy-mech-07", "phy-mechanics")],
    "তরঙ্গ ও শক্তি": [("phy-wave-01", "phy-waves")],
    "তরঙ্গ ও শব্দ": [("phy-wave-03", "phy-waves")],
    "জ্যামিতিক  আলোকবিজ্ঞান": [("phy-wave-04", "phy-waves")],
    "স্থির তড়িৎ": [("phy-elec-01", "phy-electricity")],
    "চল তড়িৎ": [("phy-elec-03", "phy-electricity")],
    "তড়িৎ প্রবাহের চৌম্বক ক্রিয়া ও চুম্বকত্ব": [("phy-elec-04", "phy-electricity")],
    "সেমিকন্ডাক্টর ও ইলেক্ট্রনিক্স": [("phy-mod-04", "phy-modern")],
    "তাপগতিবিদ্যা": [("chem-phy-02", "chem-physical")],
    "পদার্থবিদ্যা": [("phy-mech-01", "phy-mechanics")],

    # Chemistry topics
    "গুণগত রসায়ন (দ্বিতীয় অধ্যায়)": [("chem-str-01", "chem-structure")],
    "পরিবেশ রসায়ন (প্রথম অধ্যায়)": [("chem-str-02", "chem-structure")],
    "জৈব রসায়ন": [("chem-org-01", "chem-organic")],
    "তড়িৎ রসায়ন": [("chem-phy-05", "chem-physical")],
    "জারণ-বিজারণ": [("chem-phy-05", "chem-physical")],

    # Higher Math topics
    "উচ্চতর গণিত": [("hm-calc-01", "hmath-calculus")],
    "যোগজীকরণ": [("hm-calc-04", "hmath-calculus")],
    "ম্যাট্রিক্স ও নির্ণায়ক": [("hm-alg-02", "hmath-algebra")],
    "বিপরীত ত্রিকোণমিতিক ফাংশন ও ত্রিকোণমিতিক সমীকরণ": [("hm-trig-02", "hmath-trig")],
    "কনিক": [("hm-coord-03", "hmath-coord")],
    "ফাংশন ও ফাংশনের লেখচিত্র": [("hm-alg-04", "hmath-algebra")],
    "সমতলে বস্তুকণার গতি (Motion of particles in a plane)": [("phy-mech-04", "phy-mechanics")],

    # Biology topics
    "জীববিজ্ঞান": [("bio-cell-01", "bio-cell")],
}

# Broader keyword matching for subjects not in the exact map
KEYWORD_LESSON_MAP: list[tuple[str, str, str]] = [
    # (keyword_in_subject, lesson_id, unit_id)
    ("তড়িৎ", "phy-elec-03", "phy-electricity"),
    ("চুম্বক", "phy-elec-04", "phy-electricity"),
    ("আলোক", "phy-wave-04", "phy-waves"),
    ("তরঙ্গ", "phy-wave-02", "phy-waves"),
    ("গতি", "phy-mech-03", "phy-mechanics"),
    ("বল", "phy-mech-05", "phy-mechanics"),
    ("তাপ", "chem-phy-02", "chem-physical"),
    ("রসায়ন", "chem-str-01", "chem-structure"),
    ("জৈব", "chem-org-01", "chem-organic"),
    ("গণিত", "hm-calc-01", "hmath-calculus"),
    ("ত্রিকোণ", "hm-trig-01", "hmath-trig"),
    ("ম্যাট্রিক্স", "hm-alg-02", "hmath-algebra"),
    ("জীব", "bio-cell-01", "bio-cell"),
    ("উদ্ভিদ", "bio-bot-01", "bio-botany"),
    ("প্রাণি", "bio-zoo-01", "bio-zoology"),
    ("কোষ", "bio-cell-01", "bio-cell"),
    ("DNA", "bio-gen-01", "bio-genetics"),
    ("জেনেটিক", "bio-gen-03", "bio-genetics"),
]

# University classification
ENGINEERING_UNIVERSITIES = {"buet", "kuet", "ruet", "cuet", "buet-admission"}
MEDICAL_KEYWORDS_IN_EXAM = ["medical", "মেডিকেল"]


def classify_question(q: dict) -> tuple[str | None, str | None]:
    """Map a question to (lesson_id, unit_id) based on its subject tag."""
    subject = q.get("subject", "")

    # Exact match first
    if subject in SUBJECT_MAP:
        return SUBJECT_MAP[subject][0]

    # Keyword fallback
    for keyword, lesson_id, unit_id in KEYWORD_LESSON_MAP:
        if keyword in subject:
            return lesson_id, unit_id

    return None, None


def is_engineering_relevant(q: dict) -> bool:
    """Check if a question is relevant for engineering admission."""
    u = q.get("university", "").lower()
    subject = q.get("subject", "")
    if any(eu in u for eu in ENGINEERING_UNIVERSITIES):
        return True
    # Physics, Chemistry, Higher Math subjects
    eng_keywords = ["পদার্থ", "তড়িৎ", "বল", "গতি", "তাপ", "তরঙ্গ", "আলোক", "চুম্বক",
                    "সেমিকন্ডাক্টর", "মহাকর্ষ", "রসায়ন", "জৈব রসায়ন", "পরিবেশ রসায়ন",
                    "গুণগত", "জারণ", "গণিত", "ক্যালকুলাস", "যোগজীকরণ", "ম্যাট্রিক্স",
                    "ত্রিকোণমিতি", "কনিক", "ভেক্টর", "ফাংশন"]
    return any(kw in subject for kw in eng_keywords)


def is_medical_relevant(q: dict) -> bool:
    """Check if a question is relevant for medical admission."""
    exam = q.get("exam_name", "").lower()
    subject = q.get("subject", "")
    if any(mk in exam for mk in MEDICAL_KEYWORDS_IN_EXAM):
        return True
    med_keywords = ["জীববিজ্ঞান", "উদ্ভিদ", "প্রাণি", "কোষ", "জেনেটিক", "DNA",
                    "শ্বসন", "সালোকসংশ্লেষণ", "রসায়ন", "জৈব রসায়ন", "পরিবেশ রসায়ন",
                    "গুণগত", "পদার্থ", "তড়িৎ", "বল", "গতি"]
    return any(kw in subject for kw in med_keywords)


def build_exercise(q: dict) -> dict:
    """Convert a raw SattAcademy question to a lesson exercise."""
    options = []
    for i, opt in enumerate(q.get("options", [])):
        options.append({
            "id": chr(65 + i),  # A, B, C, D
            "text": opt.strip() if opt else "",
            "text_bn": opt.strip() if opt else "",
            "isCorrect": i == q.get("correct_option_index", -1),
        })

    return {
        "id": q.get("question_id", ""),
        "type": "mcq",
        "question": q.get("question_text", "").strip(),
        "question_bn": q.get("question_text", "").strip(),
        "options": options,
        "correct_answer": chr(65 + q.get("correct_option_index", 0)),
        "correct_answer_text": q.get("correct_answer", ""),
        "source": q.get("exam_name", ""),
        "university": q.get("university", ""),
        "year": q.get("exam_year", ""),
        "subject_tag": q.get("subject", ""),
        "has_image": q.get("question_image") is not None,
    }


def build_plan(
    plan_name: str,
    plan_name_bn: str,
    target_exam: str,
    questions: list[dict],
    max_per_lesson: int = 15,
) -> dict:
    """Build a complete lesson plan with exercises grouped by curriculum lesson."""
    # Group questions by lesson
    lesson_exercises: dict[str, list[dict]] = {}
    lesson_units: dict[str, str] = {}
    unmapped = 0

    for q in questions:
        lesson_id, unit_id = classify_question(q)
        if not lesson_id:
            unmapped += 1
            continue
        lesson_exercises.setdefault(lesson_id, []).append(build_exercise(q))
        lesson_units[lesson_id] = unit_id

    # Build lesson plan structure
    from clawpy.curriculum.syllabus import ALL_SUBJECTS
    from clawpy.curriculum.models import SubjectId

    lessons = []
    total_exercises = 0

    for curriculum in ALL_SUBJECTS.values():
        for unit in curriculum.units:
            for lesson in unit.lessons:
                exercises = lesson_exercises.get(lesson.id, [])
                if not exercises:
                    continue

                # For easy plan, take simpler questions (shorter text = usually easier)
                exercises.sort(key=lambda e: len(e.get("question", "")))
                selected = exercises[:max_per_lesson]
                total_exercises += len(selected)

                lessons.append({
                    "lesson_id": lesson.id,
                    "lesson_title": lesson.title,
                    "lesson_title_bn": lesson.title_bn,
                    "unit_id": unit.id,
                    "unit_title": unit.title,
                    "unit_title_bn": unit.title_bn,
                    "subject": curriculum.subject.value,
                    "subject_title_bn": curriculum.title_bn,
                    "difficulty": "easy",
                    "exercise_count": len(selected),
                    "xp_reward": 20,
                    "estimated_minutes": max(5, len(selected) * 1),  # 1 min per question
                    "concepts": lesson.concepts,
                    "exercises": selected,
                })

    # Sort: interleave subjects
    subject_groups: dict[str, list[dict]] = {}
    for l in lessons:
        subject_groups.setdefault(l["subject"], []).append(l)

    interleaved = []
    iters = {s: iter(ls) for s, ls in subject_groups.items()}
    active = list(iters.keys())
    while active:
        for s in list(active):
            try:
                interleaved.append(next(iters[s]))
            except StopIteration:
                active.remove(s)

    return {
        "plan_name": plan_name,
        "plan_name_bn": plan_name_bn,
        "target_exam": target_exam,
        "difficulty": "easy",
        "total_lessons": len(interleaved),
        "total_exercises": total_exercises,
        "unmapped_questions": unmapped,
        "total_source_questions": len(questions),
        "lessons": interleaved,
    }


def main():
    print(f"Loading questions from {DATA_PATH}...")
    all_questions = []
    with open(DATA_PATH, encoding="utf-8") as f:
        for line in f:
            all_questions.append(json.loads(line))
    print(f"Loaded {len(all_questions):,} questions")

    # Filter for engineering and medical
    eng_questions = [q for q in all_questions if is_engineering_relevant(q)]
    med_questions = [q for q in all_questions if is_medical_relevant(q)]
    print(f"Engineering-relevant: {len(eng_questions):,}")
    print(f"Medical-relevant: {len(med_questions):,}")

    # Build plans
    eng_plan = build_plan(
        "Engineering Easy Plan",
        "ইঞ্জিনিয়ারিং সহজ প্ল্যান",
        "buet",
        eng_questions,
        max_per_lesson=15,
    )

    med_plan = build_plan(
        "Medical Easy Plan",
        "মেডিকেল সহজ প্ল্যান",
        "medical",
        med_questions,
        max_per_lesson=15,
    )

    # Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    eng_path = os.path.join(OUTPUT_DIR, "engineering_easy.json")
    with open(eng_path, "w", encoding="utf-8") as f:
        json.dump(eng_plan, f, ensure_ascii=False, indent=2)
    print(f"\nEngineering plan: {eng_plan['total_lessons']} lessons, {eng_plan['total_exercises']} exercises")
    print(f"  Saved to {eng_path}")
    print(f"  Unmapped: {eng_plan['unmapped_questions']} questions")

    med_path = os.path.join(OUTPUT_DIR, "medical_easy.json")
    with open(med_path, "w", encoding="utf-8") as f:
        json.dump(med_plan, f, ensure_ascii=False, indent=2)
    print(f"\nMedical plan: {med_plan['total_lessons']} lessons, {med_plan['total_exercises']} exercises")
    print(f"  Saved to {med_path}")
    print(f"  Unmapped: {med_plan['unmapped_questions']} questions")

    # Print lesson summary
    for plan_name, plan in [("Engineering", eng_plan), ("Medical", med_plan)]:
        print(f"\n{'='*60}")
        print(f"{plan_name} Plan — {plan['total_lessons']} lessons")
        print(f"{'='*60}")
        for i, lesson in enumerate(plan["lessons"]):
            print(f"  {i+1:2}. [{lesson['subject']:12}] {lesson['lesson_title_bn']:<30} "
                  f"({lesson['exercise_count']} questions)")


if __name__ == "__main__":
    main()
