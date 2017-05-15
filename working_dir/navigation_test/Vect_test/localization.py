import numpy as np
from scipy import optimize
from scipy.optimize import least_squares
import math

maxrssi = 0

def localization(x,y,rssi):
    
    try:
        global maxrssi
        maxrssi = dbm_to_mw(np.max(rssi))
        rssimw = np.power(10,rssi/10)
        InitialValue = np.array([1.,1.,2.,-49.])
        r1 = optimize.least_squares(estimation,InitialValue,bounds=([-np.inf,-np.inf,1.5,-50],[np.inf,np.inf,4.,-48.]),args = (rssi, x.astype(np.int64), y.astype(np.int64), rssimw))
    except:
        return None,None

    return r1.x[0],r1.x[1]

def estimation(parameter, rssi, x, y, rssimw):
    try:
        return (rssimw/maxrssi)*(rssi-func(parameter,x,y))
    except:
        return None

def func(parameter, x, y):
    try:
        return parameter[3]-parameter[2]*10*np.log10(np.sqrt((x-parameter[0])**2+(y-parameter[1])**2))
    except:
        return None
def  dbm_to_mw(value):
    return math.pow(10, value/10)

if __name__ == "__main__":
    x = np.array([1,2,3,4,5,6,7,8,9])
    y = np.array([3,4,6,2,4,6,7,5,7])
    r = np.array([-50,-40,-43,-77,-54,-76,-76,-33,-67])

    print(localization(x,y,r))
