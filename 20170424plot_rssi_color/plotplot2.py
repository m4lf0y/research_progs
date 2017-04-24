import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


def animate_latlon(i):

    graph_data2 = open('test_data.txt','r').read()
    lines2 = graph_data2.split('\n')
    xs40 = []
    xs50 = []
    xs60 = []
    xs70 = []
    xs80 = []
    xs90 = []
    ys40 = []
    ys50 = []
    ys60 = []
    ys70 = []
    ys80 = []
    ys90 = []

    rs = []
    for line in lines2:
        if len(line) > 1:
            x, y, rssi = line.split(',')
            if int(int(rssi)/10)==-4:
                xs40.append(x)
                ys40.append(y)
            elif int(int(rssi)/10)==-5:
                xs50.append(x)
                ys50.append(y)
            elif int(int(rssi)/10)==-6:
                xs60.append(x)
                ys60.append(y)
            elif int(int(rssi)/10)==-7:
                xs70.append(x)
                ys70.append(y)
            elif int(int(rssi)/10)==-8:
                xs80.append(x)
                ys80.append(y)
            elif int(int(rssi)/10)==-9:
                xs90.append(x)
                ys90.append(y)
            rs.append(rssi)
    ax2.clear()

    ax2.plot(xs40, ys40, c = 'r', marker = 'o', alpha = 0.5, label = '-49 ~ -40')
    ax2.plot(xs50, ys50, c = 'g', marker = '^', alpha = 0.4, label = '-59 ~ -50')
    ax2.plot(xs60, ys60, c = 'c', marker = '^', alpha = 0.3, label = '-69 ~ -60')
    ax2.plot(xs70, ys70, c = 'm', marker = 's', alpha = 0.2, label = '-79 ~ -70')
    ax2.plot(xs80, ys80, c = 'y', marker = '.', alpha = 0.1, label = '-89 ~ -80')
    ax2.legend()
#    ax2.scatter(xs40, ys40, c = 'r', marker = 'o', alpha = 0.5, label = '-49 ~ -40')
#    ax2.scatter(xs50, ys50, c = rs, marker = '^', alpha = 0.5, label = '-59 ~ -50')
#    ax2.scatter(xs60, ys60, c = rs, marker = '^', alpha = 0.5, label = '-69 ~ -60')
#    ax2.scatter(xs70, ys70, c = rs, marker = 's', alpha = 0.5, label = '-79 ~ -70')
#    ax2.scatter(xs80, ys80, c = rs, marker = '.', alpha = 0.5, label = '-89 ~ -80')

style.use('fivethirtyeight')

fig = plt.figure()

ax2 = fig.add_subplot(1,1,1)
ani= animation.FuncAnimation(fig, animate_latlon, interval=1000)

plt.legend()
plt.show()
