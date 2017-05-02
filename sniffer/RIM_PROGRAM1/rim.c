#include <stdio.h>
#include <stdlib.h>
#include <pcap.h>
#include <time.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <termios.h>
#include <math.h>
#include "radiotap-parser.h" 
#include "ieee80211_radiotap.h"
#include "byteorder.h"

int a=0;
#define BAUDRATE B4800
//#define MODEMDEVICE "/dev/ttyUSB0"
#define MODEMDEVICE "/dev/tty.usbserial"

/* Frame */
struct wi_frame {
  u_int16_t fc;                 /* Frame control */
  u_int16_t wi_duration;        /* Duration/ID */
  u_int8_t wi_add1[6];          /* Destination MAC address */
  u_int8_t wi_add2[6];          /* Source MAC address */
  u_int8_t wi_add3[6];          /* BSSID */
  u_int16_t wi_sequenceControl; /* Sequence control */
  unsigned int qosControl:2;    
  unsigned int frame[23124];    /* payload */
};

char* print_packet_time(const u_char *packet, struct pcap_pkthdr packet_header){
  return ("\n    Time: %s \n",ctime((const time_t*)&packet_header.ts.tv_sec));
}

void init_file(void){
  FILE *pFile=NULL;
  pFile=fopen("output.txt","w");
  fclose(pFile);
  return;
}

int pnmea(char *buf,FILE *pFile) {
  
  double s1,s2;
  double m1,m2;
  double gps_lat,gps_lon;
  double lat;
  double lon;
  char ew;
  char ns;
  char stat; 
  char *p; 
  time_t timer;
  struct tm *date;
  char str[256];

  /*
    GPSレシーバから、GPRMC形式のデータを解析
    $GPRMC形式のデータフォーマットは以下
    
    $GPRMC,<1>,<2><3><4><5><6><7><8><9><10><11><12>*hh<CR><LF>

    <1> 測位時のUTC: hhmmss format
    <2> ステータス, A=整合性のある位置, V=NAV 受信警告
    <3> 緯度 ddmm.mmmmm format
    <4> 北半球、南半球 N or S
    <5> 経度 dddmm.mmmm format
    <6> 東半球、西半球 E or W
    <7> 対地速度 0.0.0~999.9 ノット
    <8> 対地進行方位
    <9> 測位時のUTC, day, ddmmyy format
    <10> 磁北偏差 000.0~180.0　度
    <11> 磁北偏移の方向, E or W
    <12> Mode indicator

    GPSから得られるデータは世界測地系としています。
    (OpenStreetMap)
  */

  if ((p=strtok(buf,","))==NULL)
    return 0;
  if (strcmp(p,"$GPRMC")!=0)
    return 0;
  if ((p=strtok(NULL,","))==NULL)
    return 0;
  if ((p=strtok(NULL,","))==NULL)
    return 0; 
  stat=p[0];
  if ((p=strtok(NULL,","))==NULL)
    return 0;
  sscanf(p,"%lf",&lat);
  if ((p=strtok(NULL,","))==NULL)
    return 0;
  ns=p[0];
  if ((p=strtok(NULL,","))==NULL)
    return 0;
  sscanf(p,"%lf",&lon);
  if ((p=strtok(NULL,","))==NULL)
    return 0;
  ew=p[0];
  
  if (stat!='A')
    return 0;
  
  /* GPSデータをDMS(度分秒)形式で表示する場合 */
  /*
  m1=(int)fmod(lat,100.0);
  m2=(int)fmod(lon,100.0);
  s1=lat-(int)lat;
  s1=s1*60;
  s2=lon-(int)lon;
  s2=s2*60;
  
  if (ns=='N'){
    fprintf(pFile,"N:%.0lf.%.0lf.%.3lf ",floor(lat/100.0), m1, s1);
    printf("N:%.0lf.%.0lf.%.3lf ",floor(lat/100.0), m1, s1);
  } else if (ns=='S'){
    fprintf(pFile,"S:%.0lf.%.0lf.%.3lf ",floor(lat/100.0), m1, s1);
    printf("S:%.0lf.%.0lf.%.3lf ",floor(lat/100.0), m1, s1);
  }
  
  if (ew=='E'){
    fprintf(pFile,"- E:%.0lf.%.0lf.%.3lf / ",floor(lon/100.0), m2, s2);
    printf("- E:%.0lf.%.0lf.%.3lf / ",floor(lon/100.0), m2, s2);
  } else if (ns=='W'){
    fprintf(pFile,"- W:%.0lf.%.0lf.%.3lf / ",floor(lon/100.0), m2, s2);
    printf("- W:%.0lf.%.0lf.%.3lf / ",floor(lon/100.0), m2, s2);
  }
  */

  /* GPSデータを１０進数形式で表示する場合(OpenStreetMap用) */
  
  m1=((int)fmod(lat,100.0))/60.0;
  m2=((int)fmod(lon,100.0))/60.0;
  s1=(60*(lat-(int)lat))/3600.0;
  s2=(60*(lon-(int)lon))/3600.0;
  
  gps_lat=(int)floor(lat/100.0)+m1+s1;
  gps_lon=(int)floor(lon/100.0)+m2+s2;

  if (ns=='N'){
    fprintf(pFile,"N:%lf ",gps_lat);
    printf("N:%lf ",gps_lat);
  } else if (ns=='S'){
    fprintf(pFile,"S:%lf ",gps_lat);
    printf("S:%lf ",gps_lat);
  }
  if (ew=='E'){
    fprintf(pFile,"- E:%lf / ",gps_lon);
    printf("- E:%lf / ",gps_lon);
  } else if (ns=='W'){
    fprintf(pFile,"- W:%lf ",gps_lon);
    printf("- W:%lf ",gps_lon);
  }
  return 1;

}

/* In this function, packet information (i.e., MAC address) would be extracted. */
void packet_process(u_char *cnt, const struct pcap_pkthdr* pkthdr, const u_char* packet)
{
  
  int k=6,next_arg_index=0,status;
  int *counter=(int *) cnt;
  int8_t rssi=0;
  struct ieee80211_radiotap_header *rh=(struct ieee80211_radiotap_header *)packet;
  struct wi_frame *fr=(struct wi_frame *)(packet+rh->it_len);
  struct ieee80211_radiotap_iterator iterator;
  u_char *ptr;
  FILE *pFile=NULL;
  
  int fd, c, res, flag=0;
  int i=0;
  int j=0;
  struct termios oldtio, newtio;
  unsigned char buf[512];
  
  // 出力ファイル
  pFile=fopen("output.txt","a");
  
  /* シリアル通信を行うための設定 */

  if((fd = open(MODEMDEVICE, O_RDWR | O_NOCTTY ))==-1){
    perror(MODEMDEVICE);
    exit(1);
  }
  
  tcgetattr(fd, &oldtio);
  bzero(&newtio, sizeof(newtio));
  newtio.c_cflag = (BAUDRATE | CRTSCTS | CS8 | CLOCAL | CREAD);
  newtio.c_iflag = (IGNPAR | ICRNL);
  newtio.c_oflag = 0;
  newtio.c_lflag = ICANON;
  tcflush(fd, TCIFLUSH);
  tcsetattr(fd,TCSANOW,&newtio);
  
  ptr=fr->wi_add2; // set src MAC address
  ++(*counter); // パケット数
  
  printf("[%03d] ",*counter);
  fprintf(pFile,"[%03d] ",*counter);

  while (1) {
    res = read(fd,buf,512);
    if(pnmea(buf,pFile)){
      break;
    }
  }

  printf("MAC address:");
  fprintf(pFile,"MAC address:");
  
  if(ieee80211_radiotap_iterator_init(&iterator,rh,pkthdr->len)){
    printf(" failed to Initialization ");
  }
  
  // Parse MAC address
  do{
    fprintf(pFile,"%s%02X",(k==6)?" ":":",*ptr);
    printf("%s%02X",(k==6)?" ":":",*ptr);
    ptr++;
  } while(--k>0);
  
  // Parse radiotap header until getting the RSSI
  do{
    next_arg_index=ieee80211_radiotap_iterator_next(&iterator);
    if(iterator.this_arg_index==IEEE80211_RADIOTAP_DBM_ANTSIGNAL){
      rssi=iterator.this_arg[0]; 
      status=1;
      break;
    }
  } while(next_arg_index>=0);
  
  printf(" / RSSI: %d",rssi);
  fprintf(pFile," / RSSI: %d",rssi);

  fprintf(pFile," / Time: %s",print_packet_time(packet,*pkthdr));
  printf(" / Time: %s",print_packet_time(packet,*pkthdr));
 
  a++; // to operate output file
  
  // close file and dev
  fclose(pFile);
  tcsetattr(fd, TCSANOW, &oldtio); 
  close(fd);

  return;
  
}

int main(int argc,char *argv[]){
  
  int count=0; /* packet counter */
  char *dev=argv[1]; /* set a device (an interface we sniff on) */
  char errbuf[PCAP_ERRBUF_SIZE]; /* Error string  */
  pcap_t *handle=pcap_create(dev,errbuf); /* Session handle  */
  
  struct bpf_program fp; /* The compiled filter expression */
  char filter_exp[]="wlan subtype probe-req"; /* The filter expression. Get probe- request */
  bpf_u_int32 mask; /* The netmask of our sniffing device */
  bpf_u_int32 net;  /* The IP of our sniffing device */
  
  struct pcap_pkthdr header;
  const u_char *packet;
  
  init_file(); // initialize the output file
  
  /* Get a device name we sniff on */
  /* Here, device name can be got from command line */
  printf("Specified device name: %s\n",dev);
  if (dev==NULL){
    printf("Please specify the device name.\n");
    exit(1);
  }
  
  /* find a netmask of the device */
  if ( pcap_lookupnet(dev,&net,&mask,errbuf) == 1 ){
    fprintf(stderr,"Can't get netmask for device %s\n",dev);
    net=0; 
    mask=0;
  } else {
    printf("Successfully get netmask of device. \n");
  }
  
  /* Create a sniff session */
  pcap_set_rfmon(handle,1);        /* turn on monitor mode */
  pcap_set_snaplen(handle,BUFSIZ); /* snapshot length */
  pcap_set_timeout(handle,10000);  /* Timeout in millisecond */
  pcap_activate(handle);           /* activate the session */
  
  /* open a device */
  if (handle == NULL){
    fprintf(stderr,"Couldn't open device %s: %s\n",dev,errbuf);
    exit(1);
  } else {
    printf("Successfully open device: %s\n",dev);
  }
  
  /* compile a filter */
  if (pcap_compile(handle,&fp,filter_exp,0,net)==-1){
    fprintf(stderr,"Couldn't parse filter %s: %s\n",filter_exp,pcap_geterr(handle));
    exit(2);
  } else {
    printf("Successfully compile.\n");
  }
  
  /* install a filter */
  if (pcap_setfilter(handle,&fp) == -1) {
    fprintf(stderr,"Couldn't install filter %s: %s\n",filter_exp,pcap_geterr(handle));
    exit(3);
  } else {
    printf("Successfully install filer.\n");
  }
  
  packet = pcap_next(handle,&header); // capture a packet 
  pcap_loop(handle,-1,packet_process,(u_char *)&count); // call back
  pcap_close(handle); // close a session
  
  return 0;
  
}
