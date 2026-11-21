import csv
import io

RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
Guindy,2026-10-04,1500
"""


def load_clean(text):
    """Return valid station, date and PM2.5 records."""

    rows = []

    reader = csv.DictReader(io.StringIO(text))

    for row in reader:
        value = row["pm25"].strip()

        if value == "" or value.upper() == "NA":
            continue

        try:
            pm25 = float(value)
        except ValueError:
            continue

        if pm25 < 0 or pm25 > 999:
            continue

        rows.append((
            row["station"].strip().title(),
            row["date"].strip(),
            pm25
        ))

    return rows


def min_max(values):
    if not values:
        return []

    minimum = min(values)
    maximum = max(values)

    if maximum == minimum:
        return [0.0 for value in values]

    return [
        round((value - minimum) / (maximum - minimum), 3)
        for value in values
    ]


clean = load_clean(RAW)

print(clean)
print(min_max([pm for _, _, pm in clean]))
