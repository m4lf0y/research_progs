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

Alpha = 0
Beta = 0
dis = np.array([])
#txt1 = "ave1.txt"
txt1 = "ave/ave14.txt"
txt2 = "ave/ave2.txt"
txt3 = "ave/ave3.txt"
txt4 = "ave/ave4.txt"
rssi = np.array([])

def text_to_list1(devtext):
    for line in open(devtext,"r"):
        data = line.split()
        global dis,rssi
        d = float(data[0])
        r = float(data[1])
        dis = np.append(dis,d)
        rssi = np.append(rssi,r)


##########################################
#Main Function
##########################################
if __name__ == "__main__":

    text_to_list1(txt1)
    plt.plot(dis,rssi,marker='o',label="1")
    #plt.scatter(dis,rssi,marker='o',label="1")
    dis = np.array([])
    rssi = np.array([])
    '''
    text_to_list1(txt3)
    plt.plot(dis,rssi,marker='s',label="2")
    #plt.scatter(dis,rssi,marker='s',label="2")
    dis = np.array([])
    rssi = np.array([])
    
    text_to_list1(txt2)
    plt.plot(dis,rssi,marker='^',label="3")
    #plt.scatter(dis,rssi,marker='^',label="3")
    dis = np.array([])
    rssi = np.array([])
    
    text_to_list1(txt4)
    plt.plot(dis,rssi,label="4")
    #plt.scatter(dis,rssi,label="4")
    dis = np.array([])
    rssi = np.array([])
    '''
    plt.grid(True)
    plt.xlabel("Distance [m]")
    plt.ylabel("RSSI [dBm]")
    plt.legend(loc='upper left')
    plt.show()

