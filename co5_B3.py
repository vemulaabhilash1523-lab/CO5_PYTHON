import csv
import sqlite3
import importlib
from collections import defaultdict

try:
    pd = importlib.import_module("pandas")
except ImportError:
    pd = None

data = [
    ("Adyar", "2026-10-01", 48),
    ("Adyar", "2026-10-01", 52),
    ("Guindy", "2026-10-01", 90),
    ("Guindy", "2026-10-01", 100),
    ("Adyar", "2026-10-02", 60),
    ("Guindy", "2026-10-02", 120)
]

# Create CSV file
with open("small_air_quality.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["station", "date", "pm25"])
    writer.writerows(data)


# Method 1: Plain Python and CSV
groups = defaultdict(list)

with open("small_air_quality.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        key = (row["station"], row["date"])
        groups[key].append(float(row["pm25"]))

python_result = {
    key: sum(values) / len(values)
    for key, values in groups.items()
}


# Method 2: Pandas
df = pd.read_csv("small_air_quality.csv")

pandas_result = (
    df.groupby(["station", "date"])["pm25"]
    .mean()
    .to_dict()
)


# Method 3: SQLite
con = sqlite3.connect(":memory:")

con.execute("""
CREATE TABLE readings (
    station TEXT,
    date TEXT,
    pm25 REAL
)
""")

con.executemany(
    "INSERT INTO readings VALUES (?, ?, ?)",
    data
)

sql_result = con.execute("""
SELECT station, date, AVG(pm25)
FROM readings
GROUP BY station, date
""").fetchall()

sql_result = {
    (station, date): average
    for station, date, average in sql_result
}


print("Python:", python_result)
print("Pandas:", pandas_result)
print("SQL:", sql_result)

print(
    "All results agree:",
    all(
        abs(python_result[key] - pandas_result[key]) < 1e-9
        and abs(python_result[key] - sql_result[key]) < 1e-9
        for key in python_result
    )
)

con.close()
