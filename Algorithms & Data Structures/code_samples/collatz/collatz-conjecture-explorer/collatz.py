import sqlite3
import datetime
import signal
import sys
from statistics import median, pstdev

DB_FILE = "collatz.db"
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

# Define the database structure.
def setup_database():
    """
    Create the required tables in the database.
    """
    tables = {
        "collatz": """CREATE TABLE IF NOT EXISTS collatz (
                      starting_number INTEGER,
                      number_of_steps INTEGER,
                      max_value INTEGER,
                      sequence_length INTEGER,
                      convergence INTEGER,
                      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                      )""",
        "distribution": """CREATE TABLE IF NOT EXISTS distribution (
                           stat_name TEXT,
                           value REAL
                           )""",
        "sequence_length": """CREATE TABLE IF NOT EXISTS sequence_length (
                              number INTEGER PRIMARY KEY,
                              steps INTEGER
                              )""",
        "convergence": """CREATE TABLE IF NOT EXISTS convergence (
                          number INTEGER PRIMARY KEY,
                          converges INTEGER
                          )""",
        "date_time": """CREATE TABLE IF NOT EXISTS date_time (
                        id INTEGER PRIMARY KEY,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        )""",
    }

    for table in tables.values():
        c.execute(table)


# Check the Collatz conjecture for the given number.
def check_collatz(n):
    """
    Perform the Collatz conjecture for a number n.
    """
    original_n, steps, max_value = n, 0, n
    sequence = []

    while True:
        sequence.append(n)
        c.execute("SELECT steps FROM sequence_length WHERE number = ?", (n,))
        row = c.fetchone()

        if row:
            steps += row[0]
            break
        elif n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1

        steps += 1
        max_value = max(max_value, n)

        if n in {1, 2, 4}:
            break

    for i, num in enumerate(sequence):
        c.execute(
            "INSERT OR REPLACE INTO sequence_length VALUES (?, ?)", (num, steps - i)
        )

    converges = 1 if n == 1 else 0
    c.execute(
        "INSERT OR REPLACE INTO convergence VALUES (?, ?)", (original_n, converges)
    )

    return steps, max_value, steps - 1, converges


# Calculate statistics after the script is stopped.
def calculate_stats():
    """
    Calculate basic statistical values for max_values.
    """
    c.execute("SELECT max_value FROM collatz")
    max_values = [row[0] for row in c.fetchall()]

    stats = {
        "min": min(max_values) if max_values else 0,
        "max": max(max_values) if max_values else 0,
        "mean": sum(max_values) / len(max_values) if max_values else 0,
        "median": median(max_values) if max_values else 0,
        "std_dev": pstdev(max_values) if max_values else 0,
    }

    for stat, value in stats.items():
        c.execute("INSERT INTO distribution VALUES (?, ?)", (stat, value))


# Define shutdown operations.
def shutdown(signal, frame):
    """
    Perform operations needed before shutdown.
    """
    calculate_stats()
    conn.close()
    sys.exit(0)


# The main function.
def main():
    """
    Main function to process each number for the Collatz conjecture.
    """
    setup_database()

    c.execute("SELECT MAX(starting_number) FROM collatz")
    last_number = c.fetchone()[0]
    start_number = last_number + 1 if last_number else 1

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    for i in range(start_number, float("inf")):
        print(f"Processing: {i}")
        try:
            steps, max_value, sequence_length, converges = check_collatz(i)
        except Exception as e:
            print(f"Error encountered while processing {i}: {e}")
            break

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(
            "INSERT INTO collatz VALUES (?, ?, ?, ?, ?, ?)",
            (i, steps, max_value, sequence_length, converges, timestamp),
        )
        c.execute("INSERT INTO date_time (id) VALUES (?)", (i,))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
