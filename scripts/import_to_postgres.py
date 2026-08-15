"""Import SattAcademy admission questions into PostgreSQL.

Usage:
    DATABASE_URL="postgresql://shikkha:shikkha_secret@localhost:5432/shikkhadikkha" \
        uv run python scripts/import_to_postgres.py
"""

from __future__ import annotations

import json
import os
import sys

DATA_PATH = os.environ.get(
    "SATT_QUESTIONS_PATH",
    "/home/projects/BanglaDataManager/data-crawling/data/satt_academy_admission/satt_academy_admission_questions.jsonl",
)
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://shikkha:shikkha_secret@localhost:5432/shikkhadikkha",
)
BATCH_SIZE = 500


def main():
    try:
        import psycopg2
    except ImportError:
        print("Installing psycopg2-binary...")
        os.system(f"{sys.executable} -m pip install psycopg2-binary -q")
        import psycopg2

    print(f"Loading questions from {DATA_PATH}...")
    questions = []
    with open(DATA_PATH, encoding="utf-8") as f:
        for line in f:
            questions.append(json.loads(line))
    print(f"Loaded {len(questions):,} questions")

    print(f"Connecting to {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}...")
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Check existing count
    cur.execute("SELECT COUNT(*) FROM admission_question")
    existing = cur.fetchone()[0]
    if existing > 0:
        print(f"Table already has {existing:,} rows. Truncating...")
        cur.execute("TRUNCATE admission_question")
        conn.commit()

    print(f"Importing {len(questions):,} questions in batches of {BATCH_SIZE}...")

    inserted = 0
    skipped = 0
    for i in range(0, len(questions), BATCH_SIZE):
        batch = questions[i:i + BATCH_SIZE]
        values = []
        for q in batch:
            qid = q.get("question_id", "")
            if not qid or not q.get("question_text", "").strip():
                skipped += 1
                continue

            options = q.get("options", [])
            # Clean options
            clean_options = [str(o).strip() for o in options if o]

            values.append((
                qid,
                q.get("university", ""),
                q.get("exam_name", ""),
                q.get("exam_year", ""),
                q.get("question_text", "").strip(),
                clean_options,
                q.get("correct_answer", ""),
                q.get("correct_option_index", 0),
                q.get("subject", ""),
                q.get("tags", []),
                q.get("question_type", "mcq"),
                q.get("question_image") is not None,
                q.get("question_image"),
            ))

        if values:
            args_str = ",".join(
                cur.mogrify(
                    "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", v
                ).decode("utf-8")
                for v in values
            )
            cur.execute(
                f"INSERT INTO admission_question "
                f"(id, university, exam_name, exam_year, question_text, options, "
                f"correct_answer, correct_index, subject, tags, question_type, "
                f"has_image, image_url) VALUES {args_str} "
                f"ON CONFLICT (id) DO NOTHING"
            )
            inserted += len(values)
            conn.commit()

        if (i // BATCH_SIZE) % 10 == 0:
            print(f"  {inserted:,} inserted, {skipped:,} skipped...")

    conn.commit()

    # Verify
    cur.execute("SELECT COUNT(*) FROM admission_question")
    total = cur.fetchone()[0]

    # Stats
    cur.execute("SELECT university, COUNT(*) FROM admission_question GROUP BY university ORDER BY COUNT(*) DESC LIMIT 10")
    uni_stats = cur.fetchall()

    cur.execute("SELECT subject, COUNT(*) FROM admission_question GROUP BY subject ORDER BY COUNT(*) DESC LIMIT 15")
    subj_stats = cur.fetchall()

    cur.execute("SELECT exam_year, COUNT(*) FROM admission_question GROUP BY exam_year ORDER BY exam_year DESC LIMIT 10")
    year_stats = cur.fetchall()

    cur.close()
    conn.close()

    print(f"\nDone! {total:,} questions in database ({skipped:,} skipped)")
    print(f"\nTop universities:")
    for uni, count in uni_stats:
        print(f"  {count:5,}  {uni}")
    print(f"\nTop subjects:")
    for subj, count in subj_stats:
        print(f"  {count:5,}  {subj}")
    print(f"\nBy year:")
    for year, count in year_stats:
        print(f"  {count:5,}  {year}")


if __name__ == "__main__":
    main()
