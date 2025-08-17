import string

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

print("Vocabulary:", word_to_index)

# Vectorize sentences
vectors = []
for tokens, label in data:
    vector = [0] * len(word_to_index)
    for word in tokens:
        if word in word_to_index:
            index = word_to_index[word]
            vector[index] += 1
    vectors.append((vector, label))

print("Vectors:", vectors)

"""TO DO
Convert vectors and labels into arrays

So they can be fed into a neural network.

Use explicit loops if avoiding list comprehensions.

Train/test split

Separate data into training and testing sets to evaluate performance.

Build the neural network

Define input size, hidden layers, and output layer.

Compile the model with a loss function and optimizer.

Train the model

Fit the network on your training data.

Evaluate the model

Predict on test data and calculate accuracy (or other metrics).

Optional improvements

Larger stopword set, lemmatization, TF-IDF instead of counts, more data.

"""