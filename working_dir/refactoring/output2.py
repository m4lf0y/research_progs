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

error1 = []
error2 = []
numrssi = []

##########################################
#Functions
##########################################


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
    global rim_lon_x,rim_lat_y,rssi,sevhig,countN
    temp_r = np.array([])
    temp = []
    Numrss = []
    Error = []
    Numrss2 = []
    Error2 = []
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
    #print len(temp)
    countN = len(temp)
    rssi = temp_r
    rim_lon_x = temp_r
    rim_lat_y = temp_r
    #print "[m] : Error(Alpha=-49) : Error"

    for j in range(5,countN,5):
        rssi = temp_r
        rim_lon_x = temp_r
        rim_lat_y = temp_r
        for i in range(0,j):
            rssi = np.append(rssi,temp[i][0])
            rim_lon_x = np.append(rim_lon_x,temp[i][1])
            rim_lat_y = np.append(rim_lat_y,temp[i][2])

        InitialValue = np.array([1.,1.,-49,2.])
        r1 = optimize.least_squares(est_xyab,InitialValue,bounds=([-np.inf,-np.inf,-50,1.5],[np.inf,np.inf,-48,4]),args=(rssi,rim_lon_x,rim_lat_y))
        error2 = dis_two_points(target_lon_x,target_lat_y,r1.x[0],r1.x[1])
        
        Numrss2.append(len(rssi))
        Error2.append(error2)
        
        InitialValue = np.array([1.,1.,2.])
        r1 = optimize.least_squares(est_xyb,InitialValue,bounds=([-np.inf,-np.inf,1.5],[np.inf,np.inf,4]),args=(rssi,rim_lon_x.astype(np.int64),rim_lat_y.astype(np.int64)))
        error = dis_two_points(target_lon_x,target_lat_y,r1.x[0],r1.x[1])
        
        print "{0} {1} {2}".format(len(rssi),error,error2)
        Numrss.append(len(rssi))
        Error.append(error)
    plt.plot(Numrss,Error,marker='o',label="Alpha=-49")
    plt.plot(Numrss2,Error2,marker='^',label="Estimate A and B")
    plt.grid(True)
    plt.xlabel('Number of rssi')
    plt.ylabel('Error')
    plt.legend(loc='upper right')
    #plt.show()

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
    return np.linalg.norm(u)

def plot(est_x,est_y): 
    area = np.pi * 1 **2
    plt.scatter(rim_lon_x,rim_lat_y,s=area,c='b',marker='^',label='Observation Point')
    area = np.pi * 3 ** 2
    plt.scatter(target_lon_x,target_lat_y,s=area,c='r',marker='s',alpha=0.5,label='Actual position')
    plt.scatter(est_x,est_y,s=300,c='b',alpha=0.5,label='Estimated position')
    
    plt.grid(True)
    plt.title('plot')
    plt.xlabel('x[m]')
    plt.ylabel('y[m]')
    
    plt.show()

def convert_int():
    global rim_lon_x,rim_lat_y
    rim_lon_x = rim_lon_x.astype(np.int64)
    rim_lat_y = rim_lat_y.astype(np.int64)

##########################################
#Main Function
##########################################
if __name__ == "__main__":

    tmp0 = []
    tmp1 = []
    tmp2 = []
    for line in open("output2.txt","r"):
        data = line.split()
        tmp0.append(int(data[0]))
        tmp1.append(float(data[1]))
        tmp2.append(float(data[2]))

    for j in range(5,max(tmp0)+5,5):
        sum1 = 0
        sum2 = 0
        num1 = 0
        for i in range(len(tmp0)):
            if tmp0[i]==j:
                sum1+=tmp1[i]
                sum2+=tmp2[i]
                num1+=1
        numrssi.append(j)
        error1.append(sum1/num1)
        error2.append(sum2/num1)
        
    print numrssi

    plt.plot(numrssi,error1,marker='o',label="Alpha=-49")
    plt.plot(numrssi,error2,marker='^',label="Estimate A and B")
    plt.grid(True)
    plt.xlabel('Number of rssi')
    plt.ylabel('Error')
    plt.legend(loc='upper right')
    plt.show()

