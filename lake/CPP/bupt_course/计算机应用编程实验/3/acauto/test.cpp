#include <stdio.h>
#include <stdlib.h>
#include <iostream>

using namespace std;

void swap(int *arr, int i, int j) {
    arr[i] ^= arr[j] ^= arr[i] ^= arr[j];
}
// 主函数
int main() {
    int a[2] = {3,4};
    swap(a,0,1);
    cout << a[0] << a[1] << endl;

    return 0;
}