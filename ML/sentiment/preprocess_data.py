import string
import numpy as np
import pickle

# Sample data
data = [
    ("I love this movie", 1),
    ("This film is terrible", 0),
    ("Amazing experience", 1),
    ("I hate this", 0),
]

# Preprocessing function
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    words = text.split()
    stopwords = {'the', 'a', 'of'}
    sentence = []
    for word in words:
        if word not in stopwords:
            sentence.append(word)
    return sentence

# Preprocess data
for i in range(len(data)):
    sentence, label = data[i]
    data[i] = (preprocess(sentence), label)

# Build vocabulary
vocab_set = set()
for tokens, _ in data:
    for word in tokens:
        vocab_set.add(word)

vocab_list = sorted(list(vocab_set))
word_to_index = {}
index = 0
for word in vocab_list:
    word_to_index[word] = index
    index += 1

# Vectorize sentences
vectors = []
for tokens, label in data:
    vector = [0] * len(word_to_index)
    for word in tokens:
        if word in word_to_index:
            index = word_to_index[word]
            vector[index] += 1
    vectors.append((vector, label))

# Convert to numpy arrays
X = []
y = []

for vector, label in vectors:
    X.append(vector)
    y.append(label)
X = np.array(X)
y = np.array(y)

# Save preprocessed data
with open("dataset.pkl", "wb") as f:
    pickle.dump((X, y, word_to_index), f)

print("Preprocessing done. Data saved to dataset.pkl")
