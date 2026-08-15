"""QuestionLookup tool — search 17K+ admission questions in PostgreSQL."""

from __future__ import annotations

import json
import os
from typing import Any

from clawpy.tool.base import Permission, RunContext, ToolResult

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://shikkha:shikkha_secret@localhost:5432/shikkhadikkha",
)

# University slug → search patterns
_UNIVERSITY_MAP: dict[str, list[str]] = {
    "du": ["dhaka-university"],
    "buet": ["buet"],
    "medical": ["medical"],
    "ru": ["rajshahi-university"],
    "cu": ["chittagong-university"],
    "ju": ["jahangirnagar-university", "jagannath-university"],
    "kuet": ["kuet"],
    "ruet": ["ruet"],
    "cuet": ["cuet"],
}


class QuestionLookupTool:
    """Search 17,000+ real Bangladesh admission test questions in PostgreSQL."""

    _conn: Any = None

    @property
    def name(self) -> str:
        return "QuestionLookup"

    @property
    def description(self) -> str:
        return (
            "Search 17,000+ real Bangladesh university admission test questions. "
            "Filter by subject (Bangla tag like গতিবিদ্যা, জৈব রসায়ন, etc.), "
            "university (du/buet/ru/cu/ju/medical), year (2017-2026), "
            "or free-text search in Bangla/English. Returns MCQs with options and correct answer."
        )

    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "subject": {
                    "type": "string",
                    "description": "Subject tag in Bangla (e.g. 'গতিবিদ্যা', 'জৈব রসায়ন', 'English') or English keyword",
                },
                "search": {
                    "type": "string",
                    "description": "Free-text search in question text (Bangla or English)",
                },
                "university": {
                    "type": "string",
                    "description": "University: du, buet, ru, cu, ju, medical, kuet, ruet, cuet",
                },
                "year": {
                    "type": "string",
                    "description": "Exam year (e.g. '2023')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max questions to return (default 5, max 20)",
                },
            },
            "required": [],
        }

    def permission_for(self, input: dict[str, Any]) -> Permission:
        return Permission.READ_ONLY

    def is_read_only(self, input: dict[str, Any]) -> bool:
        return True

    def _get_conn(self) -> Any:
        if self._conn is None or self._conn.closed:
            import psycopg2
            self._conn = psycopg2.connect(DATABASE_URL)
            self._conn.autocommit = True
        return self._conn

    async def run(self, input: dict[str, Any], ctx: RunContext) -> ToolResult:
        try:
            conn = self._get_conn()
        except Exception as e:
            return ToolResult(content=f"Database connection failed: {e}", is_error=True)

        cur = conn.cursor()

        conditions: list[str] = []
        params: list[Any] = []

        # Subject filter — map English names to Bangla DB tags
        _SUBJECT_MAP = {
            "physics": ["পদার্থ", "গতি", "বল", "তাপ", "আলো", "তরঙ্গ", "বিদ্যুৎ", "চুম্বক"],
            "chemistry": ["রসায়ন", "জৈব", "অজৈব", "পরমাণু", "মোল"],
            "math": ["গণিত", "বীজগণিত", "জ্যামিতি", "ক্যালকুলাস", "সমীকরণ"],
            "biology": ["জীব", "উদ্ভিদ", "প্রাণী", "কোষ", "জেনেটিক"],
            "english": ["English", "Grammar", "Vocabulary", "Sentence"],
            "bangla": ["বাংলা", "ব্যাকরণ", "সাহিত্য", "কবিতা"],
        }
        subject = input.get("subject", "").strip()
        if subject:
            mapped = _SUBJECT_MAP.get(subject.lower())
            if mapped:
                or_clauses = " OR ".join(["subject ILIKE %s"] * len(mapped))
                conditions.append(f"({or_clauses})")
                params.extend(f"%{m}%" for m in mapped)
            else:
                conditions.append("subject ILIKE %s")
                params.append(f"%{subject}%")

        # University filter
        university = input.get("university", "").strip().lower()
        if university:
            slugs = _UNIVERSITY_MAP.get(university, [university])
            placeholders = ",".join(["%s"] * len(slugs))
            conditions.append(f"university IN ({placeholders})")
            params.extend(slugs)

        # Year filter
        year = input.get("year", "").strip()
        if year:
            conditions.append("exam_year = %s")
            params.append(year)

        # Free-text search
        search = input.get("search", "").strip()
        if search:
            conditions.append("to_tsvector('simple', question_text) @@ plainto_tsquery('simple', %s)")
            params.append(search)

        limit = min(input.get("limit", 5), 20)

        where = ""
        if conditions:
            where = "WHERE " + " AND ".join(conditions)

        query = f"""
            SELECT id, university, exam_name, exam_year, question_text,
                   options, correct_answer, correct_index, subject
            FROM admission_question
            {where}
            ORDER BY RANDOM()
            LIMIT %s
        """
        params.append(limit)

        try:
            cur.execute(query, params)
            rows = cur.fetchall()
        except Exception as e:
            return ToolResult(content=f"Query failed: {e}", is_error=True)
        finally:
            cur.close()

        if not rows:
            return ToolResult(content="No questions found matching the criteria.")

        questions = []
        for row in rows:
            options = []
            for i, opt in enumerate(row[5]):
                options.append({
                    "id": chr(65 + i),
                    "text": opt,
                    "isCorrect": i == row[7],
                })
            questions.append({
                "id": row[0],
                "university": row[1],
                "exam": row[2][:80],
                "year": row[3],
                "question": row[4],
                "options": options,
                "correct_answer": row[6],
                "subject": row[8],
            })

        output = json.dumps(questions, ensure_ascii=False, indent=2)
        return ToolResult(content=f"Found {len(questions)} question(s):\n{output}")
