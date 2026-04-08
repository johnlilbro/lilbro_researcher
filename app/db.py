import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "app.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS generations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                source_file TEXT NOT NULL,
                kind TEXT NOT NULL,
                mode TEXT NOT NULL,
                saved_file TEXT NOT NULL,
                usage_json TEXT NOT NULL
            )
            """
        )
        conn.commit()


def add_generation(item: dict) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO generations (timestamp, source_file, kind, mode, saved_file, usage_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                item["timestamp"],
                item["source_file"],
                item["kind"],
                item["mode"],
                item["saved_file"],
                json.dumps(item["usage"]),
            ),
        )
        conn.commit()


def recent_generations(limit: int = 50) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT timestamp, source_file, kind, mode, saved_file, usage_json
            FROM generations
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    items = []
    for row in rows:
        items.append(
            {
                "timestamp": row["timestamp"],
                "source_file": row["source_file"],
                "kind": row["kind"],
                "mode": row["mode"],
                "saved_file": row["saved_file"],
                "usage": json.loads(row["usage_json"]),
            }
        )
    return items
