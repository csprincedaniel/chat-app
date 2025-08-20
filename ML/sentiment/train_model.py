import os
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models

# Determine script directory and file path
base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "dataset_sparse.pkl")

# Load sparse preprocessed data
with open(file_path, "rb") as f:
    X_sparse, y, vectorizer = pickle.load(f)

# Split data
X_train_sparse, X_test_sparse, y_train, y_test = train_test_split(
    X_sparse, y, test_size=0.2, random_state=42
)

# Build neural network
input_size = X_train_sparse.shape[1]
model = models.Sequential([
    layers.Input(shape=(input_size,)),  # input layer
    layers.Dense(256, activation="relu"),  # hidden layer
    layers.Dense(128, activation="relu"),  # hidden layer
    layers.Dense(1, activation="sigmoid")  # output layer
])

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

# Helper generator to feed sparse data in batches
def batch_generator(X_sparse, y, batch_size):
    num_samples = X_sparse.shape[0]
    for i in range(0, num_samples, batch_size):
        X_batch = X_sparse[i:i+batch_size].toarray()  # convert sparse to dense
        y_batch = y[i:i+batch_size]
        yield X_batch, y_batch

# Train the model
batch_size = 64
epochs = 20
for epoch in range(epochs):
    for X_batch, y_batch in batch_generator(X_train_sparse, y_train, batch_size):
        model.train_on_batch(X_batch, y_batch)

# Save trained model
model.save(os.path.join(base_path, "trained_model.h5"))

# Evaluate on test data
pred_labels = []
batch_size_eval = 1024
for i in range(0, X_test_sparse.shape[0], batch_size_eval):
    X_batch = X_test_sparse[i:i+batch_size_eval].toarray()
    probs = model.predict(X_batch, verbose=0)
    pred_labels.extend((probs > 0.5).astype(int).reshape(-1))

pred_labels = np.array(pred_labels)
accuracy = (pred_labels == y_test).mean()
print("Test accuracy:", accuracy)
