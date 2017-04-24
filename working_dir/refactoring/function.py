"""Docstring"""

import numpy as np

def devtext_to_list():
    '''Docstring
    Textfile(dev00.rim) to np.array
    '''
    for line in open(devtext,"r"):
        if line[0]=="#":
            continue
        data = line.split()
        global rim_lat_y,rim_lon_x,rssi
        x,y = gps_to_xy(float(data[1]),float(data[0]))
        rim_lat_y = np.append(rim_lat_y,y)
        rim_lon_x = np.append(rim_lon_x,x)
        rssi = np.append(rssi,float(data[2]))

def devtext_to_list_max():
    '''Docstring
    Textfile(dev00.rim) to np.array
    (maximum valeu of each square)
    '''
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
    '''Docstring
    Textfile(dev00.rim) to np.array
    (minimum value of each square)
    '''
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
    '''Docstring'''
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
    '''Docstring'''
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
    '''Docstring'''
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
    '''Docstring'''
    EPSG4612 = pyproj.Proj("+init=EPSG:4612")  #http://sanvarie.hatenablog.com/entry/2016/01/04/170242
    EPSG2451 = pyproj.Proj("+init=EPSG:2451")  #Japan - zone-9 http://d.hatena.ne.jp/tmizu23/20091215/1260868350
    y,x = pyproj.transform(EPSG4612,EPSG2451,lon,lat)
    return x,y

def xy_to_1():      #Convert the minimum of x and y to 1
    '''Docstring'''
    global rim_lat_y,rim_lon_x,xmin,ymin
    xmin = np.min(rim_lon_x)-1
    ymin = np.min(rim_lat_y)-1
    rim_lat_y -= ymin
    rim_lon_x -= xmin

def target_to_xy():     #Convert the target of x and y to x-xmin and y-ymin
    '''Docstring'''
    global target_lon_x,target_lat_y,rim_lon_x,rim_lat_y
    target_lon_x,target_lat_y = gps_to_xy(target_lon,target_lat)
    target_lon_x -= xmin
    target_lat_y -= ymin

def est_ab(parameter,x,rssi):
    '''Docstring'''
    a = parameter[0]
    b = parameter[1]
    residual = rssi-(a-b*10*np.log10(x))
    return residual

def est_xyb(parameter,rssi,x,y):      #leastsq's function  Estimate target of x,y and Beta
    '''Docstring'''
    return rssi - func(parameter,x,y)

def est_xyb2(parameter,rssi,x,y,rssimw):
    '''Docstring'''
    return (rssimw/maxrssi)*(rssi - func(parameter,x,y))

def est_xyab(parameter,rssi,x,y):   #leastsq's function Estimate target of x,y and Alpha,Beta
    '''Docstring'''
    return rssi - func2(parameter,x,y)

def est_xyab2(parameter,rssi,x,y,rssimw):
    '''Docstring'''
    return (rssimw/maxrssi)*(rssi - funcab2(parameter,x,y))

def est_xy(parameter,rssi,x,y):     #leastsq's function Estimate target of x,y
    '''Docstring'''
    return rssi - func3(parameter,x,y)

def funcab2(parameter,x,y):
    '''Docstring'''
    return parameter[3]-parameter[2]*10*np.log10(np.sqrt((x-parameter[0])**2+(y-parameter[1])**2))

def func(parameter,x,y):
    '''Docstring'''
    return Alpha-parameter[2]*10*np.log10(np.sqrt((x-parameter[0])**2+(y-parameter[1])**2))

def func2(parameter,x,y):
    '''Docstring'''
    return parameter[2]-parameter[3]*10*np.log10(np.sqrt((x-parameter[0])**2+(y-parameter[1])**2))

def func3(parameter,x,y):
    '''Docstring'''
    return Alpha-Beta*10*np.log10(np.sqrt((x-parameter[0])**2+(y-parameter[1])**2))

def dis_two_points(x1,y1,x2,y2):       #Return the distance between the two points
    '''Docstring'''
    a = np.array([x1,y1])
    b = np.array([x2,y2])
    u = b -a
    return np.linalg.norm(u)

def plot(est_x,est_y): 
    '''Docstring'''
    area = np.pi * 1 **2
    plt.scatter(rim_lon_x,rim_lat_y,s=area,c='b',marker='^',label='Observation Point')
    area = np.pi * 3 ** 2
    plt.scatter(target_lon_x,target_lat_y,s=300,c='r',marker='*',alpha=0.5,label='Actual position')
    plt.scatter(est_x,est_y,s=300,c='b',alpha=0.5,label='Estimated position')
    
    plt.grid(True)
    plt.xlabel('x[m]')
    plt.ylabel('y[m]')
    
    plt.show()

def plot100():
    '''Docstring'''
    plt.scatter(est100x,est100y,s=1,c='b',marker='^',label='Estimated position')
    plt.scatter(target_lon_x,target_lat_y,s=300,c='r',marker='*',alpha=0.5,label='Actual position')

    plt.grid(True)
    plt.xlabel('x[m]')
    plt.ylabel('y[m]')
    
    plt.show()

def convert_int():
    '''Docstring'''
    global rim_lon_x,rim_lat_y
    rim_lon_x = rim_lon_x.astype(np.int64)
    rim_lat_y = rim_lat_y.astype(np.int64)

def  dbm_to_mw(value):
    '''Docstring'''
    return math.pow(10, value/10)
