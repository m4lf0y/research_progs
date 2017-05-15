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

x = 1
y = 0
x1 = np.array([0,1,2,3,4,5,6])
y1 = np.array([0,1,2,3,4,5,6])

print(x1-x)

print(type(x))
print(type(x1[0]))
print(distance_between(x,y,x1,y1))
print(angle_between(x,y,x1,y1))

ax = plt.subplot(111,projection='polar')
c = ax.scatter(angle_between(x,y,x1,y1),distance_between(x,y,x1,y1),c='r')

plt.show()
