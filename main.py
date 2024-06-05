import pandas as pd

file_path = r'/DS/corp_pfd.dif'

with open(file_path, 'r') as file:
    lines = file.readlines()

columns = []
data = []
collect_columns = False
collect_data = False

for line in lines:
    line = line.strip()
    if line == 'START-OF-FIELDS':
        collect_columns = True
        continue
    elif line == 'END-OF-FIELDS':
        collect_columns = False
        continue
    elif line == 'START-OF-DATA':
        collect_data = True
        continue
    elif line == 'END-OF-DATA':
        collect_data = False
        continue

    if collect_columns:
        columns.append(line)
    elif collect_data:
        data.append(line.split('|'))

# Find the maximum number of fields in data rows
max_fields = max(len(row) for row in data)

# Ensure all data rows have the same number of fields as columns by padding with None
data = [row + [None] * (max_fields - len(row)) for row in data]

df = pd.DataFrame(data, columns=columns[:max_fields])
