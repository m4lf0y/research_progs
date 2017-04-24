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
from sympy import sympify
import matplotlib.animation as animation

##########################################
#global variables##########################################

#target_lat = 37.525171 #m_dev44.rim
#target_lon = 139.938322
#target_lat = 37.52527 #m_dev2.rim
#target_lon = 139.939093
target_lat = 37.525308 #1_dev34.rim 1_dev16.rim
target_lon = 139.937960
#target_lat = 37.525275 #1_dev33.rim
#target_lon = 139.937851
#target_lat = 37.525382 #2_dev23.rim
#target_lon = 139.937911
#target_lat = 37.525295 #4_dev8.rim 5_dev15.rim
#target_lon = 139.938999
target_lat = 37.525355 #4_dev9.rim 5_dev16.rim
target_lon = 139.938932
#target_lat = 37.525295 #67_dev2.rim
#target_lon = 139.939094
target_lat = 37.525310 #67_dev1.rim
target_lon = 139.939045
#target_lat = 37.525522 #8_dev2.rim
#target_lon = 139.939111
#target_lat = 23.525471 #8_dev1.rim
#target_lon = 139.939047
#target_lat = 37.525310 #116_devA4.rim 116_devB4.rim 116_devA4_2.rim 116_devB4_2.rim
#target_lon = 139.937839


target_lat_y = 0
target_lon_x = 0
xmin = 0
ymin = 0
Alpha = -49
Beta = 2 # at the time of estimate Alpha.
devtext = 'device/67_dev1.rim'
#devtext = 'device/test67.rim'
maxrssi = 0

rim_lat_y = np.array([])
rim_lon_x = np.array([])
rssi = np.array([])
rssimw = np.array([])
distance = np.array([])
#sevhig = np.array([])
sevhig = []

est100x = np.array([])
est100y = np.array([])
##########################################
#Functions
##########################################

def devtext_to_list(): #Text(dev00.rim) to np.array
    for line in open(devtext,"r"):
        if line[0]=="#":
            continue
        data = line.split()
        print(data[0])
        global rim_lat_y,rim_lon_x,rssi
        x,y = gps_to_xy(float(data[1]),float(data[0]))
        rim_lat_y = np.append(rim_lat_y,y)
        rim_lon_x = np.append(rim_lon_x,x)
        rssi = np.append(rssi,float(data[2]))

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

def devtext_to_list_ave(): #Text(dev00.rim) to np.array (average velue of each square)
    global rim_lon_x,rim_lat_y,rssi
    temp_r = np.array([])
    for i in range(len(rssi)):
        rsum = 0
        num = 0
        for j in range(len(rssi)):
            if rim_lon_x[i]==rim_lon_x[j] and rim_lat_y[i]==rim_lat_y[j]:
                rsum += rssi[j]
                num += 1
        temp_r = np.append(temp_r,rsum/num)
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

def devtext_to_list_sevhig():
    global rim_lon_x,rim_lat_y,rssi,sevhig
    temp_r = np.array([])
    temp = []
    for i in range(len(rssi)):
        rmax = -1000
        for j in range(len(rssi)):
            if rim_lon_x[i]==rim_lon_x[j] and rim_lat_y[i]==rim_lat_y[j]:
                if rmax < rssi[j]:
                    rmax = rssi[j]
        temp.append((rmax,rim_lon_x[i],rim_lat_y[i]))
    temp = list(set(temp))
    temp.sort()
    temp.reverse()
    rssi = temp_r
    rim_lon_x = temp_r
    rim_lat_y = temp_r
    print("input number")
    inputNum = input()
    for i in range(0,inputNum):
        rssi = np.append(rssi,temp[i][0])
        rim_lon_x = np.append(rim_lon_x,temp[i][1])
        rim_lat_y = np.append(rim_lat_y,temp[i][2])

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

def target_to_xy():     #Convert the target of x and y to x-xmin and y-ymin
    global target_lon_x,target_lat_y,rim_lon_x,rim_lat_y
    target_lon_x,target_lat_y = gps_to_xy(target_lon,target_lat)
    target_lon_x -= xmin
    target_lat_y -= ymin

def est_ab(parameter,x,rssi):
    a = parameter[0]
    b = parameter[1]
    residual = rssi-(a-b*10*np.log10(x))
    return residual

def est_xyb(parameter,rssi,x,y):      #leastsq's function  Estimate target of x,y and Beta
    return rssi - func(parameter,x,y)

def est_xyb2(parameter,rssi,x,y,rssimw):
    return (rssimw/maxrssi)*(rssi - func(parameter,x,y))

def est_xyab(parameter,rssi,x,y):   #leastsq's function Estimate target of x,y and Alpha,Beta
    return rssi - func2(parameter,x,y)

def est_xyab2(parameter,rssi,x,y,rssimw):
    return (rssimw/maxrssi)*(rssi - funcab2(parameter,x,y))

def est_xy(parameter,rssi,x,y):     #leastsq's function Estimate target of x,y
    return rssi - func3(parameter,x,y)

def funcab2(parameter,x,y):
    return parameter[3]-parameter[2]*10*np.log10(np.sqrt((x-parameter[0])**2+(y-parameter[1])**2))

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
    return np.linalg.norm(u)

def plot(est_x,est_y):
    U = 1
    V = 1

    area = np.pi * 1 **2
    #plt.scatter(rim_lon_x,rim_lat_y,s=area,c='b',marker='^',label='Observation Point')
    plt.quiver(rim_lon_x,rim_lat_y,U,V,angles='xy',scale_units='xy',scale=1)
    area = np.pi * 3 ** 2
    plt.scatter(target_lon_x,target_lat_y,s=300,c='r',marker='*',alpha=0.5,label='Actual position')
    plt.scatter(est_x,est_y,s=300,c='b',alpha=0.5,label='Estimated position')
    
    plt.grid(True)
    plt.xlabel('x[m]')
    plt.ylabel('y[m]')
    
    plt.show()

def plot_ani(est_x,est_y):
    fig = plt.figure()
    ims = []
    area = np.pi*3**2

    for i in range(rim_lon_x.size):
        im = plt.scatter(rim_lon_x[:i],rim_lat_y[:i],s=area,c='b',marker='^',label='ObservationPoint')
        ims.append(im)

    ani = animation.ArtistAnimation(fig,ims,interval=100)
    plt.show()

def plot100():
    plt.scatter(est100x,est100y,s=1,c='b',marker='^',label='Estimated position')
    plt.scatter(target_lon_x,target_lat_y,s=300,c='r',marker='*',alpha=0.5,label='Actual position')

    plt.grid(True)
    plt.xlabel('x[m]')
    plt.ylabel('y[m]')
    
    plt.show()

def convert_int():
    global rim_lon_x,rim_lat_y
    rim_lon_x = rim_lon_x.astype(np.int64)
    rim_lat_y = rim_lat_y.astype(np.int64)

def  dbm_to_mw(value):
    return math.pow(10, value/10)

##########################################
#Main Function
##########################################
if __name__ == "__main__":

    devtext_to_list()
    print(len(rssi))
    xy_to_1()
    convert_int()

    print("Enter a number\n[1:max 2:min 3:ave 4:med 5:sevhig other:no change]")
    inputNum = input()
    if int(inputNum)==1:
        devtext_to_list_max()
        print("Maximum value of each squares")
    elif int(inputNum)==2:
        devtext_to_list_min()
        print("Minimum value of each squares")
    elif int(inputNum)==3:
        devtext_to_list_ave()
        print("Average value of each squares")
    elif int(inputNum)==4:
        devtext_to_list_med()
        print("Median value of each squares")
    elif int(inputNum)==5:
        devtext_to_list_sevhig()
        print("Several heigher")
    else:
        print("No change")

    target_to_xy()
    for i in range(len(rssi)):
        distance = np.append(distance,dis_two_points(rim_lon_x[i],rim_lat_y[i],target_lon_x,target_lat_y))
#estimate the x and y
#    Alpha = -49
#    Beta = 2
#    initialValue = np.array([1.,1.])
#    r1 = optimize.least_squares(est_xy,initialValue,bounds=(-100,100),args=(rssi,rim_lon_x,rim_lat_y))
#    print "estimate x and y (Alpha = -45,Beta = 2)"
#    print "estimated Error : {0}\n".format(dis_two_points(target_lon_x,target_lat_y,r1.x[0],r1.x[1]))


#estimate the alpha and beta
#    initialValue = np.array([-55,2])
#    r1 = optimize.least_squares(est_ab,initialValue,bounds=([-60,1.5],[-35,4]),args=(distance,rssi))
#    Alpha = r1.x[0]
#    Beta = r1.x[1]

#Estimate x,y,Beta
    Alpha = -49
    InitialValue = np.array([1.,1.,2.])
    r1 = optimize.least_squares(est_xyb,InitialValue,bounds=([-np.inf,-np.inf,1.5],[np.inf,np.inf,4]),args=(rssi,rim_lon_x.astype(np.int64),rim_lat_y.astype(np.int64)))

#Test print
    print("     rssi :"+format(rssi))
    print("     Alpha :"+format(Alpha))
    print("     estimated Beta :"+format(r1.x[2]))
    print("     estimated Error :"+format(dis_two_points(target_lon_x,target_lat_y,r1.x[0],r1.x[1])))
#    plot(r1.x[0],r1.x[1])


#Estimate x,y,Beta
#    maxrssi = dbm_to_mw(np.max(rssi)); 
#    rssimw = np.power(10,rssi/10)
#    Alpha = -49
#    InitialValue = np.array([1.,1.,2.])
#    r1 = optimize.least_squares(est_xyb2,InitialValue,bounds=([-np.inf,-np.inf,2],[np.inf,np.inf,4]),args=(rssi,rim_lon_x.astype(np.int64),rim_lat_y.astype(np.int64),rssimw))

#Estimate x,y,Alpha,Beta
    maxrssi = dbm_to_mw(np.max(rssi)); 
    rssimw = np.power(10,rssi/10)
    InitialValue = np.array([1.,1.,2.,-49.])
    r1 = optimize.least_squares(est_xyab2,InitialValue,bounds=([-np.inf,-np.inf,2,-50],[np.inf,np.inf,4,-48]),args=(rssi,rim_lon_x.astype(np.int64),rim_lat_y.astype(np.int64),rssimw))
#    r1 = optimize.least_squares(est_xyab2,InitialValue,bounds=([-np.inf,-np.inf,-np.inf,-np.inf],[np.inf,np.inf,np.inf,np.inf]),args=(rssi,rim_lon_x.astype(np.int64),rim_lat_y.astype(np.int64),rssimw))
#Test print
    print("     rssi :"+format(rssi))
    print("     Alpha :"+format(Alpha))
    print("     estimated Alpha :"+format(r1.x[3]))
    print("     estimated Beta : "+format(r1.x[2]))
    print("     estimated Error : "+format(dis_two_points(target_lon_x,target_lat_y,r1.x[0],r1.x[1])))
    plot_ani(r1.x[0],r1.x[1])

# 100~複数推定
"""
    for i in range(len(rssi)):
        if i>99:
            #r1 = optimize.least_squares(est_xyab2,InitialValue,bounds=([-np.inf,-np.inf,2,-50],[np.inf,np.inf,4,-48]),args=(rssi[i-99:i],rim_lon_x[i-99:i].astype(np.int64),rim_lat_y[i-99:i].astype(np.int64),rssimw[i-99:i]))
            r1 = optimize.least_squares(est_xyab2,InitialValue,bounds=([-np.inf,-np.inf,2,-50],[np.inf,np.inf,4,-48]),args=(rssi[0:i],rim_lon_x[0:i].astype(np.int64),rim_lat_y[0:i].astype(np.int64),rssimw[0:i]))
        print("     estimated Error : "+format(dis_two_points(target_lon_x,target_lat_y,r1.x[0],r1.x[1])))
        est100x = np.append(est100x,r1.x[0])
        est100y = np.append(est100y,r1.x[1])

    plot100()
"""
