import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

# ── DB config
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME", "gamecafe"),
}

QUERIES_FILE = "../db_proof/queries.sql"
OUTPUT_FILE  = "../db_proof/query_outputs.txt"
LINE         = "─" * 60


def parse_queries(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    raw = content.split(";")
    queries = []
    for q in raw:
        lines = [l for l in q.splitlines() if l.strip() and not l.strip().startswith("--")]
        cleaned = "\n".join(lines).strip()
        if cleaned:
            queries.append(cleaned)
    return queries


def format_table(headers, rows):
    if not rows:
        return "  (no rows returned)"

    widths = [
        max(len(str(h)), max((len(str(r[i])) for r in rows), default=0))
        for i, h in enumerate(headers)
    ]
    fmt = "  " + "  ".join(f"{{:<{w}}}" for w in widths)
    sep = "  " + "  ".join("-" * w for w in widths)

    lines = [fmt.format(*headers), sep]
    for row in rows:
        clean = [val if val is not None else "NULL" for val in row]
        lines.append(fmt.format(*clean))
    return "\n".join(lines)


def run_queries():
    queries = parse_queries(QUERIES_FILE)

    if not queries:
        print("No queries found in queries.sql — add some and try again.")
        return

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur  = conn.cursor()
    except Error as e:
        print(f"Could not connect to MySQL: {e}")
        return

    output_lines = ["QUERY OUTPUTS", "=" * 60, ""]

    for i, query in enumerate(queries, start=1):
        output_lines.append(f"{LINE}")
        output_lines.append(f"  Query {i}")
        output_lines.append(f"{LINE}")
        output_lines.append(f"  SQL: {query[:120]}{'...' if len(query) > 120 else ''}")
        output_lines.append("")

        try:
            cur.execute(query)
            all_rows = cur.fetchall()
            headers  = [desc[0] for desc in cur.description] if cur.description else []
            total    = len(all_rows)
            preview  = all_rows[:5]

            output_lines.append(f"  Total rows returned: {total}")
            output_lines.append("")

            if total == 0:
                output_lines.append("  0 rows returned.")
            else:
                output_lines.append(f"  First {min(5, total)} row(s):")
                output_lines.append(format_table(headers, preview))

        except Error as e:
            output_lines.append(f"  ERROR: {e}")

        output_lines.append("")

    cur.close()
    conn.close()

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(output_lines))

    print(f"Done! Results written to {OUTPUT_FILE}")


if __name__ == "__main__":
    run_queries()