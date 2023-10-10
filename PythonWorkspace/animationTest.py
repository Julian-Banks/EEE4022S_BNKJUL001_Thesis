import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

fig, ax = plt.subplots()

def animate(i):
    values = [random.randint(0, 100), random.randint(0, 100)]
    ax.clear()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 100)
    ax.bar(list(range(2)), values)

ani = animation.FuncAnimation(fig, animate, frames=50, interval=10, blit=False)

plt.show()