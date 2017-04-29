OBJS = radiotap-parser.o rim.o
CC = gcc
CFLAGS = -O -g

rim : $(OBJS)
	$(CC) $(OBJS) -o rim -lpcap -lm -lsqlite3 -L/usr/lib64/ -I/usr/include/
radiotap-parser.o : radiotap-parser.c radiotap-parser.h byteorder.h ieee80211_radiotap.h
	$(CC) $(CFLAGS) -c radiotap-parser.c -o radiotap-parser.o
rim.o : rim.c radiotap-parser.h
	$(CC) $(CFLAGS) -c rim.c -o rim.o -lpcap -lm
clean:
	rm -rf *.o rim
