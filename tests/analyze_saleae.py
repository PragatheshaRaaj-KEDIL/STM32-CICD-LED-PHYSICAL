from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "test-results" / "saleae"

csv_file = OUT / "digital.csv"

print("=" * 60)
print("SALEAE ANALYSIS")
print("=" * 60)

if not csv_file.exists():
    raise FileNotFoundError(f"Saleae CSV not found: {csv_file}")

print("Reading:", csv_file)

with open(csv_file, newline="") as f:
    rows = list(csv.reader(f))

if len(rows) < 2:
    raise RuntimeError("Saleae CSV contains no samples.")

print("Samples:", len(rows) - 1)

header = rows[0]
print("Header:", header)

# Detect transitions in the first digital data column.
values = []

for row in rows[1:]:
    if len(row) >= 2:
        values.append(row[1])

unique_values = set(values)

print("Detected logic states:", unique_values)

if len(unique_values) < 2:
    raise RuntimeError(
        "FAIL: GPIO did not toggle. "
        "Only one logic state was captured."
    )

print("=" * 60)
print("PASS: GPIO TOGGLE DETECTED")
print("=" * 60)