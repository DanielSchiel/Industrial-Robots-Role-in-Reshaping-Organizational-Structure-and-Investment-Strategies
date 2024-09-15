import pandas as pd

# Load the Excel files
matrix_df = pd.read_excel('Data/Manual Matching.xlsx', index_col=0)
abilities_df = pd.read_excel('Data/Abilities.xlsx')  # The ability descriptions

# List of professions to exclude
excluded_titles = [
    "Airline Pilots, Copilots, and Flight Engineers",
    "Firefighters",
    "Manufactured Building and Mobile Home Installers",
    "Commercial Pilots",
    "Police and Sheriff's Patrol Officers",
    "Models",
    "Proofreaders and Copy Markers",
    "Locker Room, Coatroom, and Dressing Room Attendants",
    "Door-to-Door Sales Workers, News and Street Vendors, and Related Workers",
    "Telemarketers"
]

# Step 1: Filter relevant columns
filtered_abilities_df = abilities_df[['Title', 'Element Name', 'Scale Name', 'Data Value']]

# Exclude the specified titles
filtered_abilities_df = filtered_abilities_df[~filtered_abilities_df['Title'].isin(excluded_titles)]

# Step 2: Calculate the average 'Data Value' for each 'Title' and 'Element Name'
averaged_abilities_df = filtered_abilities_df.groupby(['Title', 'Element Name']).agg({'Data Value': 'mean'}).reset_index()

# Step 3 and 4: Multiply the average value with the corresponding matrix values and sum the results
matrix_columns = matrix_df.columns
summed_results = []

for index, row in averaged_abilities_df.iterrows():
    title = row['Title']
    element_name = row['Element Name']
    data_value = row['Data Value']
    
    if element_name in matrix_columns:
        matrix_values = matrix_df[element_name].values
        multiplied_values = matrix_values * data_value
        summed_value = multiplied_values.sum()
        
        summed_results.append({
            'Title': title,
            'Element Name': element_name,
            'Data Value': data_value,
            'Summed Multiplied Value': summed_value
        })

# Step 5: Merge the summed results back into the original averaged DataFrame
summed_results_df = pd.DataFrame(summed_results)
final_df = pd.merge(averaged_abilities_df, summed_results_df[['Title', 'Element Name', 'Summed Multiplied Value']],
                    on=['Title', 'Element Name'])

# Additional Steps: Summing, Sorting, and Scaling
# Calculate the sum of 'Summed Multiplied Value' for each unique 'Title'
title_sums_df = final_df.groupby('Title').agg({'Summed Multiplied Value': 'sum'}).reset_index()

# Sort the results by 'Summed Multiplied Value'
sorted_title_sums_df = title_sums_df.sort_values(by='Summed Multiplied Value', ascending=False)

# Step 6: Scaling the results between 0 and 1
min_value = sorted_title_sums_df['Summed Multiplied Value'].min()
max_value = sorted_title_sums_df['Summed Multiplied Value'].max()
sorted_title_sums_df['Scaled Value'] = (sorted_title_sums_df['Summed Multiplied Value'] - min_value) / (max_value - min_value)

sorted_title_sums_df.rename(columns={"Title": "Occupation"}, inplace=True)
sorted_title_sums_df.drop(columns=["Summed Multiplied Value"], inplace=True)
sorted_title_sums_df.rename(columns={"Scaled Value": "IROE"}, inplace=True)
# Save the sorted DataFrame to an Excel file
output_path = 'Data/IROE.xlsx'


try:
    sorted_title_sums_df.to_excel(output_path, index=False)
    print(f"File saved successfully at: {output_path}")
except Exception as e:
    print(f"Error saving the file: {e}")

print(sorted_title_sums_df.head())
print(sorted_title_sums_df.shape)  # To check the number of rows and columns
