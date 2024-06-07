import pandas as pd

#File paths
corp_pfd_path = r'corp_pfd.dif'
r_fields_path = r'reference_fileds.csv'
r_securities_path = r'reference_securities.csv'

#Reading the DIF file
with open(corp_pfd_path, 'r') as file:
    lines = file.readlines()

columns = []    # Will hold column names
data = []       # Will store rows of data

# DIF files have START/END markers to delimit sections
collect_columns = False # Flags when we're reading column names
collect_data = False    # Flags when we're reading data rows

#Parsing the DIF file
for line in lines:
    line = line.strip() # Remove extra whitespace
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
        data.append(line.split('|')[:-1]) # Collect data rows, splitting on '|' and removing extra delimiter

# Creating DataFrame from parsed data
df = pd.DataFrame(data, columns=columns)

# --- 2. Create DataFrame and Validate Using Reference Fields ---
# Load reference fields to ensure we only keep valid columns
r_fields = pd.read_csv(r_fields_path)
rf_columns = [col.upper() for col in r_fields['field'] if col.upper() in df.columns] #Extracting the list of columns from r_fields that are present in the DataFrame

# Filter the DataFrame to only include columns from reference fields
df = df[rf_columns]

# --- 3. Identify New Securities ---
# Load the reference securities file to compare against
r_securities = pd.read_csv(r_securities_path)
rs_columns = [col.upper() for col in r_securities.columns]

# Find securities in df NOT present in r_securities (using ID_BB_GLOBAL)
new_securities = df[~df['ID_BB_GLOBAL'].isin(r_securities['ID_BB_GLOBAL'.lower()])]

# Remove any duplicate new securities based on ID_BB_GLOBAL
new_securities = new_securities.drop_duplicates(subset=['ID_BB_GLOBAL'])

# --- 4. Create `new_securities.csv` ---
new_securities[rs_columns].to_csv('new_securities.csv ', index = False)

# --- 5. Generate `security_data.csv` ---
security_data = []

# Create rows for security_data.csv, one per new security
for index, row in new_securities.iterrows():
    security_data.append({
        'ID_BB_GLOBAL': row['ID_BB_GLOBAL'],
        'FIELD': ', '.join(rf_columns),
        'VALUE': ', '.join([row[col] for col in rf_columns]),
        'SOURCE': 'corp_pfd.dif',
        'TSTAMP': pd.Timestamp.now() 
    })

# Create DataFrame for security_data and save to CSV
security_data = pd.DataFrame(security_data)
security_data.to_csv('security_data.csv', index = False)