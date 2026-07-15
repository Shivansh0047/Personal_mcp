from fastmcp import FastMCP
import os
import sqlite3
import tempfile

# ==========================================================
# Database and File Paths
# ==========================================================

# Use the system temporary directory to avoid permission issues
TEMP_DIR = tempfile.gettempdir()

# SQLite database location
DB_PATH = os.path.join(TEMP_DIR, "expenses.db")

# Path to categories.json (stored beside this script)
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

print(f"Database path: {DB_PATH}")

# Create the MCP server
mcp = FastMCP("ExpenseTracker")


# ==========================================================
# Database Initialization
# ==========================================================

def init_db():
    """
    Creates the database and expenses table if they don't exist.
    Also verifies that the database is writable.
    """
    try:
        with sqlite3.connect(DB_PATH) as c:

            # Enable WAL mode for better concurrent access
            c.execute("PRAGMA journal_mode=WAL")

            # Create table
            c.execute("""
                CREATE TABLE IF NOT EXISTS expenses(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    subcategory TEXT DEFAULT '',
                    note TEXT DEFAULT ''
                )
            """)

            # Simple write test
            c.execute(
                "INSERT OR IGNORE INTO expenses(date, amount, category) VALUES ('2000-01-01', 0, 'test')"
            )
            c.execute("DELETE FROM expenses WHERE category='test'")

            print("Database initialized successfully with write access")

    except Exception as e:
        print(f"Database initialization error: {e}")
        raise


# Initialize database when server starts
init_db()


# ==========================================================
# Tool : Add Expense
# ==========================================================

@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
    """
    Add a new expense record.
    """

    try:
        with sqlite3.connect(DB_PATH) as c:

            cur = c.execute(
                """
                INSERT INTO expenses
                (date, amount, category, subcategory, note)
                VALUES (?, ?, ?, ?, ?)
                """,
                (date, amount, category, subcategory, note)
            )

            c.commit()

            return {
                "status": "success",
                "id": cur.lastrowid,
                "message": "Expense added successfully"
            }

    except sqlite3.OperationalError as e:

        if "readonly" in str(e).lower():
            return {
                "status": "error",
                "message": "Database is in read-only mode. Check file permissions."
            }

        return {
            "status": "error",
            "message": f"Database error: {str(e)}"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }


# ==========================================================
# Tool : List Expenses
# ==========================================================

@mcp.tool()
def list_expenses(start_date, end_date):
    """
    Return all expenses between the given dates.
    """

    try:
        with sqlite3.connect(DB_PATH) as c:

            cur = c.execute(
                """
                SELECT
                    id,
                    date,
                    amount,
                    category,
                    subcategory,
                    note
                FROM expenses
                WHERE date BETWEEN ? AND ?
                ORDER BY date DESC, id DESC
                """,
                (start_date, end_date)
            )

            cols = [d[0] for d in cur.description]

            return [
                dict(zip(cols, row))
                for row in cur.fetchall()
            ]

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error listing expenses: {str(e)}"
        }


# ==========================================================
# Tool : Expense Summary
# ==========================================================

@mcp.tool()
def summarize(start_date, end_date, category=None):
    """
    Summarize expenses grouped by category.
    Optionally filter by a single category.
    """

    try:
        with sqlite3.connect(DB_PATH) as c:

            query = """
                SELECT
                    category,
                    SUM(amount) AS total_amount,
                    COUNT(*) AS count
                FROM expenses
                WHERE date BETWEEN ? AND ?
            """

            params = [start_date, end_date]

            # Apply category filter if provided
            if category:
                query += " AND category = ?"
                params.append(category)

            query += """
                GROUP BY category
                ORDER BY total_amount DESC
            """

            cur = c.execute(query, params)

            cols = [d[0] for d in cur.description]

            return [
                dict(zip(cols, row))
                for row in cur.fetchall()
            ]

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error summarizing expenses: {str(e)}"
        }


# ==========================================================
# Resource : Expense Categories
# ==========================================================

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    """
    Return the list of supported expense categories.

    Reads categories.json if available.
    Falls back to a default category list otherwise.
    """

    try:

        default_categories = {
            "categories": [
                "Food & Dining",
                "Transportation",
                "Shopping",
                "Entertainment",
                "Bills & Utilities",
                "Healthcare",
                "Travel",
                "Education",
                "Business",
                "Other"
            ]
        }

        try:
            with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
                return f.read()

        except FileNotFoundError:
            import json
            return json.dumps(default_categories, indent=2)

    except Exception as e:
        return f'{{"error":"Could not load categories: {str(e)}"}}'


# ==========================================================
# Start MCP Server
# ==========================================================

if __name__ == "__main__":

    # Start HTTP server
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000
    )

    # For stdio transport, use:
    # mcp.run()