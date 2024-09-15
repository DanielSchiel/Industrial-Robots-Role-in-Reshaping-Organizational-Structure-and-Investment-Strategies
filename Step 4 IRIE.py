import os
import pandas as pd

# Define the path to the folder containing the Excel files
folder_path = 'Data/National Employment Matrix'

# Specify the columns to keep
columns_to_keep = ['Occupation Title', 'Occupation Code', 'Occupation Type', '2022 Percent of Industry']

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # Load the CSV file
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        
        # Keep only the specified columns if they exist in the file
        df = df[[col for col in columns_to_keep if col in df.columns]]
        
        # Save the cleaned dataframe back to a CSV file (overwriting the original)
        df.to_csv(file_path, index=False)
        
        print(f"Processed and saved {filename}.")

print("Processing complete for all CSV files in the folder.")



# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # Load the CSV file
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        
        # Remove rows where "Occupation Type" is "Summary"
        df = df[df['Occupation Type'] != 'Summary']
        
        # Save the cleaned dataframe back to the CSV file (overwriting the original)
        df.to_csv(file_path, index=False)
        
        print(f"Processed and saved {filename}.")


match_file_path = 'Data/U.S. Bureau Data occupations matched with IROE(ONet) occupations.xlsx'
# Load the Excel file that contains the "Occupation Code" and "IROE" data
match_df = pd.read_excel(match_file_path)

# Strip whitespace and ensure consistent capitalization in the "Occupation Code"
match_df['Occupation Code'] = match_df['Occupation Code'].str.strip().str.upper()

# Create a dictionary for quick lookup of IROE values based on Occupation Code
iroe_dict = pd.Series(match_df.IROE.values, index=match_df['Occupation Code']).to_dict()

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # Load the CSV file
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        
        # Clean up the "Occupation Code" by removing ="..." formatting
        df['Occupation Code'] = df['Occupation Code'].str.replace(r'="(.*)"', r'\1', regex=True).str.strip().str.upper()
        
        # Add a new "IROE" column to the dataframe and populate it with the corresponding values
        df['IROE'] = df['Occupation Code'].map(iroe_dict)
        
        # Debugging: Print a sample of the mappings to verify correctness
        print(f"Sample mapping for {filename}:")
        print(df[['Occupation Code', 'IROE']].head(10))  # Adjust the number to see more rows if needed
        
        # Save the updated dataframe back to the CSV file (overwriting the original)
        df.to_csv(file_path, index=False)
        
        print(f"Processed and updated {filename} with IROE data.")

print("Processing complete for all CSV files in the folder.")

# Create an empty DataFrame to store the results
result_df = pd.DataFrame(columns=['2022 National Employment Matrix code', 'IRIE'])

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # Load the CSV file
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        
        # Clean up the "Occupation Code" by removing ="..." formatting
        df['Occupation Code'] = df['Occupation Code'].str.replace(r'="(.*)"', r'\1', regex=True).str.strip().str.upper()
        
        # Add the "IROE" column by mapping the Occupation Code to IROE values
        df['IROE'] = df['Occupation Code'].map(iroe_dict)
        
        # Calculate the IRIE as the product of "2022 Percent of Industry" and "IROE"
        df['IRIE'] = df['2022 Percent of Industry'] * df['IROE']
        
        # Sum the IRIE values to get a single value for the entire file
        total_irie = df['IRIE'].sum()
        
        # Add a new row to the result_df with the filename and the total IRIE
        result_df = result_df.append({
            '2022 National Employment Matrix code': filename,
            'IRIE': total_irie
        }, ignore_index=True)

# Display the resulting DataFrame (not saving it)
result_df.head(20)  # Display the first 20 rows for inspection


# Load the "vorletzter step" Excel file
vorletzter_step_path = 'Data/U.S. Bureau Industry Overview.xlsx'
vorletzter_df = pd.read_excel(vorletzter_step_path)

# Clean up the "2022 National Employment Matrix code" column in the vorletzter_step file
vorletzter_df['2022 National Employment Matrix code'] = vorletzter_df['2022 National Employment Matrix code'].astype(str).str.zfill(6)

# Create a dictionary to map the codes to titles
code_to_title_dict = pd.Series(vorletzter_df['2022 National Employment Matrix title'].values, 
                               index=vorletzter_df['2022 National Employment Matrix code']).to_dict()

# Function to extract the numeric code from the filename in result_df
def extract_code(filename):
    # Assuming the code is the part after "IND_" and before ".csv"
    return filename.split('_')[-1].replace('.csv', '')

# Replace the "2022 National Employment Matrix code" in result_df with the title
result_df['2022 National Employment Matrix code'] = result_df['2022 National Employment Matrix code'].apply(extract_code).map(code_to_title_dict)

result_df = result_df.sort_values(by='IRIE', ascending=False)
result_df.columns = ['Industry', 'IRIE']
result_df[result_df.columns[0]] = result_df[result_df.columns[0]].str.lstrip()

# Scaling the values with the MinMaxScaler
min_value = result_df['IRIE'].min()
max_value = result_df['IRIE'].max()
sorted_title_sums_df['Scaled Value'] = (result_df['IRIE'] - min_value) / (max_value - min_value)

sorted_title_sums_df.head()

# Display the resulting DataFrame (not saving it)
# Save the DataFrame to an Excel file without the index
result_df.to_excel('Data/IRIE.xlsx', index=False)


