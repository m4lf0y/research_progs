import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

def animate_latlon(i):

    graph_data2 = open('test_latlon.txt','r').read()
    lines2 = graph_data2.split('\n')
    xs2 = []
    ys2 = []
    for line in lines2:
        if len(line) > 1:
            x, y = line.split(',')
            xs2.append(x)
            ys2.append(y)
    ax2.clear()
    ax2.scatter(xs2, ys2)
    
style.use('fivethirtyeight')

fig = plt.figure()

ax2 = fig.add_subplot(1,1,1)
ani= animation.FuncAnimation(fig, animate_latlon, interval=1000)


plt.show()
