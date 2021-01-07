#include <math.h>
#include <iostream>
#include <unistd.h>
#include <string.h>
#include "murmur3.c"

using namespace std;
#define N 256

int bf(double f, int n, char* save_path){
    // +0.5 用来实现正数的四舍五入
    int m = 0.5 + n / log(2) * log(1 / f) / log(2);  //需开辟的存储空间位数
    int k = 0.5 + log(2) * m / n;  // 哈希函数的个数
    // 0.693 <- math.log(2)
    // 1.44 <- 1/math.log(2)


    // init bits
    long long *bits;
    long long total_bits = (m / 64 + 1) * sizeof(long long);
    long long addr;
    bits = (long long *) malloc(total_bits);
    for (int i = 0; i < (m / 64 + 1); i++) {
        bits[i] = 0;
    }


    FILE *fpr = NULL;
    char buff[N];
    fpr = fopen("/home/wanglei/course/dict.txt", "r");
    if (fpr == NULL) {
        cout << "fail to open dict.txt" << endl;
    }

    uint32_t hash[4];                /* Output for the hash */
    uint32_t seed[k];                /* Seed value for hash */
    srand(1);                   // seed's seed
    for (int i = 0; i < k; i++) {
        seed[i] = rand();
    }

    long long mask;
    int string_len;
    // dont ues fscanf, since some lines may contain spaces
    while (fgets(buff, N, fpr) != NULL) {
        string_len = strlen(buff);
        if(buff[string_len-1] == '\n'){
            buff[string_len-1] = '\0';
            string_len -= 1;
        }
        for (int i = 0; i < k; i++) {
            MurmurHash3_x64_128(buff, string_len, seed[i], hash);
            addr = (hash[0] + hash[1] + hash[2] + hash[3]) % total_bits;
            mask = 1LL << (addr % 64);
            bits[addr / 64] |= mask;
        }
    }
    fclose(fpr);
    fpr = fopen("/home/wanglei/course/string.txt", "r");
//    FILE *fpw = fopen(save_path, "w+");
    if (fpr == NULL) {
        cout << "fail to open string.txt" << endl;
    }
//    if (fpw == NULL) {
//        cout << "fail to open res.txt" << endl;
//    }
    bool exist_flag;
    int count = 0;
    while (fgets(buff, N, fpr) != NULL) {
        exist_flag = true;
        string_len = strlen(buff);
        if(buff[string_len-1] == '\n'){
            buff[string_len-1] = '\0';
            string_len -= 1;
        }
        for (int i = 0; i < k; i++) {
            MurmurHash3_x64_128(buff, string_len, seed[i], hash);
            addr = (hash[0] + hash[1] + hash[2] + hash[3]) % total_bits;
            if (((bits[addr / 64] >> (addr % 64)) & 1) == 0) {
                exist_flag = false;
                break;
            }
        }
        if (exist_flag == false) {
            continue;
        }
//        fputs(buff, fpw);
//        fputc('\n', fpw);
        count++;
    }
    fclose(fpr);
//    fclose(fpw);


    free(bits);
    cout << "Error rate：" << f << "  " << "string_match:" << count << endl;
    return count;
}


int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(0);

    clock_t start_t;
    start_t = clock();

    // true ans    11489

    //  f  n  save_path
    int l = 1270000;
    int h = 15000000;
    int temp;
    int m;
    while(l<h){
        m = (h-l)/2+l;
        temp = bf(0.000001, m, "/home/wanglei/course/result/bupt_7_1.txt");
        if(temp>6306){
            l = m+1;
        }else{
            h = m;
        }
        cout << m << endl;
    }
    cout << h << endl;
//    bf(0.0001, 10226665, "/home/wanglei/course/result/bupt_7_1.txt");
//    bf(0.00001, 8113313, "/home/wanglei/course/result/bupt_7_2.txt");
//    bf(0.000001, 6980010, "/home/wanglei/course/result/bupt_7_3.txt");

//    sleep(3);
    cout << "runtime:" << "  "  << (double) (clock() - start_t) / (double) (CLOCKS_PER_SEC) << endl;
    return 0;

}