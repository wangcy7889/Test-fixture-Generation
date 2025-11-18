import os
import asyncpg
from typing import Dict, Any

async def upsert_user_score(user_id: int,
                            score: int,
                            table: str = "user_scores") -> Dict[str, Any]:

    dsn = os.getenv("PG_DSN")
    if not dsn:
        raise EnvironmentError("Error: PG_DSN is not set")

    conn = await asyncpg.connect(dsn)


    await conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} (
            user_id INT PRIMARY KEY,
            high_score INT NOT NULL
        )
    """)


    row = await conn.fetchrow(f"""
        INSERT INTO {table} (user_id, high_score)
        VALUES ($1, $2)
        ON CONFLICT (user_id)
        DO UPDATE SET high_score = GREATEST({table}.high_score, EXCLUDED.high_score)
        RETURNING user_id, high_score
    """, user_id, score)

    await conn.close()
    return dict(row)
