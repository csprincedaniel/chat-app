import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import pickle
import os

base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "IMDB_Dataset.csv")

# Load CSV
df = pd.read_csv(file_path)

# Preprocess function
def preprocess(text):
    import string
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

texts = df['review'].apply(preprocess).tolist()
labels = (df['sentiment'] == 'positive').astype(int).values

# Vectorize using sparse CountVectorizer
vectorizer = CountVectorizer(stop_words=['the', 'a', 'of'])
X = vectorizer.fit_transform(texts)  # sparse matrix
y = labels

# Save sparse matrix and vectorizer
with open(os.path.join(base_path, "dataset_sparse.pkl"), "wb") as f:
    pickle.dump((X, y, vectorizer), f)
