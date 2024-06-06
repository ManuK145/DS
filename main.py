import pandas as pd

#File paths
corp_pfd_path = r'/DS/corp_pfd.dif'
r_fields_path = r'/DS/reference_fileds.csv'

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

#Reading and filtering reference fields CSV
r_fields = pd.read_csv(r_fields_path)
r_fields = r_fields[r_fields['id_field'] == 1]

df = df[['ID_BB_GLOBAL','ID_BB_UNIQUE','ID_CUSIP','ID_ISIN','ID_SEDOL1','NAME','TICKER','EXCH_CODE']]
df

r_fields = pd.read_csv(r_fields_path)
rf_columns = [col.upper() for col in r_fields['field'] if col.upper() in df.columns] #Extracting the list of columns from r_fields that are present in the DataFrame

df = df[rf_columns]