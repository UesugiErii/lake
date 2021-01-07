#include <iostream>

using namespace std;

typedef struct node {
    struct node *next[2];
    int valid_bits;
    bool end;
    char data[1];
} Node;

int main(void) {

    Node * root;
	cout << &*root << endl;
    cout << &root->valid_bits << endl;
    cout << &root->data << endl;

    return 0;
}