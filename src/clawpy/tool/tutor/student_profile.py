"""StudentProfile tool — read and update student learning analytics."""

from __future__ import annotations

import json
import os
from typing import Any

from clawpy.tool.base import Permission, RunContext, ToolResult

_PROFILES_DIR = os.environ.get("DIKKHA_PROFILES_DIR", "/tmp/dikkha_profiles")


class StudentProfileTool:
    """Read and update a student's learning profile — strengths, weaknesses, streaks."""

    @property
    def name(self) -> str:
        return "StudentProfile"

    @property
    def description(self) -> str:
        return (
            "Read or update a student's learning profile. "
            "Shows weak subjects, accuracy by topic, streak, XP, and study patterns. "
            "Use this to personalize tutoring."
        )

    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["read", "update"],
                    "description": "Read the profile or update it with new data",
                },
                "user_id": {
                    "type": "string",
                    "description": "Student's user ID",
                },
                "update_data": {
                    "type": "object",
                    "description": "Data to merge into profile (for 'update' action)",
                    "properties": {
                        "subject": {"type": "string"},
                        "topic": {"type": "string"},
                        "correct": {"type": "boolean"},
                        "time_taken": {"type": "number"},
                    },
                },
            },
            "required": ["action", "user_id"],
        }

    def permission_for(self, input: dict[str, Any]) -> Permission:
        if input.get("action") == "update":
            return Permission.WORKSPACE_WRITE
        return Permission.READ_ONLY

    def is_read_only(self, input: dict[str, Any]) -> bool:
        return input.get("action") != "update"

    def _profile_path(self, user_id: str) -> str:
        os.makedirs(_PROFILES_DIR, exist_ok=True)
        return os.path.join(_PROFILES_DIR, f"{user_id}.json")

    def _load_profile(self, user_id: str) -> dict[str, Any]:
        path = self._profile_path(user_id)
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "user_id": user_id,
                "total_questions": 0,
                "correct_answers": 0,
                "streak": 0,
                "xp": 0,
                "level": 1,
                "subject_stats": {},
                "weak_topics": [],
                "strong_topics": [],
            }

    def _save_profile(self, user_id: str, profile: dict[str, Any]) -> None:
        path = self._profile_path(user_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)

    async def run(self, input: dict[str, Any], ctx: RunContext) -> ToolResult:
        user_id = input["user_id"]
        action = input["action"]

        profile = self._load_profile(user_id)

        if action == "read":
            return ToolResult(content=json.dumps(profile, ensure_ascii=False, indent=2))

        # Update
        data = input.get("update_data", {})
        subject = data.get("subject", "")
        topic = data.get("topic", "")
        correct = data.get("correct", False)

        profile["total_questions"] = profile.get("total_questions", 0) + 1
        if correct:
            profile["correct_answers"] = profile.get("correct_answers", 0) + 1
            profile["streak"] = profile.get("streak", 0) + 1
            profile["xp"] = profile.get("xp", 0) + 10
        else:
            profile["streak"] = 0
            profile["xp"] = profile.get("xp", 0) + 2  # XP for trying

        # Subject stats
        if subject:
            stats = profile.setdefault("subject_stats", {})
            s = stats.setdefault(subject, {"total": 0, "correct": 0, "topics": {}})
            s["total"] += 1
            if correct:
                s["correct"] += 1
            if topic:
                t = s["topics"].setdefault(topic, {"total": 0, "correct": 0})
                t["total"] += 1
                if correct:
                    t["correct"] += 1

        # Recalculate weak/strong topics
        weak = []
        strong = []
        for subj, s in profile.get("subject_stats", {}).items():
            if s["total"] >= 3:
                acc = s["correct"] / s["total"]
                if acc < 0.5:
                    weak.append(subj)
                elif acc >= 0.8:
                    strong.append(subj)
        profile["weak_topics"] = weak
        profile["strong_topics"] = strong

        # Level up every 100 XP
        profile["level"] = 1 + profile.get("xp", 0) // 100

        self._save_profile(user_id, profile)
        return ToolResult(content=f"Profile updated. XP: {profile['xp']}, Streak: {profile['streak']}, Level: {profile['level']}")
