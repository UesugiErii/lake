#include <vector>
#include <iostream>

using namespace std;

// vector is variable capacity array

// vector can also be used as a stack 

// push_back()       <->       push()
// pop_back()        <->       pop()
// size()            <->       size()
// *(v.end()-1)      <->       top()              before use, make sure that size() != 0


int main(){
	vector<int> v;  // init
	vector<int>::iterator vit;  // v_iterator
	
	// insert
	v.push_back(1);  // 1
	v.push_back(3);  // 1 3
	vit = v.begin();
	vit ++;
	v.insert(vit,2);  // 1 2 3
	
	// size
	v.size();  // 3
	
	// pop
	v.pop_back();  // 1 2
	
	// back
	v.back();  // 2       return last

	// print
	for(vit=v.begin();vit!=v.end();vit++){
		cout << *vit;
	}
	cout << "\n";
	for(int i=0;i<v.size();i++){
		cout << v[i];
	}
	
	// erase
	v.erase(v.begin()+1);  // del 2
	
	
	cout << "\n";
	cout << *(v.end()-1);  // print last
}
