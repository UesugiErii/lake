#include <vector>
#include <iostream>
#include <algorithm>
#include <string>

using namespace std;

struct people{
	int age;
	string name;
};

bool Less(const people& s1, const people& s2)
{
	return s1.age < s2.age;  // Sort age from small to large
}

int main(){
	
	// easy example
	vector<int>v {3,2,4};
	
	sort(v.begin(),v.end(),less<int>());  // 2 3 4   default
	sort(v.begin(),v.end(),greater<int>());  // 4 3 2
	
	for(int i=0;i<v.size();i++){
		cout << v[i] << " ";
	}
	
	
	// custom comparison function
	
	struct people p1,p2;
	p1.name = "p1";
	p1.age = 20;
	p2.name = "p2";
	p2.age = 10;
	
	vector<struct people>p {p1,p2};

	sort(p.begin(),p.end(),Less);  // {p2,10} {p1,20}
	
	cout << "\n";
	cout << p[0].name << " " << p[0].age << "\n";
	cout << p[1].name << " " << p[1].age << "\n";
}
