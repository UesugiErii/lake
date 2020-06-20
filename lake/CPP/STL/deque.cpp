#include <deque>
#include <iostream>

using namespace std;

// double-ended queue
// https://blog.csdn.net/longshengguoji/article/details/8519812

int main(){
	// init
	deque<int> dq ;
	deque<int>::iterator dqit;  // deque iterator
	
	// insert
	dq.push_back(2);  // 2
	dq.push_back(3);  // 2 3
	dq.push_front(1); // 1 2 3
	dq.push_front(0); // 0 1 2 3
	dq.insert(dq.begin()+1,9);  // 0 9 1 2 3
	
	// erase
	dq.erase(dq.begin()+3);  // 0 9 1 3
	
	// pop 
	dq.pop_back();  // 0 9 1
	dq.pop_front(); // 9 1
	
	
	// print
	for(dqit=dq.begin();dqit!=dq.end();dqit++){
		cout << *dqit;
	}
	cout << "\n";
	for(int i=0;i<dq.size();i++){
		cout << dq[i];
	}
	
	
	// empty()
	cout << dq.size();
	
}
