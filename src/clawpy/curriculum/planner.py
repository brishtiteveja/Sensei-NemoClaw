"""Lesson plan generator — creates personalized Duolingo-style learning paths.

Given a student's target exam, difficulty preference, and optional weak areas,
generates an ordered sequence of lessons across subjects.
"""

from __future__ import annotations

import uuid
from typing import Any

from .models import (
    Difficulty,
    LessonPlan,
    SubjectId,
    TargetExam,
)
from .syllabus import ALL_SUBJECTS, EXAM_SUBJECTS


def generate_lesson_plan(
    student_id: str,
    target_exam: TargetExam = TargetExam.GENERAL,
    difficulty: Difficulty = Difficulty.MEDIUM,
    subjects: list[SubjectId] | None = None,
    weak_topics: list[str] | None = None,
    max_lessons: int | None = None,
) -> LessonPlan:
    """Generate a personalized lesson plan.

    Strategy:
    - Interleave subjects (like Duolingo mixes skills)
    - Start with easier lessons, ramp up
    - Prioritize weak topics if provided
    - Filter by target exam's relevant subjects
    """
    # Determine which subjects to include
    exam_subjects = EXAM_SUBJECTS.get(target_exam, list(ALL_SUBJECTS.keys()))
    if subjects:
        active_subjects = [s for s in subjects if s in exam_subjects]
    else:
        active_subjects = exam_subjects

    # Collect all lessons per subject, filtered by difficulty
    subject_lessons: dict[SubjectId, list[dict[str, str]]] = {}
    total_minutes = 0

    for subj_id in active_subjects:
        curriculum = ALL_SUBJECTS.get(subj_id)
        if not curriculum:
            continue

        lessons = []
        for unit in curriculum.units:
            for lesson in unit.lessons:
                # Include lessons at or below the target difficulty
                lesson_diff = _difficulty_rank(lesson.difficulty)
                target_diff = _difficulty_rank(difficulty)

                if lesson_diff <= target_diff:
                    entry = {
                        "subject": subj_id.value,
                        "unit_id": unit.id,
                        "unit_title": unit.title,
                        "unit_title_bn": unit.title_bn,
                        "lesson_id": lesson.id,
                        "lesson_title": lesson.title,
                        "lesson_title_bn": lesson.title_bn,
                        "difficulty": lesson.difficulty.value,
                        "minutes": str(lesson.estimated_minutes),
                        "xp": str(lesson.xp_reward),
                        "concepts": ", ".join(lesson.concepts),
                    }
                    # Boost priority for weak topics
                    priority = lesson.order
                    if weak_topics:
                        for wt in weak_topics:
                            if (wt.lower() in lesson.title.lower()
                                    or wt.lower() in ", ".join(lesson.concepts).lower()
                                    or wt.lower() in unit.title.lower()):
                                priority -= 100  # Move to front
                                entry["_weak_boost"] = "true"
                                break
                    entry["_priority"] = str(priority)
                    lessons.append(entry)
                    total_minutes += lesson.estimated_minutes

        # Sort by priority within subject
        lessons.sort(key=lambda x: int(x["_priority"]))
        subject_lessons[subj_id] = lessons

    # Interleave subjects (round-robin)
    path: list[dict[str, str]] = []
    iterators = {s: iter(ls) for s, ls in subject_lessons.items() if ls}
    active = list(iterators.keys())

    while active:
        for subj in list(active):
            try:
                entry = next(iterators[subj])
                # Clean internal keys
                clean = {k: v for k, v in entry.items() if not k.startswith("_")}
                path.append(clean)
            except StopIteration:
                active.remove(subj)

    if max_lessons:
        path = path[:max_lessons]

    # Title
    exam_name = target_exam.value.upper()
    diff_label = difficulty.value.capitalize()
    title = f"{exam_name} Preparation — {diff_label}"
    title_bn = f"{exam_name} প্রস্তুতি — {_difficulty_bn(difficulty)}"

    return LessonPlan(
        id=str(uuid.uuid4())[:8],
        student_id=student_id,
        title=title,
        title_bn=title_bn,
        target_exam=target_exam,
        difficulty=difficulty,
        subjects=active_subjects,
        path=path,
        total_lessons=len(path),
        estimated_hours=total_minutes // 60,
    )


def get_subject_overview(subject_id: SubjectId) -> dict[str, Any]:
    """Get a summary of a subject's curriculum."""
    curriculum = ALL_SUBJECTS.get(subject_id)
    if not curriculum:
        return {"error": f"Subject {subject_id} not found"}

    units = []
    total_lessons = 0
    for unit in curriculum.units:
        lessons = [
            {
                "id": l.id,
                "title": l.title,
                "title_bn": l.title_bn,
                "difficulty": l.difficulty.value,
                "minutes": l.estimated_minutes,
                "concepts": l.concepts,
            }
            for l in unit.lessons
        ]
        total_lessons += len(lessons)
        units.append({
            "id": unit.id,
            "title": unit.title,
            "title_bn": unit.title_bn,
            "icon": unit.icon,
            "nctb_chapter": unit.nctb_chapter,
            "nctb_class": unit.nctb_class,
            "lesson_count": len(lessons),
            "lessons": lessons,
        })

    return {
        "subject": subject_id.value,
        "title": curriculum.title,
        "title_bn": curriculum.title_bn,
        "icon": curriculum.icon,
        "target_exams": [e.value for e in curriculum.target_exams],
        "total_units": len(units),
        "total_lessons": total_lessons,
        "units": units,
    }


def get_lesson_detail(lesson_id: str) -> dict[str, Any] | None:
    """Get full details of a specific lesson."""
    for curriculum in ALL_SUBJECTS.values():
        for unit in curriculum.units:
            for lesson in unit.lessons:
                if lesson.id == lesson_id:
                    return {
                        "id": lesson.id,
                        "title": lesson.title,
                        "title_bn": lesson.title_bn,
                        "description": lesson.description,
                        "description_bn": lesson.description_bn,
                        "difficulty": lesson.difficulty.value,
                        "xp_reward": lesson.xp_reward,
                        "estimated_minutes": lesson.estimated_minutes,
                        "concepts": lesson.concepts,
                        "prerequisites": lesson.prerequisites,
                        "subject": curriculum.subject.value,
                        "unit_id": unit.id,
                        "unit_title": unit.title,
                        "unit_title_bn": unit.title_bn,
                    }
    return None


def _difficulty_rank(d: Difficulty) -> int:
    return {"easy": 1, "medium": 2, "hard": 3}[d.value]


def _difficulty_bn(d: Difficulty) -> str:
    return {"easy": "সহজ", "medium": "মাঝারি", "hard": "কঠিন"}[d.value]
