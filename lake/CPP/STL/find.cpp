#include <algorithm>
#include <vector>
#include <iostream> 

using namespace std;

int main(){
	vector<int> numbers {5, 46, -5, -6, 23, 17, 5, 9, 6, 5};
	int v = 23;
	auto iter = find(numbers.begin(),numbers.end(), v);
	if (iter != numbers.end()){
		cout << v << " was found. \n";
	}
    
    int count = 0;
    int five = 5;
	auto start_iter = std::begin(numbers);
	auto end_iter = std::end(numbers);
	while((start_iter = std::find(start_iter, end_iter, five)) != end_iter){
	++count;
	++start_iter;
	}
	std::cout << five << " was found " << count << " times." << std::endl; // 3 times
    
}
