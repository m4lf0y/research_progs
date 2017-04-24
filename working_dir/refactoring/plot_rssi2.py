import numpy as np
import matplotlib.pyplot as pylab
import matplotlib.pyplot as plt
from scipy import optimize
from scipy import stats
from scipy.optimize import minimize
from scipy.optimize import least_squares
from scipy.stats import gaussian_kde,chi2,expon,gamma,erlang
import math
import random
from sympy import *
import pyproj
import pulp
from sympy import sympify

##########################################
#global variables##########################################

target_lat = 37.525171 #m_dev44.rim
target_lon = 139.938322
#target_lat = 37.52527 #m_dev2.rim
#target_lon = 139.939093
target_lat2 = 37.525308 #1_dev34.rim 1_dev16.rim(Ouchi)
target_lon2 = 139.937960
#target_lat = 37.525275 #1_dev33.rim
#target_lon = 139.937851
target_lat3 = 37.525382 #2_dev23.rim
target_lon3 = 139.937911
target_lat4 = 37.525295 #4_dev8.rim 5_dev15.rim
target_lon4 = 139.938999
#target_lat = 37.525355 #4_dev9.rim 5_dev16.rim
#target_lon = 139.938932
target_lat5 = 37.525304 #6_dev1.rim 7_dev1.rim
target_lon5 = 139.939094


target_lat_y = 0
target_lon_x = 0
xmin = 0
ymin = 0
Alpha = -45
Beta = 2
#devtext = 'device/m_dev44.rim'

rim_lat_y = np.array([])
rim_lon_x = np.array([])
rssi = np.array([])
distance = np.array([])
ave_rssi = np.array([])
max_rssi = np.array([])

##########################################
#Functions
##########################################

def devtext_to_list(devtext): #Text(dev00.rim) to np.array
    for line in open(devtext,"r"):
        if line[0]=="#":
            continue
        data = line.split()
        global rim_lat_y,rim_lon_x,rssi,distance
        x,y = gps_to_xy(float(data[1]),float(data[0]))
        rim_lat_y = np.append(rim_lat_y,y)
        rim_lon_x = np.append(rim_lon_x,x)
        rssi = np.append(rssi,float(data[2]))
        distance = np.append(distance,dis_two_points(x,y,target_lon_x,target_lat_y))

def devtext_to_list_max(): #Text(dev00.rim) to np.array (maximum velue of each square)
    global rim_lon_x,rim_lat_y,rssi
    temp_r = np.array([])
    for i in range(len(rssi)):
        rmax = -1000
        for j in range(len(rssi)):
            if rim_lon_x[i]==rim_lon_x[j] and rim_lat_y[i]==rim_lat_y[j]:
                if rmax < rssi[j]:
                    rmax = rssi[j]
        temp_r = np.append(temp_r,rmax)
    rssi = temp_r

def devtext_to_list_min(): #Text(dev00.rim) to np.array (minimum velue of each square)
    global rim_lon_x,rim_lat_y,rssi
    temp_r = np.array([])
    for i in range(len(rssi)):
        rmin = 1000
        for j in range(len(rssi)):
            if rim_lon_x[i]==rim_lon_x[j] and rim_lat_y[i]==rim_lat_y[j]:
                if rmin > rssi[j]:
                    rmin = rssi[j]
        temp_r = np.append(temp_r,rmin)
    rssi = temp_r

def devtext_to_list_med(): #Text(dev00.rim) to np.array (median velue of each square)
    global rim_lon_x,rim_lat_y,rssi
    temp_r = np.array([])
    for i in range(len(rssi)):
        temp_med = ([])
        for j in range(len(rssi)):
            if rim_lon_x[i]==rim_lon_x[j] and rim_lat_y[i]==rim_lat_y[j]:
                temp_med = np.append(temp_med,rssi[j])
        temp_r = np.append(temp_r,np.median(temp_med))
    rssi = temp_r

def gps_to_xy(lon,lat): #Convert the GPSs to xy
    EPSG4612 = pyproj.Proj("+init=EPSG:4612")  #http://sanvarie.hatenablog.com/entry/2016/01/04/170242
    EPSG2451 = pyproj.Proj("+init=EPSG:2451")  #Japan - zone-9 http://d.hatena.ne.jp/tmizu23/20091215/1260868350
    y,x = pyproj.transform(EPSG4612,EPSG2451,lon,lat)
    return x,y

def xy_to_1():      #Convert the minimum of x and y to 1
    global rim_lat_y,rim_lon_x,xmin,ymin
    xmin = np.min(rim_lon_x)-1
    ymin = np.min(rim_lat_y)-1
    rim_lat_y -= ymin
    rim_lon_x -= xmin

def target_to_xy(lon,lat):     #Convert the target of x and y to x-xmin and y-ymin
    global target_lon_x,target_lat_y
    target_lon_x,target_lat_y = gps_to_xy(lon,lat)

def est_ab(parameter,x,rssi):
    a = parameter[0]
    b = parameter[1]
    residual = rssi-(a-b*10*np.log10(x))
    return residual

def est_xyb(parameter,rssi,x,y):      #leastsq's function  Estimate target of x,y and Beta
    return rssi - func(parameter,x,y)

def est_xyab(parameter,rssi,x,y):   #leastsq's function Estimate target of x,y and Alpha,Beta
    return rssi - func2(parameter,x,y)

def est_xy(parameter,rssi,x,y):     #leastsq's function Estimate target of x,y
    return rssi - func3(parameter,x,y)

def func(parameter,x,y):
    return Alpha-parameter[2]*10*np.log10(np.sqrt((x-parameter[0])**2+(y-parameter[1])**2))

def func2(parameter,x,y):
    return parameter[2]-parameter[3]*10*np.log10(np.sqrt((x-parameter[0])**2+(y-parameter[1])**2))

def func3(parameter,x,y):
    return Alpha-Beta*10*np.log10(np.sqrt((x-parameter[0])**2+(y-parameter[1])**2))

def dis_two_points(x1,y1,x2,y2):       #Return the distance between the two points
    a = np.array([x1,y1])
    b = np.array([x2,y2])
    u = b -a
    if np.linalg.norm(u)==0:
        return 1
    else:
        return np.linalg.norm(u)

def plot(est_x,est_y): 
    area = np.pi * 1 **2
    plt.scatter(rim_lon_x,rim_lat_y,s=area,c='b',marker='^',label='Observation Point')
    area = np.pi * 3 ** 2
    plt.scatter(target_lon_x,target_lat_y,s=area,c='r',marker='s',alpha=0.5,label='Actual position')
    plt.scatter(est_x,est_y,s=300,c='b',alpha=0.5,label='Estimated position')
    
    plt.grid(True)
    plt.title('plot')
    plt.xlabel('x')
    plt.ylabel('y')
    
    plt.show()

def plot_rssi():
    global distance
    plt.scatter(distance,rssi,marker='x',label="Measured RSSI")
    plt.scatter(distance,ave_rssi,marker='o',label="Average")
    #plt.scatter(distance,max_rssi,marker='^',label="Max") 
    distance = np.unique(distance)
    y = Alpha-10*Beta*np.log10(distance)
    plt.plot(distance,y,label=r'$y=\alpha-10*\beta*np.log10(d)$')
    plt.grid(True)
    plt.xlabel("Distance [m]")
    plt.ylabel("RSSI [dBm]")
    plt.legend(loc='upper left')
    plt.show()

def convert_int():
    global rim_lon_x,rim_lat_y,distance
    rim_lon_x = rim_lon_x.astype(np.int64)
    rim_lat_y = rim_lat_y.astype(np.int64)
    distance = distance.astype(np.int64)

def ave():
    global rim_lon_x,rim_lat_y,rssi,ave_rssi
    temp_r = np.array([])
    for i in range(len(rssi)):
        rsum = 0
        num = 0
        for j in range(len(rssi)):
            if distance[i]==distance[j]:
                rsum += rssi[j]
                num += 1
        temp_r = np.append(temp_r,rsum/num)
    ave_rssi = temp_r

def rssmax():
    global rim_lon_x,rim_lat_y,rssi,max_rssi
    temp_r = np.array([])
    for i in range(len(rssi)):
        rmax = -1000
        for j in range(len(rssi)):
            if distance[i]==distance[j]:
                if rmax < rssi[j]:
                    rmax = rssi[j]
        temp_r = np.append(temp_r,rmax)
    max_rssi = temp_r

def dis_5():
    global distance
    distance = distance/5*5

def est_ab(parameter,x,rssi):
    a = parameter[0]
    b = parameter[1]
    residual = rssi-(a-b*10*np.log10(x))
    return residual


##########################################
#Main Function
##########################################
if __name__ == "__main__":

    #target_to_xy(target_lon,target_lat)
    #devtext_to_list('device/m_dev44.rim')
    #target_to_xy(target_lon2,target_lat2)
    #devtext_to_list('device/1_dev16.rim')
    #target_to_xy(target_lon2,target_lat2)
    #devtext_to_list('device/1_dev34.rim')
    #target_to_xy(target_lon3,target_lat3)
    #devtext_to_list('device/2_dev23.rim')
    #target_to_xy(target_lon4,target_lat4)
    #devtext_to_list('device/45_dev815.rim')
    target_to_xy(target_lon5,target_lat5)
    devtext_to_list('device/67_dev2.rim')

    #estimate the alpha and beta
    initialValue = np.array([-55,2])
    r1 = optimize.least_squares(est_ab,initialValue,bounds=([-60,1.5],[-35,4]),args=(distance,rssi))
    Alpha = r1.x[0]
    Beta = r1.x[1]
    print "Alpha : {0}\nBeta : {1}".format(Alpha,Beta)

    convert_int()
    dis_5()

    ave()
    rssmax()
    plot_rssi()
    print len(rssi)
