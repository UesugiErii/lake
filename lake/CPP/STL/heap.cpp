#include <vector>
#include <iostream>
#include <algorithm>

using namespace std;

int main(){

	vector<int>v {3,2,4};

	make_heap(v.begin(),v.end());  // {3,2,4} -> {4 2 3}  default is Max-heap
	// make_heap(v.begin(),v.end(),less<int>());  // Same as the previous line
	//make_heap(v.begin(),v.end(),greater<int>());  // {3,2,4} -> {2 3 4}  Min-heap
	
	// insert
	v.push_back(5);  // 4 2 3 5
	push_heap(v.begin(), v.end());  // 5 4 3 2
	
	// pop
	pop_heap(v.begin(),v.end());  // 4 2 3 5
	v.pop_back();  // 4 2 3
	
	
	for(int i=0;i<v.size();i++){
		cout << v[i] << " ";
	}


}

