from main import RNN
model = RNN()
model.load_weights('model_weight')

Ex = 100000000
En = 5000000
He = 20000000

import numpy as np

x = np.empty((1, 1000, 1),dtype=np.float32)
for i in range(1000):
    En_ = np.random.normal(loc=En, scale=He)
    x[0, i, 0] = np.random.normal(loc=Ex, scale=np.abs(En_))

print(model.predict(x).numpy())