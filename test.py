import pandas as pd

# Read the file into a DataFrame
# Adjust the file path and delimiter if needed
df = pd.read_csv('final_data.txt', delimiter='\t')  # Use '\t' for tab-separated values or ',' for comma-separated

# Drop the date column (assuming it's the third column, index 2)
df = df.drop(df.columns[2], axis=1)

# Save the DataFrame to a new file
df.to_csv('data_without_date.txt', index=False, sep='\t')  # Use '\t' for tab-separated values or ',' for comma-separated