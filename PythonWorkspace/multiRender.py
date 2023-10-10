import matplotlib.pyplot as plt
import random

fig, axs = plt.subplots(1, 2, figsize=(10, 5))

for i in range(50):
    axs[0].cla()
    axs[1].cla()
    values = [random.randint(0, 100), random.randint(0, 100)]
    axs[0].set_xlim(0, 1)
    axs[0].set_ylim(0, 100)
    axs[0].bar(list(range(2)), values)
    axs[1].set_xlim(0, 1)
    axs[1].set_ylim(0, 100)
    axs[1].bar(list(range(2)), values[::-1])
    plt.pause(0.01)

plt.show()