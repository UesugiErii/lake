#include <map>
#include <iostream>
#include <vector>
#include <string>

using namespace std;

// map and dict in Python is very similar

int main(){
	
	// init
	map<string,int> m;
	map<string, int>::iterator mit;  // m iterator
	
	// insert
	m["test"] = 0;
	m["test2"] = 2;
	
	// find
	cout << "//find\n";
	mit = m.find("test1");
	if(mit == m.end()){
		cout << "test1 dont exit\n";
	}
	mit = m.find("test");
	if(mit != m.end()){
		cout << mit->first << "->" << mit->second << "\n";
	}
	
	// traversal
	cout << "//traversal\n";
	for(mit=m.begin();mit!=m.end();mit++){
		cout << mit->first << "->" << mit->second << "\n";
	}
	
	// erase
	m.erase("test");
	
	
}
