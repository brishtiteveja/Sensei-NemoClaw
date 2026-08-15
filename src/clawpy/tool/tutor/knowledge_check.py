"""KnowledgeCheck tool — pull a random question from Postgres for mid-conversation quizzes."""

from __future__ import annotations

import json
import os
from typing import Any

from clawpy.tool.base import Permission, RunContext, ToolResult

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://shikkha:shikkha_secret@localhost:5432/shikkhadikkha",
)


class KnowledgeCheckTool:
    """Pull a random question from the database to quiz the student mid-conversation."""

    _conn: Any = None

    @property
    def name(self) -> str:
        return "KnowledgeCheck"

    @property
    def description(self) -> str:
        return (
            "Get a random practice question from the database to check if the student "
            "understands a concept. Use after explaining something to verify comprehension."
        )

    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "Topic to find a question for (Bangla or English)",
                },
                "subject": {
                    "type": "string",
                    "description": "Subject tag (e.g. 'গতিবিদ্যা', 'জৈব রসায়ন')",
                },
            },
            "required": ["topic"],
        }

    def permission_for(self, input: dict[str, Any]) -> Permission:
        return Permission.READ_ONLY

    def is_read_only(self, input: dict[str, Any]) -> bool:
        return True

    def _get_conn(self) -> Any:
        if self._conn is None or getattr(self._conn, 'closed', True):
            import psycopg2
            self._conn = psycopg2.connect(DATABASE_URL)
            self._conn.autocommit = True
        return self._conn

    async def run(self, input: dict[str, Any], ctx: RunContext) -> ToolResult:
        topic = input.get("topic", "").strip()
        subject = input.get("subject", "").strip()

        try:
            conn = self._get_conn()
        except Exception as e:
            return ToolResult(
                content=f"Database unavailable. Generate a question about '{topic}' yourself."
            )

        cur = conn.cursor()
        conditions: list[str] = []
        params: list[Any] = []

        # Try full-text search on topic
        if topic:
            conditions.append(
                "(to_tsvector('simple', question_text) @@ plainto_tsquery('simple', %s) "
                "OR subject ILIKE %s)"
            )
            params.extend([topic, f"%{topic}%"])

        if subject:
            conditions.append("subject ILIKE %s")
            params.append(f"%{subject}%")

        where = ""
        if conditions:
            where = "WHERE " + " AND ".join(conditions)

        try:
            cur.execute(f"""
                SELECT id, question_text, options, correct_answer, correct_index, subject, university, exam_year
                FROM admission_question
                {where}
                ORDER BY RANDOM()
                LIMIT 1
            """, params)
            row = cur.fetchone()
        except Exception as e:
            return ToolResult(
                content=f"Query failed. Generate a question about '{topic}' yourself."
            )
        finally:
            cur.close()

        if not row:
            return ToolResult(
                content=f"No questions found for '{topic}'. Generate one yourself."
            )

        options = []
        for i, opt in enumerate(row[2]):
            options.append({
                "id": chr(65 + i),
                "text": opt,
                "isCorrect": i == row[4],
            })

        output = {
            "question": row[1],
            "options": [{"id": o["id"], "text": o["text"]} for o in options],
            "subject": row[5],
            "source": f"{row[6]} ({row[7]})",
            "_correct_answer": row[3],
            "_correct_index": row[4],
        }
        return ToolResult(content=json.dumps(output, ensure_ascii=False, indent=2))
