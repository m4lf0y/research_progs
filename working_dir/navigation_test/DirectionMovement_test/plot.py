import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import localization
import math

curx = 0
cury = 0
prex = 0
prey = 0

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

    global curx,cury,prex,prey

    graph_data2 = open('../test_data.txt','r').read()
    lines2 = graph_data2.split('\n')
    allx = np.array([])
    ally = np.array([])
    allr = np.array([])
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

    maxr = -100
    maxx = 0
    maxy = 0

    '''
    current position = allx[-1],ally[-1]
    '''

    for i,line in enumerate(lines2):
        if len(line) > 1:
            x, y, rssi = line.split(',')
            allx = np.append(allx,int(float(x)))
            ally = np.append(ally,int(float(y)))
            allr = np.append(allr,int(rssi))

            if maxr <= int(rssi):
                maxr = int(rssi)
                maxx = int(float(x))
                maxy = int(float(y))

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

    ax2.scatter(xs40,ys40, c = 'r', marker = 'o', alpha = 0.5, label = '-49 ~ -40')
    ax2.scatter(xs50,ys50, c = 'g', marker = '^', alpha = 0.4, label = '-59 ~ -50')
    ax2.scatter(xs60,ys60, c = 'c', marker = '^', alpha = 0.3, label = '-69 ~ -60')
    ax2.scatter(xs70,ys70, c = 'm', marker = 's', alpha = 0.2, label = '-79 ~ -70')
    ax2.scatter(xs80,ys80, c = 'y', marker = '.', alpha = 0.1, label = '-89 ~ -80')
    ax2.scatter(xs90,ys90, c = 'y', marker = '.', alpha = 0.1, label = '-99 ~ -90')

#    if est_x and est_y:
#        ax2.scatter(est_x,est_y,c = 'b', marker = 'o', alpha = 0.5, s = 100, label = 'estimated position')

    u = float(x)
    v = float(y)
    if allx[-1]==allx[-2] and ally[-1]==ally[-2]:
        i = -3
        while(True):
            prex = allx[i]
            prey = ally[i]
            i = i - 1
            if prex != allx[-1] or prey != ally[-1]:
                break
    '''
    if float(x)!=curx or float(y)!=cury:
        prex = curx
        prey = cury

    u = curx-prex
    v = cury-prey

#    a = math.sqrt(u**2+v**2)
#    ax2.quiver(float(x),float(y),(u/a),(v/a),angles='xy',scale_units='xy',scale=1)
    a = math.sqrt(u**2+v**2)
    '''

    ax2.arrow(prex,prey,u-prex,v-prey,head_width=1,head_length=1,fc='k',ec='k')


    ax2.legend()
style.use('fivethirtyeight')

fig = plt.figure()

ax2 = fig.add_subplot(1,1,1)
ani= animation.FuncAnimation(fig, animate_latlon, interval=1000)

plt.legend()
plt.show()
