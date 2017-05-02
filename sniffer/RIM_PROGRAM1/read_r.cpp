#include <fstream>
#include <iostream>
#include <string>
#include <boost/regex.hpp>
#include <map>
#include <iterator>
#include <vector>
#include <algorithm>
#include <cerrno>
#include <stdlib.h>
#include <stdio.h>
int file_num=1;
using namespace std;

int main() {
  ifstream ifs("output.txt");  // 入力ファイルの読み込み
  string str, inputNumber;
  vector<string> mac;
  map<int,string> m_mac, m_time, m_rssi, m_gps;
  multimap<string,int> m_mac2;
  char* number;
  char number_buff[256]; //
  typedef map<int,string>::const_iterator itr;
  typedef multimap<string,int>::const_iterator itr2;
  int i = 0, j = 0, k = 0, m = 0, n=0;
  int value;
 
   /* Open file */
  if (ifs.fail()) //failbit(内部動作原因による入力ミス),badbit(ストリームバッファの入力操作失敗)のどちらかあるいは両方が1ならば、両方が0ならばfalse 
    {
      cerr << "Couldn't open" << endl;
      return -1;
    }
  
  /* all */
  // boost::regex pat ("^(.+?)([0-9A-F]{2}[:]){5}([0-9A-F]{2})(.+?)$"); 

  /* Mac Address */
  boost::regex mac_pattern ("([0-9A-Fa-f]{2}[:]){5}[0-9A-Fa-f]{2}");

  /* Time Stamp */
  boost::regex time_pattern ("([A-Za-z]{3}(\\s){1,2}){2}[0-9]{1,2}(\\s)([0-9]{2}[:]){2}[0-9]{2}(\\s)[0-9]{4}");

  /* RSSI */
  boost::regex rssi_pattern ("(\\s)(\\-)[0-9]{2}");

  /* GPS */
  // boost::regex gps_pattern("N:([0-9]{2,3}(.)){3}[0-9]{4}(\\s)(.)(\\s)E:([0-9]{2,3}(.)){3}[0-9]{4}");
  boost::regex gps_pattern("N:[0-9]{2}(.)[0-9]{6}(\\s)(.)(\\s)E:[0-9]{3}(.)[0-9]{6}");
  
  /* GPS Latitude */
  boost::regex gps_lat("[0-9]{2}(.)[0-9]{6}(\\s)");
  
  /* GPS Longitude*/
  boost::regex gps_lon("[0-9]{3}(.)[0-9]{6}");
  
  /* Output regex pattern*/
  cout << "MAC Address pattern: " << mac_pattern << endl
       << "Timestamp pattern: " << time_pattern << endl
       << "RSSI pattern: " << rssi_pattern << endl
       << "GPS pttern: " << gps_pattern << endl;
  
  /* Check strings */  
  while (getline(ifs, str)) { // reading each line
    boost::smatch matches; //retain matched strings
    if (boost::regex_search(str, matches, mac_pattern)) {
      mac.push_back(matches.str()); // a matched string is pushed
      m_mac.insert(make_pair(++i, matches.str())); // make_pair(key, value)
      m_mac2.insert(make_pair(matches.str(),i));
    }
    
    if (boost::regex_search(str, matches, time_pattern)) {
      m_time.insert(make_pair(++j, matches.str()));
    }

    if (boost::regex_search(str, matches, rssi_pattern)) {
      m_rssi.insert(make_pair(++k, matches.str()));
    }

    if (boost::regex_search(str, matches, gps_pattern)) {
      m_gps.insert(make_pair(++n, matches.str()));
    }
  } 
  
  /* sort mac address then erase duplication mac addrss */
  sort(mac.begin(),mac.end());
  mac.erase(unique(mac.begin(), mac.end()), mac.end());

  //// ここからMACアドレス毎に詳細を各ファイルに出力する
  vector<string>::iterator ti = mac.begin();
   while(ti != mac.end()){
     
     string dirname = ""; //書き込むディレクトリ先を指定
     string filename = "dev"+std::to_string(file_num)+ ".rim"; //書き込むファイルを指定
     ofstream writing_file;
     file_num++;
     writing_file.open(dirname+filename, ios::trunc); // 書き込むファイルをオープン
     writing_file << "#" << *ti << endl; //ファイル内先頭にMACアドレスを表示
     itr2 p = m_mac2.find(*ti);
     itr2 p2 = m_mac2.upper_bound(*ti);
     boost::smatch matches;
     
    /* Output files */
     while(p != m_mac2.end()){
       if(p2->second == p->second) break;
       if(p != m_mac2.end()) {
	 itr i_stamp = m_time.find(p->second);
	 itr i_rssi = m_rssi.find(p->second);
	 itr i_gps = m_gps.find(p->second);
	 if(boost::regex_search(i_gps->second,matches,gps_lat))
	   {
	     writing_file << matches.str();
	   }
	 if(boost::regex_search(i_gps->second,matches,gps_lon))
	   {
	     writing_file << matches.str();
	   }
	 writing_file  <<  i_rssi->second  << endl;
	 p++;
       }
     }
     *ti++;
   }

   return 0;
   
}
