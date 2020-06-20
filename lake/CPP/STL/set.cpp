#include <iostream>
#include <set>

using namespace std;

int main(){
	set<int> s;
	set<int>::iterator sit;
    
    // insert
	s.insert(2);  // 2
	s.insert(1);  // 1 2
	s.insert(3);  // 1 2 3
	
	// print all
	for(sit=s.begin();sit!=s.end();sit++){
		cout << *sit;  // 1 2 3     default is increasing
	}
	
	// erase
	s.erase(3);  // 1 2
	
	//clear() delete all
	
	// find
	cout << "\n";
	if(s.find(5)!=s.end())
        cout<<"FOUND"<<"\n";
    else
        cout<<"NOT FOUND"<<"\n";
	
	
	// count
	cout << s.count(1) << endl; 
	cout << s.count(5) << endl;
	
} 
