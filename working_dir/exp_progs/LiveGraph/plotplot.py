import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

def animate(i):

    #graph_data = open('test_rssi.txt','r').read()
    graph_data = open('../RIM_PROGRAM1/output/70:18:8B:80:C9:E3','r').read()
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
    ax1.plot(xs, ys)
    
style.use('fivethirtyeight')

fig = plt.figure()

ax1 = fig.add_subplot(1,1,1)
ani= animation.FuncAnimation(fig, animate, interval=1000)


plt.show()
