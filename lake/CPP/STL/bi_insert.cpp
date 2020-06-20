#include <cmath>
#include <algorithm>
#include <iostream>
#include <vector>
#include <iomanip>
#include <string>
#include <unordered_map>

using namespace std;


void f(vector<int>& v, int value){
	int low=0;
	int high=v.size()-1;
	int mid;
	while (low <= high){
		mid = (low+high)/2;
		if(v[mid] >= value){
			high = mid - 1;
		}else{
			low = mid + 1;
		}
	}
	
	if(v[mid] >= value){
		v.insert(v.begin()+mid,value);	
	}else{
		v.insert(v.begin()+mid+1,value);
	} 
}


int main(){
	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	
	vector<int> v {1,3,5,7,9,11};  // init
	vector<int>::iterator vit;  // v_iterator
	
	
	f(v,2);
	f(v,0);
	f(v,4);
	f(v,12);
	f(v,8);
	f(v,10);
	f(v,6);
	f(v,12);
	f(v,6);
	f(v,2);
	
	for(vit=v.begin();vit!=v.end();vit++){
		cout << *vit << " ";
	}
}

