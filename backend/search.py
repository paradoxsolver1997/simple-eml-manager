# backend/search.py

from backend.database import connect


ALLOWED_FIELDS = {"subject", "sender", "recipients", "body", "all"}


def build_match_expression(query: str, field: str) -> str:
    """
    structure FTS5 MATCH expression
    """
    query = query.strip()

    if not query:
        return ""

    safe = query.replace('"', '""')

    if field == "all":
        # let FTS itself matches in all columns
        return f'"{safe}"'

    # Field level search（FTS5 native syntax）
    return f'{field}:"{safe}"'


def search_emails(query: str, field: str = "all", limit: int = 100):
    if field not in ALLOWED_FIELDS:
        raise ValueError(f"Invalid search field: {field}")

    match_expr = build_match_expression(query, field)

    if not match_expr:
        return []

    conn = connect()

    sql = """
        SELECT
            e.*,
            bm25(emails_fts) AS rank
        FROM emails_fts
        JOIN emails e ON e.id = emails_fts.rowid
        WHERE emails_fts MATCH ?
        ORDER BY rank
        LIMIT ?
    """

    rows = conn.execute(sql, (match_expr, limit)).fetchall()
    conn.close()
    print([dict(row) for row in rows])
    return [dict(row) for row in rows]
