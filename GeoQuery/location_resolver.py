from sqlalchemy import text
from database import engine


def resolve_location(location):
    tables = [
        ("states", "state"),
        ("districts", "district"),
        ("subdistricts", "subdistrict")
    ]

    with engine.connect() as conn:
        for table, level in tables:
            sql = text(f"""
            SELECT 1
            FROM {table}
            WHERE LOWER(name)=LOWER(:loc)
            LIMIT 1
            """)

            result = conn.execute(
                sql,
                {"loc": location}
            ).fetchone()
            if result:
                return level
    return None