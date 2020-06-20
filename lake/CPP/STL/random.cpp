#include <iostream>
#include <algorithm>


#include <stdlib.h> 
#include <time.h>

using namespace std;

int main(){
	// min 0
	cout << RAND_MAX << "\n";  // 32767   2**15-1
	
	srand((unsigned)time(NULL));  // seed
	for (size_t i = 0; i < 10; i++) {
	    cout << rand() << "\n";
	}
	
}


// http://notes.maxwi.com/2016/04/10/cpp-random/
