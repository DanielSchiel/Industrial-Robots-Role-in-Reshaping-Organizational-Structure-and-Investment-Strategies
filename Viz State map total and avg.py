import pandas as pd
import folium
import pickle
from folium import Choropleth


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

# Create a function to extract the state from the AREA_TITLE
def extract_state(area_title):
    return area_title.split(", ")[-1] if ", " in area_title else None

# Add state information to the dataframe
geo_viz['State'] = geo_viz['AREA_TITLE'].apply(extract_state)

# Aggregate the data by state, summing the 'Result' values (for both scaled and total)
state_data_avg = geo_viz.groupby('State')['Result'].sum().reset_index()
state_data_total = geo_viz.groupby('State')['Result_Total'].sum().reset_index()

# Prepare the state geo data
geo_json_data = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json"

# Create the first map (average per person)
m1 = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Add the Choropleth layer for the first map
Choropleth(
    geo_data=geo_json_data,
    name='choropleth',
    data=state_data_avg,
    columns=['State', 'Result'],
    key_on='feature.id',  # This assumes that the GeoJSON file's feature id matches state abbreviations
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Average Result by State (Per Person)'
).add_to(m1)

# Add layer control to toggle between layers
folium.LayerControl().add_to(m1)

# Save the first map as an HTML file
m1.save('Data/State map avg.html')

# Create the second map (overall total)
m2 = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Add the Choropleth layer for the second map
Choropleth(
    geo_data=geo_json_data,
    name='choropleth',
    data=state_data_total,
    columns=['State', 'Result_Total'],
    key_on='feature.id',  # This assumes that the GeoJSON file's feature id matches state abbreviations
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Total Result by State'
).add_to(m2)

# Add layer control to toggle between layers
folium.LayerControl().add_to(m2)

# Save the second map as an HTML file
m2.save('Data/State map total.html')

print("Choropleth maps saved as 'state_choropleth_map_avg.html' and 'state_choropleth_map_total.html'.")

