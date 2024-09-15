import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load your datasets
matrix_df = pd.read_excel('Data/Robot skills with descriptions.xlsx', index_col=0)  # The matrix you want to fill
abilities_df = pd.read_excel('Data/Human abilities with descriptions.xlsx')  # The ability descriptions

abilities = abilities_df['Abilities Element Name'].fillna('')
descriptions = abilities_df['Associated Work Activities'].fillna('')


# Combine the task names and ability descriptions into a single list for comparison
all_text = list(matrix_df.index) + list(descriptions)

# Convert the text data into TF-IDF vectors
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(all_text)

# Calculate cosine similarity
similarity_matrix = cosine_similarity(tfidf_matrix)

# Split the similarity matrix into task-to-ability and ability-to-ability similarities
task_ability_similarity = similarity_matrix[:len(matrix_df.index), len(matrix_df.index):]

# Define a function to assign 1, 0.5, or 0 based on similarity
def assign_value(similarity):
    if similarity > 0.01:  # High similarity, you can adjust the threshold
        return 1
    else:  # Low similarity
        return 0

# Apply the function to each cell in the matrix
for i, task in enumerate(matrix_df.index):
    for j, ability in enumerate(matrix_df.columns):
        similarity = task_ability_similarity[i, j]
        matrix_df.at[task, ability] = assign_value(similarity)

# Save the updated matrix to a new Excel file
matrix_df.to_excel('Data/LLM Matching 1 and 0 input.xlsx')

print("Matrix successfully updated and saved!")


print(matrix_df.shape)  # Shape of the task-ability matrix
print(task_ability_similarity.shape)  # Shape of the similarity matrix
print(task_ability_similarity)
for i in task_ability_similarity:
    print(i)