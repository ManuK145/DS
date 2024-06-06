import pandas as pd

#File paths
corp_pfd_path = r'/DS/corp_pfd.dif'
r_fields_path = r'/DS/reference_fileds.csv'
r_securities_path = r'/DS/reference_securities.csv'

#Reading the DIF file
with open(corp_pfd_path, 'r') as file:
    lines = file.readlines()

columns = []
data = []
collect_columns = False
collect_data = False

#Parsing the DIF file
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
        if '#' not in line and len(line) > 0:
            columns.append(line)
    elif collect_data:
        data.append(line.split('|')[:-1])

# Creating DataFrame from parsed data
df = pd.DataFrame(data, columns=columns)

r_fields = pd.read_csv(r_fields_path)
rf_columns = [col.upper() for col in r_fields['field'] if col.upper() in df.columns] #Extracting the list of columns from r_fields that are present in the DataFrame

df = df[rf_columns]

r_securities = pd.read_csv(r_securities_path)
rs_columns = [col.upper() for col in r_securities.columns]

new_securities = df[~df['ID_BB_GLOBAL'].isin(r_securities['ID_BB_GLOBAL'.lower()])]
new_securities = new_securities.drop_duplicates(subset=['ID_BB_GLOBAL'])

new_securities[rs_columns].to_csv('new_securities.csv ', index = False)

security_data = []

for index, row in new_securities.iterrows():
    security_data.append({
        'ID_BB_GLOBAL': row['ID_BB_GLOBAL'],
        'FIELD': ', '.join(rf_columns),
        'VALUE': ', '.join([row[col] for col in rf_columns]),
        'SOURCE': 'corp_pfd.dif',
        'TSTAMP': pd.Timestamp.now() 
    })

security_data = pd.DataFrame(security_data)
security_data.to_csv('security_data', index = False)