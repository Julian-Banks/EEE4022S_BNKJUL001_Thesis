import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import random

reg = LinearRegression()

x_values = []

y_values = []



for i in range(1000):
    plt.clf()
    x_values.append(random.randint(0, 100))
    y_values.append(random.randint(0, 100))
    
    x = np.array(x_values).reshape(-1, 1)
    y = np.array(y_values).reshape(-1, 1)

    

    if i % 10 == 0:
        reg.fit(x, y)
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        plt.scatter(x_values, y_values,color='red')
        plt.plot(list(range(0, 100)), reg.predict(np.array([x for x in range(100)]).reshape(-1, 1)), color='blue')
        plt.pause(0.001)

plt.show()

