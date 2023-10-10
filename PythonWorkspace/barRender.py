import matplotlib.pyplot as plt
import random



values = [0,0]

for i in range(50):
    plt.clf()
    values[1] = (random.randint(0, 100))
    values[0] = (random.randint(0, 100))
    plt.xlim(0,1)
    plt.ylim(0,100)
    plt.bar(list(range(2)), values)
    plt.pause(0.01)
plt.show()