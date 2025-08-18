import pickle
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import layers, models

# Load preprocessed data
with open("dataset.pkl", "rb") as f:
    X, y, word_to_index = pickle.load(f)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Build neural network
input_size = X_train.shape[1]
model = models.Sequential([
    layers.Input(shape=(input_size,)),  # input layer
    layers.Dense(16, activation="relu"),  # hidden layer
    layers.Dense(1, activation="sigmoid")  # output layer
])

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

# Train the model
history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=2,
    validation_data=(X_test, y_test),
    verbose=1
)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print("Test accuracy:", accuracy)

# Make predictions on test data
pred_probs = model.predict(X_test)
pred_labels = (pred_probs > 0.5).astype(int)

print("Predicted labels:", pred_labels.reshape(-1))
print("True labels:     ", y_test)
