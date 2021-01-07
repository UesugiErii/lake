#include <iostream>
#include <string.h>
#include "murmur3.c"

using namespace std;

#define N 64
#define seed 0
#define k 1000

typedef struct node
{
    char data[1];
    struct node *next;
} Node;

int main() {

    Node *hashtable[k];

    FILE *fpr = NULL;
    char buff[N];
    fpr = fopen("/home/wanglei/course/dict.txt", "r");
    if (fpr == NULL) {
        cout << "fail to open dict.txt" << endl;
    }
    int string_len;
    uint32_t hash[4];
    int addr;
    while (fgets(buff, N, fpr) != NULL) {
        string_len = strlen(buff);
        if(buff[string_len-1] == '\n'){
            buff[string_len-1] = '\0';
            string_len -= 1;
        }
        MurmurHash3_x64_128(buff, string_len, seed, hash);
        addr = (hash[0] + hash[1] + hash[2] + hash[3]) % k;


    }

    fclose(fpr);

}
