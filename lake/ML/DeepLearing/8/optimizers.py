# from . import schedules
# from tensorflow.python.keras.optimizer_v2.adadelta import Adadelta
# from tensorflow.python.keras.optimizer_v2.adagrad import Adagrad
# from tensorflow.python.keras.optimizer_v2.adam import Adam
# from tensorflow.python.keras.optimizer_v2.adamax import Adamax
# from tensorflow.python.keras.optimizer_v2.ftrl import Ftrl
# from tensorflow.python.keras.optimizer_v2.gradient_descent import SGD
# from tensorflow.python.keras.optimizer_v2.nadam import Nadam
# from tensorflow.python.keras.optimizer_v2.optimizer_v2 import OptimizerV2 as Optimizer
# from tensorflow.python.keras.optimizer_v2.rmsprop import RMSprop
# from tensorflow.python.keras.optimizers import deserialize
# from tensorflow.python.keras.optimizers import get
# from tensorflow.python.keras.optimizers import serialize


import tensorflow.keras.optimizers as optim

optimizer = optim.Ftrl(lr=0.02)
