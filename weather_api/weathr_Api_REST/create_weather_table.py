import sqlite3

conn = sqlite3.connect("weather.db")
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY,
        city TEXT,
        date DATE,
        min_temp REAL,
        max_temp REAL,
        avg_temp REAL,
        humidity REAL
    );
""")

conn.commit()
conn.close()