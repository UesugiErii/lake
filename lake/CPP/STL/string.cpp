#include <map>
#include <iostream>
#include <string>
 
using namespace std;

int main(){
	string s;  // init
	s = "0123456789";
	string s_copy = s;
	
	// substring
	string s1 = s.substr(2,3);  // start, length  234
	
	// insert
	s.insert(1,"11");  // start, string  011123456789
	
	// erase 
	s.erase(4,2);  // start, length  0111456789
	
	// append
	s += "99";  // 011145678999
	s += '9';  // 0111456789999
	
	// replace
	s.replace(1,3,"89");  // start, length, string  089456789999
	
	// find   no return -1
	int index1 = s.find("89");  // 1
	int index2 = s.rfind("89");  // 7
	
	// compare
	cout << (s_copy < s);  // 1
}
