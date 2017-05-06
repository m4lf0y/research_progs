import os
import time
import pyproj

def gps_to_xy(lon,lat): #Convert the GPSs to xy
    EPSG4612 = pyproj.Proj("+init=EPSG:4612")  #http://sanvarie.hatenablog.com/entry/2016/01/04/170242
    EPSG2451 = pyproj.Proj("+init=EPSG:2451")  #Japan - zone-9 http://d.hatena.ne.jp/tmizu23/20091215/1260868350
    y,x = pyproj.transform(EPSG4612,EPSG2451,lon,lat)
    return x,y

#fr = open('1_dev16.csv','r')
fr = open('45_dev916.csv','r')

# file open (write) latlon
if os.path.exists('test_latlon.txt'):
    os.remove('test_latlon.txt')
fw1 = open('test_latlon.txt','a',1)

# file open (write) rssi
if os.path.exists('test_rssi.txt'):
    os.remove('test_rssi.txt')
fw2 = open('test_rssi.txt','a',1)

i=0
for row in fr:
    i+=1

    time.sleep(0.1)

    l = row.strip().split(",")
    
    x,y = gps_to_xy(l[1],l[0])
    
    print(str(i)+','+l[2])
    print(str(x)+','+str(y))
    fw1.write(str(x)+','+str(y)+'\n')
    fw2.write(str(i)+','+l[2]+'\n')

fw1.close()
fw2.close()
fr.close()
