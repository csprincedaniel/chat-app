import pickle
from tensorflow.keras.models import load_model

# Load vectorizer and model
with open("dataset_sparse.pkl", "rb") as f:
    _, _, vectorizer = pickle.load(f)

model = load_model("trained_model.h5")

# Preprocess function
def preprocess(text):
    import string
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Test sentence
sentence = "I really loved this movie!"
cleaned = preprocess(sentence)

# Convert to vector (sparse), then dense for model
X_new = vectorizer.transform([cleaned]).toarray()

# Predict
prob = model.predict(X_new, verbose=0)[0][0]
label = int(prob > 0.5)

print("Predicted probability of positive sentiment:", prob)
print("Predicted label (1=positive, 0=negative):", label)
