from config import *


# ---------- CLI: init db ----------
@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql") as f:
            db.executescript(f.read().decode("utf-8"))
        print("Initialized the database.")


# ---------- CLI: truncate db ----------
@app.cli.command("truncate-db")
def truncate_db():
    """Delete all rows from all tables (keeps schema)."""
    db = get_db()

    # Get all table names except SQLite's internal tables
    tables = db.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
    """).fetchall()

    for t in tables:
        table_name = t["name"]
        db.execute(f"DELETE FROM {table_name}")  # remove all rows
        db.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")  # reset AUTOINCREMENT

    db.commit()
    print("All tables truncated.")
