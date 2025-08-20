from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

x = np.array([
    [1],[2],[3],[4],[5],
    [6],[7],[8],[9],[10],
    [11],[12],[13],[14],[15],
    [16],[17],[18],[19],[20],
    [21],[22],[23],[24],[25],
    [26],[27],[28],[29],[30],
    [31],[32],[33],[34],[35],
    [36],[37],[38],[39],[40],
    [41],[42],[43],[44],[45],
    [46],[47],[48],[49],[50]
], dtype=float)

y = np.array([
    2,4,6,8,10,
    12,14,16,18,20,
    22,24,26,28,30,
    32,34,36,38,40,
    42,44,46,48,50,
    52,54,56,58,60,
    62,64,66,68,70,
    72,74,76,78,80,
    82,84,86,88,90,
    92,94,96,98,100
], dtype=float)

model2 = keras.Sequential([
    keras.Input(shape=(1,)),
    keras.layers.Dense(1)
])

#optimize
optimizer = keras.optimizers.SGD(learning_rate=0.001)

#compile
model2.compile(optimizer=optimizer, loss="mean_squared_error")

#train
model2.fit(x, y, epochs=500, verbose=0)


#predict values
print(model2.predict(np.array([[6],[7]])))
