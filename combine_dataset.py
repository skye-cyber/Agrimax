import pandas as pd

# Load the datasets
df1 = pd.read_csv('dataset/data1.csv')  # Replace with your first dataset file path
df2 = pd.read_csv('dataset/synthetic_dataset.csv')  # Replace with your second dataset file path

# Combine the datasets
combined_df = pd.concat([df1, df2], ignore_index=True)

# Remove duplicate rows
# This considers entire rows for duplication; adjust 'subset' if you only want to consider certain columns
cleaned_df = combined_df.drop_duplicates()

# Save the combined and cleaned dataset
cleaned_df.to_csv('dataset/Synthetic_dataset1.csv', index=False)
