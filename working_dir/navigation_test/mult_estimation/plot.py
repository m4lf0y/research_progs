import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import localization
import math
import pyproj
import sys

argvs = sys.argv
macadr = argvs[1]

prex = 0
prey = 0

Estx = np.array([])
Esty = np.array([])

def gps_to_xy(lon,lat): #Convert the GPSs to xy
    EPSG4612 = pyproj.Proj("+init=EPSG:4612")  #http://sanvarie.hatenablog.com/entry/2016/01/04/170242
    EPSG2451 = pyproj.Proj("+init=EPSG:2451")  #Japan - zone-9 http://d.hatena.ne.jp/tmizu23/20091215/1260868350
    y,x = pyproj.transform(EPSG4612,EPSG2451,lon,lat)
    return x,y

acx, acy = gps_to_xy(139.939094,37.525295)#67_dev2


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

    global prex,prey
    global Estx,Esty

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

    est_x,est_y = localization.localization(allx,ally,allr)
    Estx = np.append(Estx,est_x)
    Esty = np.append(Esty,est_y)
    ax2.scatter(Estx, Esty, c = 'b', marker = 'o', alpha = 0.3, s = 100)
    if est_x and est_y:
        ax2.scatter(est_x,est_y,c = 'r', marker = 'o', alpha = 0.3, s = 100, label = 'estimated position')

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

    a = math.sqrt((u-prex)**2+(v-prey)**2)

    ax2.arrow(u,v,((u-prex)/a)*2,((v-prey)/a)*2,head_width=0.5,head_length=1,color='b')
    ax2.arrow(float(x),float(y),est_x-u,est_y-v,head_width=0.5,head_length=1,fc='k',ec='k')
    ax2.scatter(acx,acy,c = 'y',marker = '*',s = 200, label = 'actual position')

    ax2.set_xlim(30+1.692*10**5,75+1.692*10**5)
    ax2.set_ylim(9270,9370)
    ax2.legend()

style.use('fivethirtyeight')

fig = plt.figure()

ax2 = fig.add_subplot(1,1,1)
ani= animation.FuncAnimation(fig, animate_latlon, interval=1000)

plt.legend()
plt.show()
