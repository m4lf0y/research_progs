import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np

def distance_between(x1,y1,x2,y2):

    c = np.array([])

    for (x,y) in zip(x2,y2):
        a = np.array([x1,y1])
        b = np.array([x,y])
        c = np.append(c,np.linalg.norm(b-a))

    return c

def angle_between(x1,y1,x2,y2):
    c = np.array([])

    for (x,y) in zip(x2,y2):
        ang1 = np.arctan2(x1,y1)
        ang2 = np.arctan2(x,y)
        c = np.append(c,np.rad2deg((ang1-ang2)%(2*np.pi)))

    return c

def animate_latlon(i):

    graph_data2 = open('../test_data.txt','r').read()
    lines2 = graph_data2.split('\n')
    xs40 = np.array([])
    xs50 = np.array([])
    xs60 = np.array([])
    xs70 = np.array([])
    xs80 = np.array([])
    xs90 = np.array([])
    ys40 = np.array([])
    ys50 = np.array([])
    ys60 = np.array([])
    ys70 = np.array([])
    ys80 = np.array([])
    ys90 = np.array([])

    rs =[]

    for line in lines2:
        if len(line) > 1:
            x, y, rssi = line.split(',')
            if int(int(rssi)/10)==-4:
                xs40 = np.append(xs40,float(x))
                ys40 = np.append(ys40,float(y))
            elif int(int(rssi)/10)==-5:
                xs50 = np.append(xs50,float(x))
                ys50 = np.append(ys50,float(y))
            elif int(int(rssi)/10)==-6:
                xs60 = np.append(xs60,float(x))
                ys60 = np.append(ys60,float(y))
            elif int(int(rssi)/10)==-7:
                xs70 = np.append(xs70,float(x))
                ys70 = np.append(ys70,float(y))
            elif int(int(rssi)/10)==-8:
                xs80 = np.append(xs80,float(x))
                ys80 = np.append(ys80,float(y))
            elif int(int(rssi)/10)==-9:
                xs90 = np.append(xs90,float(x))
                ys90 = np.append(ys90,float(y))
            rs.append(rssi)
    ax2.clear()

#    print(xs80-float(x))

    print(distance_between(0,0,xs70-float(x),ys70-float(y)))

    ax2.scatter(angle_between(float(x),float(y),xs40,ys40), distance_between(0,0,xs40-float(x),ys40-float(y)), c = 'r', marker = 'o', alpha = 0.5, label = '-49 ~ -40')
    ax2.scatter(angle_between(float(x),float(y),xs50,ys50), distance_between(0,0,xs50-float(x),ys50-float(y)), c = 'g', marker = '^', alpha = 0.4, label = '-59 ~ -50')
    ax2.scatter(angle_between(float(x),float(y),xs60,ys60), distance_between(0,0,xs60-float(x),ys60-float(y)), c = 'c', marker = '^', alpha = 0.3, label = '-69 ~ -60')
    ax2.scatter(angle_between(float(x),float(y),xs70,ys70), distance_between(0,0,xs70-float(x),ys70-float(y)), c = 'm', marker = 's', alpha = 0.2, label = '-79 ~ -70')
    ax2.scatter(angle_between(float(x),float(y),xs80,ys80), distance_between(0,0,xs80-float(x),ys80-float(y)), c = 'y', marker = '.', alpha = 0.1, label = '-89 ~ -80')
    ax2.scatter(angle_between(float(x),float(y),xs90,ys90), distance_between(0,0,xs90-float(x),ys80-float(y)), c = 'y', marker = '.', alpha = 0.1, label = '-99 ~ -90')

#    ax2.scatter(x, y, c = 'k',s = 80,marker = '*', alpha = 1, label = 'current position')
#    ax2.set_ylim(-100,100)
#    ax2.set_xlim(-100,100)

    ax2.legend()
style.use('fivethirtyeight')

fig = plt.figure()

ax2 = fig.add_subplot(1,1,1,projection='polar')
ax2.set_ylim(100,100)
ax2.set_xlim(100,100)
ani= animation.FuncAnimation(fig, animate_latlon, interval=1000)

plt.legend()
plt.show()
