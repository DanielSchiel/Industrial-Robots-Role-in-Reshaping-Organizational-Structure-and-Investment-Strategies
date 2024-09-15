import pandas as pd
import folium
import pickle
from folium import Choropleth

# NEEDS TO WORK FROM HERE

# Load the necessary variables from previous steps
file_path = 'Data/MSA_M2023_dl.xlsx'
df = pd.read_excel(file_path)

df_filtered = df[df['O_GROUP'].astype(str) == "detailed"]
df_filtered = df_filtered[["AREA", "AREA_TITLE", "OCC_CODE", "TOT_EMP"]]

# Load the second Excel file
second_df = pd.read_excel('Data/U.S. Bureau Data occupations matched with IROE(ONet) occupations.xlsx')

# Ensure that "OCC_CODE" in the first dataframe and "Occupation Code" in the second are both strings
df_filtered['OCC_CODE'] = df_filtered['OCC_CODE'].astype(str)
second_df['Occupation Code'] = second_df['Occupation Code'].astype(str)

# Convert the 'TOT_EMP' column to numeric
df_filtered['TOT_EMP'] = pd.to_numeric(df_filtered['TOT_EMP'], errors='coerce')

# Merge the dataframes on the "OCC_CODE" from the first dataframe and "Occupation Code" from the second dataframe
merged_df = pd.merge(df_filtered, second_df[['Occupation Code', 'IROE']], how='left', left_on='OCC_CODE', right_on='Occupation Code')

# Create the new column by multiplying "TOT_EMP" with "IROE"
merged_df['TOT_EMP_x_IROE'] = merged_df['TOT_EMP'] * merged_df['IROE']

# Group by 'AREA_TITLE' and sum 'TOT_EMP_x_IROE' and 'TOT_EMP'
grouped_df = merged_df.groupby('AREA_TITLE').agg({
    'TOT_EMP_x_IROE': 'sum',
    'TOT_EMP': 'sum'
}).reset_index()

# Calculate the desired value for each 'AREA_TITLE'
grouped_df['Result'] = grouped_df['TOT_EMP_x_IROE'] / grouped_df['TOT_EMP']  # Average per person

# Create a second version without scaling by TOT_EMP
grouped_df['Result_Total'] = grouped_df['TOT_EMP_x_IROE']  # Overall total, not scaled

# Rename the resulting DataFrame to 'geo_viz'
geo_viz = grouped_df[['AREA_TITLE', 'Result', 'Result_Total']]

# Load the geocode cache
with open('Data/geocode_cache.pkl', 'rb') as f:
    geocode_cache = pickle.load(f)

# Add state information to the dataframe (if needed)
geo_viz['State'] = geo_viz['AREA_TITLE'].apply(lambda x: x.split(", ")[-1] if ", " in x else None)

# Prepare the county geo data
county_geo_json_data = "Data/metropolitan-statistical-area!micropolitan-statistical-area.json"  # Replace with your actual GeoJSON file path

# Create the third map (average per person at the county/MSA level)
m3 = folium.Map(location=[37.0902, -95.7129], zoom_start=5)

# Add the Choropleth layer for the county/MSA average map
Choropleth(
    geo_data=county_geo_json_data,
    name='choropleth',
    data=geo_viz,
    columns=['AREA_TITLE', 'Result'],
    key_on='feature.properties.NAME',  # Adjust this to match your GeoJSON file's property for MSA names
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Average Result by MSA (Per Person)'
).add_to(m3)

# Add layer control to toggle between layers
folium.LayerControl().add_to(m3)

# Save the third map as an HTML file
m3.save('Data/Msa map avg.html')

# Create the fourth map (total result at the county/MSA level)
m4 = folium.Map(location=[37.0902, -95.7129], zoom_start=5)

# Add the Choropleth layer for the county/MSA total map
Choropleth(
    geo_data=county_geo_json_data,
    name='choropleth',
    data=geo_viz,
    columns=['AREA_TITLE', 'Result_Total'],
    key_on='feature.properties.NAME',  # Adjust this to match your GeoJSON file's property for MSA names
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Total Result by MSA'
).add_to(m4)

# Add layer control to toggle between layers
folium.LayerControl().add_to(m4)

# Save the fourth map as an HTML file
m4.save('Data/Msa map total.html')

print("Choropleth maps saved as 'msa_choropleth_map_avg.html' and 'msa_choropleth_map_total.html'. Data saved as 'geo_viz_data.pkl'.")
