import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

def animate(i):

    graph_data = open('../test_data.txt','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    i = 0
    for line in lines:
        if len(line) > 1:
            i += 1
            la,lo,rssi = line.split(',')
            xs.append(i)
            ys.append(rssi)
    ax1.clear()
    ax1.plot(xs, ys, lw=1)
    
style.use('fivethirtyeight')

fig = plt.figure()

ax1 = fig.add_subplot(1,1,1)
ani= animation.FuncAnimation(fig, animate, interval=1000)


plt.show()
