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
Alpha2 = 0
Alpha3 = 0
Alpha4 = 0
Beta = 0
Beta2 = 0
Beta3 = 0
Beta4 = 0
dis = np.array([])
dis2 = np.array([])
dis3 = np.array([])
dis4 = np.array([])
txt1 = "ideal/ideal1.txt"
#txt1 = "ideal/ideal1_2.txt"
txt2 = "ideal/ideal2.txt"
txt3 = "ideal/ideal3.txt"
txt4 = "ideal/ideal4.txt"
yplot = np.array([])

def text_to_list1(devtext):
    global Alpha,Beta,dis,yplot
    lineCount = 0
    for line in open(devtext,"r"):
        if lineCount == 0:
            Alpha = float(line)
        elif lineCount == 1:
            Beta = float(line)
        else:
            d = float(line)
            dis = np.append(dis,d)
            y = Alpha-10*Beta*np.log10(d)
            yplot = np.append(yplot,y)
        lineCount += 1


##########################################
#Main Function
##########################################
if __name__ == "__main__":

    text_to_list1(txt1)
    plt.plot(dis,yplot,marker='o',label="1")
    dis = np.array([])
    yplot = np.array([])

    text_to_list1(txt3)
    plt.plot(dis,yplot,marker='s',label="2")
    dis = np.array([])
    yplot = np.array([])
    
    text_to_list1(txt2)
    plt.plot(dis,yplot,marker='^',label="3")
    dis = np.array([])
    yplot = np.array([])
    
    text_to_list1(txt4)
    plt.plot(dis,yplot,label="4")
    dis = np.array([])
    yplot = np.array([])
    
    plt.grid(True)
    plt.xlabel("Distance [m]")
    plt.ylabel("RSSI [dBm]")
    plt.legend(loc='upper left')
    plt.show()

