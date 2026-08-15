"""Data models for the curriculum system.

Hierarchy:
  Subject → Unit → Lesson → Exercise

Each maps to the NCTB HSC syllabus structure:
  Subject = Physics/Chemistry/Math/Biology
  Unit    = Chapter (e.g., "Mechanics", "Organic Chemistry")
  Lesson  = Topic within chapter (e.g., "Newton's First Law")
  Exercise = A single question/activity
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ExerciseType(str, Enum):
    MCQ = "mcq"
    TRUE_FALSE = "true_false"
    FILL_BLANK = "fill_blank"
    MATCHING = "matching"
    CONCEPTUAL = "conceptual"  # Open-ended, AI-graded
    WORKED_PROBLEM = "worked_problem"  # Step-by-step solve


class LessonStatus(str, Enum):
    LOCKED = "locked"
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MASTERED = "mastered"  # Completed with 90%+ accuracy


class SubjectId(str, Enum):
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    GENERAL_MATH = "general_math"
    HIGHER_MATH = "higher_math"
    BIOLOGY = "biology"


class TargetExam(str, Enum):
    DU = "du"
    BUET = "buet"
    MEDICAL = "medical"
    RU = "ru"
    JU = "ju"
    CU = "cu"
    GST = "gst"
    CUET = "cuet"
    KUET = "kuet"
    RUET = "ruet"
    IUT = "iut"
    SUST = "sust"
    GENERAL = "general"


class AdmissionTrack(str, Enum):
    UNIVERSITY = "university"
    ENGINEERING = "engineering"
    MEDICAL = "medical"


TRACK_SUBJECTS: dict[AdmissionTrack, list[SubjectId]] = {
    AdmissionTrack.UNIVERSITY: [SubjectId.PHYSICS, SubjectId.CHEMISTRY, SubjectId.HIGHER_MATH, SubjectId.BIOLOGY, SubjectId.GENERAL_MATH],
    AdmissionTrack.ENGINEERING: [SubjectId.PHYSICS, SubjectId.CHEMISTRY, SubjectId.HIGHER_MATH],
    AdmissionTrack.MEDICAL: [SubjectId.BIOLOGY, SubjectId.CHEMISTRY, SubjectId.PHYSICS, SubjectId.GENERAL_MATH],
}

TRACK_EXAMS: dict[AdmissionTrack, list[TargetExam]] = {
    AdmissionTrack.UNIVERSITY: [TargetExam.DU, TargetExam.RU, TargetExam.CU, TargetExam.JU, TargetExam.GST],
    AdmissionTrack.ENGINEERING: [TargetExam.BUET, TargetExam.CUET, TargetExam.KUET, TargetExam.RUET, TargetExam.IUT, TargetExam.SUST],
    AdmissionTrack.MEDICAL: [TargetExam.MEDICAL],
}

TRACK_SUBJECT_WEIGHTS: dict[AdmissionTrack, dict[SubjectId, float]] = {
    AdmissionTrack.UNIVERSITY: {SubjectId.PHYSICS: 0.20, SubjectId.CHEMISTRY: 0.20, SubjectId.HIGHER_MATH: 0.20, SubjectId.BIOLOGY: 0.20, SubjectId.GENERAL_MATH: 0.20},
    AdmissionTrack.ENGINEERING: {SubjectId.PHYSICS: 0.35, SubjectId.HIGHER_MATH: 0.35, SubjectId.CHEMISTRY: 0.30},
    AdmissionTrack.MEDICAL: {SubjectId.BIOLOGY: 0.40, SubjectId.CHEMISTRY: 0.30, SubjectId.PHYSICS: 0.20, SubjectId.GENERAL_MATH: 0.10},
}

TRACK_META: dict[AdmissionTrack, dict[str, str]] = {
    AdmissionTrack.UNIVERSITY: {
        "title": "University Science",
        "title_bn": "বিশ্ববিদ্যালয়",
        "description": "DU, RU, CU, JU, GST ভর্তি পরীক্ষা",
        "icon": "🏛️",
    },
    AdmissionTrack.ENGINEERING: {
        "title": "Engineering",
        "title_bn": "ইঞ্জিনিয়ারিং",
        "description": "BUET, KUET, RUET, CUET, IUT",
        "icon": "⚙️",
    },
    AdmissionTrack.MEDICAL: {
        "title": "Medical",
        "title_bn": "মেডিকেল",
        "description": "MBBS ভর্তি পরীক্ষা",
        "icon": "🏥",
    },
}


@dataclass
class Exercise:
    id: str
    type: ExerciseType
    difficulty: Difficulty
    question: str
    question_bn: str
    options: list[dict[str, Any]] = field(default_factory=list)
    correct_answer: str = ""
    explanation: str = ""
    explanation_bn: str = ""
    points: int = 10
    time_limit: int = 60  # seconds
    source: str = ""  # e.g., "BUET 2023", "UDVASH Model Test 5"
    tags: list[str] = field(default_factory=list)


@dataclass
class Lesson:
    id: str
    title: str
    title_bn: str
    description: str
    description_bn: str
    difficulty: Difficulty
    exercises: list[Exercise] = field(default_factory=list)
    exercise_count: int = 0  # Total exercises (may be loaded lazily)
    xp_reward: int = 20
    estimated_minutes: int = 10
    prerequisites: list[str] = field(default_factory=list)  # Lesson IDs
    concepts: list[str] = field(default_factory=list)  # Key concepts taught
    order: int = 0


@dataclass
class Unit:
    id: str
    title: str
    title_bn: str
    description: str
    description_bn: str
    icon: str  # Emoji or icon name
    lessons: list[Lesson] = field(default_factory=list)
    order: int = 0
    # Maps to NCTB chapter
    nctb_chapter: str = ""
    nctb_class: str = ""  # "XI" or "XII"


@dataclass
class SubjectCurriculum:
    subject: SubjectId
    title: str
    title_bn: str
    icon: str
    units: list[Unit] = field(default_factory=list)
    target_exams: list[TargetExam] = field(default_factory=list)


@dataclass
class LessonPlan:
    """A personalized learning path for a student."""
    id: str
    student_id: str
    title: str
    title_bn: str
    target_exam: TargetExam
    difficulty: Difficulty
    subjects: list[SubjectId]
    # Ordered list of (subject, unit, lesson) to study
    path: list[dict[str, str]] = field(default_factory=list)
    total_lessons: int = 0
    completed_lessons: int = 0
    estimated_hours: int = 0


@dataclass
class StudentProgress:
    """Track a student's progress through the curriculum."""
    student_id: str
    completed_lessons: dict[str, LessonResult] = field(default_factory=dict)
    current_streak: int = 0
    total_xp: int = 0
    level: int = 1
    hearts: int = 5  # Duolingo-style lives
    last_active: str = ""


@dataclass
class LessonResult:
    lesson_id: str
    score: float  # 0.0 - 1.0
    correct: int = 0
    incorrect: int = 0
    skipped: int = 0
    time_taken: int = 0  # seconds
    xp_earned: int = 0
    completed_at: str = ""
    mistakes: list[str] = field(default_factory=list)  # Exercise IDs answered wrong
