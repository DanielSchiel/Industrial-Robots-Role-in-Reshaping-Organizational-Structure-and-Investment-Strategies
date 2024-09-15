import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the Excel files
df1 = pd.read_excel('Data/Manual Matching.xlsx')
df2 = pd.read_excel('Data/LLM Matching.xlsx')

# Replace all non-zero values with 1s
df1_replaced = df1.applymap(lambda x: 1 if x != 0 else 0)
df2_replaced = df2.applymap(lambda x: 1 if x != 0 else 0)

# Perform correlation analysis between the two DataFrames for each row
correlation_matrix = df1_replaced.corrwith(df2_replaced, axis=1)

# Calculate the overall correlation between the two datasets
overall_correlation = df1_replaced.stack().corr(df2_replaced.stack())

# Display the correlation results
print("Overall Correlation:", overall_correlation)

# List of x-axis labels as provided
xtick_labels = [
    "Metal casting", "Plastic moulding", "Stamping forging, bending", 
    "Handling operations at machine tools", "Machine tending for other processes", 
    "Measurement, inspection, testing", "Palletizing", "Packaging, picking, placing", 
    "Material handling", "Arc welding", "Spot welding", "Laser welding", 
    "other welding", "Soldering", "Painting and enamelling", 
    "Application of adhesive, sealing material", "Others dispensing/spraying", 
    "Laser cutting", "Water jet cutting", "Mechanical cutting/grinding/deburring....", 
    "Other processing", "Disassembling", "Assembling and disassembling", 
    "Processing", "Dispensing", "Welding and soldering", 
    "Handling operations / Machine Tending", "Cleanroom for FPD", 
    "Cleanroom for semiconductors", "Dispensing unspecified", 
    "Processing unspecified", "Assembling unspecified", 
    "Handling operations unspecified", "Welding unspecified", 
    "Cleanroom for others", "Assembling"
]

# Plotting the split-up correlations for each row in academic-friendly style
plt.figure(figsize=(14, 8))  # Adjusted size for better readability

# Plot with provided labels as x-axis labels
plt.plot(correlation_matrix.index, correlation_matrix.values, color='black', linestyle='-', linewidth=1.5)
plt.axhline(0, color='grey', linewidth=0.5)

# Set the x-ticks and labels using the provided labels
plt.xticks(ticks=range(len(xtick_labels)), labels=xtick_labels, rotation=90, fontname='Times New Roman', fontsize=10)

# Adding labels and title with overall correlation in Times New Roman font
plt.xlabel('', fontname='Times New Roman')
plt.ylabel('Correlation Value', fontname='Times New Roman')
plt.title(f'Correlation Manual Matching vs. LLM Matching Overall Correlation: {overall_correlation:.3f}', fontname='Times New Roman')
plt.grid(True)

# Adjust layout for better fit
plt.tight_layout()
plt.show()
