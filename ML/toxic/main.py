from tensorflow import keras
from keras.layers import TextVectorization, Dense, Input
import numpy as np

# Texts and labels
texts = [
    "you are nice",
    "have a great day",
    "you are stupid",
    "shut up idiot",
    "kind and helpful",
    "go to hell"
]
labels = np.array([0, 0, 1, 1, 0, 1])

# Create vectorizer
vectorizer = TextVectorization(output_mode="tf-idf")
vectorizer.adapt(texts)

# Precompute numeric vectors
x_numeric = vectorizer(np.array(texts))

# Define model (numeric input only)
model = keras.Sequential([
    Input(shape=(x_numeric.shape[1],)),
    Dense(8, activation="relu"),
    Dense(1, activation="sigmoid")
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Train
model.fit(x_numeric, labels, epochs=50, verbose=1)

# Predict on new samples
samples = np.array(["you are kind", "stupid fool"])
x_samples = vectorizer(samples)
print(model.predict(x_samples))