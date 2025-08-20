from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

x=np.array([[0,0],[0,1],[1,0],[1,1]], dtype=float)
y=np.array([0,1,1,1], dtype=float)

model = keras.Sequential([
    layers.Dense(1, input_shape=(2,), activation="sigmoid")
])

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.1), 
              loss="binary_crossentropy", metrics=["accuracy"])
model.summary()

model.fit(x,y, epochs=500, verbose = 0)

print(model.predict(x))
