import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the Excel files
df1 = pd.read_excel('Data/IROE.xlsx')
df2 = pd.read_excel('Data/IROE LLM.xlsx')

# Keep only the relevant columns ("Title" and "Scaled Value")
df1 = df1[['Occupation', 'IROE']]
df1.columns = ['Title', 'Scaled Value']
df2 = df2[['Title', 'Scaled Value']]

df1.head()
df2.head()

# Merge the dataframes on the "Title" column
merged_df = pd.merge(df1, df2, on='Title', suffixes=('_1', '_2'))

# Calculate the correlation between the scaled values
correlation = merged_df['Scaled Value_1'].corr(merged_df['Scaled Value_2'])

# Plotting
plt.figure(figsize=(10, 6))

# Replace job titles with a simple index
x_indices = range(1, len(merged_df) + 1)

# Plot the scaled values for both datasets without markers
plt.plot(x_indices, merged_df['Scaled Value_1'], label='Manual', color='black', linestyle='-', linewidth=1.5)
plt.plot(x_indices, merged_df['Scaled Value_2'], label='LLM', color='grey', linestyle='-', linewidth=1.5)

# Adding labels and title with correlation included
plt.xlabel('Index')
plt.ylabel('Scaled Value')
plt.title(f'Scaled Value Comparison LLM Matching vs Manual Matching Overall Correlation: {correlation:.2f}', fontname='Times New Roman')
plt.xticks(rotation=90)
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
