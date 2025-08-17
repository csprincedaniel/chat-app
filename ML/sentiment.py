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

# Vectorize sentences. (I did not write the vector code. I need to analyze)
vectors = []
for tokens, label in data:
    vector = [0] * len(word_to_index)
    for word in tokens:
        if word in word_to_index:
            index = word_to_index[word]
            vector[index] += 1
    vectors.append((vector, label))

print("Vectors:", vectors)


#CONVERT DATA INTO NUMPY ARRAYS
import numpy as np
X = []
y = []

for vector, label in vectors:
    X.append(X)
    y.append(y)
X = np.array(x)
y = np.array(y)
print("Input array shape:", X.shape)
print("Label array shape:", y.shape)

#SPLIT DATA INTO TRAINING AND TESTING
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size = 0.2, random_state=42
)
print("Train set size: ",X_train.shape[0])
print("Test set size: ",X_test.shape[0])


#NEURAL NETWORK
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

input_size = X_train.shape[1]
model = keras.Sequential([
    layers.Input(shape=(input_size,)), #input layer
    layers.Dense(16, activation="relu"), #hidden layer
    layers.Dense(1, activation="sigmoid") #output layer
])

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

# Train the model
history = model.fit(
    X_train, y_train,
    epochs=20,          # how many passes through the data
    batch_size=2,       # how many samples per gradient update
    validation_data=(X_test, y_test),  # track test performance while training
    verbose=1
)
# EVALUATION (I Didn't write this. I need to analyze later)
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print("Test accuracy:", accuracy)

# Make predictions on test data
pred_probs = model.predict(X_test)
pred_labels = (pred_probs > 0.5).astype(int)

print("Predicted labels:", pred_labels.reshape(-1))
print("True labels:     ", y_test)

"""THE OLD TODO LIST. I ALR FIGURED IT OUT. JUST KEEPING IT FOR FUTURE REFERENCE.
Here’s your TO DO list converted into clear steps:

1. **Convert data into arrays**

   * Transform vectors and labels into array format suitable for a neural network.
   * Use explicit loops if avoiding list comprehensions.

2. **Split data into training and testing sets**

   * Separate your dataset to evaluate model performance.

3. **Build the neural network**

   * Define input size, hidden layers, and output layer.
   * Compile the model with a loss function and optimizer.

4. **Train the model**

   * Fit the network using the training data.

5. **Evaluate the model**

   * Predict on the test data.
   * Calculate accuracy or other performance metrics.

6. **Optional improvements**

   * Expand stopword set.
   * Apply lemmatization.
   * Use TF-IDF instead of raw counts.
   * Add more training data.
"""