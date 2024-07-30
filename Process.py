import pandas as pd
from unidecode import unidecode

file_paths = [
    "data1.csv",
    "data2.csv",
    "data_1.csv",
    "data_2.csv"
]

output_file_path = "final_data.csv"

# Function to normalize text (remove accents)
def normalize_text(text):
    if isinstance(text, str):
        return unidecode(text)
    return text

# Initialize an empty DataFrame for consolidating data
consolidated_data = pd.DataFrame()

# Process each CSV file in the list
for file_path in file_paths:
    # Try different encodings until one works
    for encoding in ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252']:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            break  # If read is successful, exit the loop
        except UnicodeDecodeError:
            continue  # Try the next encoding

    # Normalize text in all columns
    df = df.applymap(normalize_text)

    # Append to the consolidated DataFrame
    consolidated_data = pd.concat([consolidated_data, df], ignore_index=True)

# Write the consolidated data to the output CSV file
consolidated_data.to_csv(output_file_path, index=False, encoding='utf-8')

print("Data has been consolidated and normalized into", output_file_path)