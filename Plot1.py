import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig, ax = plt.subplots()

x = np.arange(53)
y = [0.175824, 0.175824, 0.703297, 0.205128, 0.644689, 0.761905, 0.205128, 0.791209, 0.14652, 0.761905, 118.065941, 117.538467, 117.831505, 117.948723, 117.978027, 117.655685, 117.948723, 117.626381, 117.948723, 117.655685, 0.205128, 0.14652, 0.205128, 0.175824, 0.14652, 0.14652, 0.117216, 0.205128, 0.644689, 0.175824, 0.703297, 117.626381, 117.948723, 117.890121, 117.948723, 117.538467, 117.538467, 117.948723, 117.948723, 117.948723, 0.117216, 0.205128, 0.14652, 0.087912, 0.175824, 0.117216, 0.205128, 0.14652, 0.087912, 0.205128, 0.644689, 117.978027, 118.007339]
line, = ax.plot(x, y)


def init():  # only required for blitting to give a clean slate.
    line.set_ydata([np.nan] * len(x))
    return line,


def animate(i):
    time.sleep(0.1)
    aux = y[0]
    y.remove(aux)
    y.append(aux)
    line.set_ydata(y)  # update the data.
    return line,


ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=2, blit=True, save_count=50)

# To save the animation, use e.g.
#
# ani.save("movie.mp4")
#
# or
#
# from matplotlib.animation import FFMpegWriter
# writer = FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("movie.mp4", writer=writer)

plt.show()
