import os
import time
import pyproj

def gps_to_xy(lon,lat): #Convert the GPSs to xy
    EPSG4612 = pyproj.Proj("+init=EPSG:4612")  #http://sanvarie.hatenablog.com/entry/2016/01/04/170242
    EPSG2451 = pyproj.Proj("+init=EPSG:2451")  #Japan - zone-9 http://d.hatena.ne.jp/tmizu23/20091215/1260868350
    y,x = pyproj.transform(EPSG4612,EPSG2451,lon,lat)
    return x,y

fr = open('../device/67_dev2_r.rim','r')

# file open (write)
if os.path.exists('../test_data.txt'):
    os.remove('../test_data.txt')
fw = open('../test_data.txt','a',1)

i=0
for row in fr:
    if row[0]=='#':
        continue
    i+=1

    time.sleep(0.1)

    l = row.strip().split(" ")
    
    x,y = gps_to_xy(l[1],l[0])
    
    print(str(i)+','+l[2])
    print(str(x)+','+str(y))
    fw.write(str(x)+','+str(y)+','+l[2]+'\n')

fw.close()
fr.close()
