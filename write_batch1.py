import csv

# Read existing header
with open('backend/data/phones_enriched.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

print(f"Header has {len(header)} columns")
print(header)