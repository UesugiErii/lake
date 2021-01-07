#include <math.h>
#include <iostream>
#include <unistd.h>
#include "murmur3.c"

using namespace std;

#define N 256

int strlen(char *buff) {
    // diy strlen
    for (int string_len = 0; string_len < N; string_len++) {
        if (buff[string_len] == '\n') {
            buff[string_len] = '\0';
        }
        if (buff[string_len] == '\0') {
            return string_len;
        }
    }
}

void bf(const double &f,const int &n, char *save_path) {

    // +0.5 用来实现正数的四舍五入
    int m = 0.5 + n / log(2) * log(1 / f) / log(2);  //需开辟的存储空间位数
    int k = 0.5 + log(2) * m / n;  // 哈希函数的个数


    // init bits
    long long *bits;
    long long total_bits = (m / 64 + 1) * sizeof(long long);
    long long addr;
    bits = (long long *) malloc(total_bits);
    for (int i = 0; i < (m / 64 + 1); i++) {
        bits[i] = 0;
    }


    // init for murmur3
    uint32_t hash[4];                /* Output for the hash */
    uint32_t seed[k];                /* Seed value for hash */
    srand(1);                   // seed's seed
    for (int i = 0; i < k; i++) {
        seed[i] = rand();
    }


    char buff[N];

    // open dict file
    FILE *fp_dict = fopen("/home/wanglei/course/dict.txt", "r");
    if (fp_dict == NULL) cout << "fail to open dict.txt" << endl;

    // open string file
    FILE *fp_string = fopen("/home/wanglei/course/string.txt", "r");
    if (fp_string == NULL) cout << "fail to open string.txt" << endl;

    // open res file
    FILE *fp_res = fopen(save_path, "w+");
    if (fp_res == NULL) cout << "fail to open result.txt" << endl;


    long long mask;
    int string_len;
    // dont ues fscanf, since some lines may contain spaces
    while (fgets(buff, N, fp_dict) != NULL) {
        string_len = strlen(buff);
        for (int i = 0; i < k; i++) {
            MurmurHash3_x64_128(buff, string_len, seed[i], hash);
            addr = (hash[0] + hash[1] + hash[2] + hash[3]) % total_bits;
            mask = 1LL << (addr % 64);
            bits[addr / 64] |= mask;
        }
    }


    bool exist_flag;
    int count = 0;
    while (fgets(buff, N, fp_string) != NULL) {
        exist_flag = true;
        string_len = strlen(buff);
        for (int i = 0; i < k; i++) {
            MurmurHash3_x64_128(buff, string_len, seed[i], hash);
            addr = (hash[0] + hash[1] + hash[2] + hash[3]) % total_bits;
            if (((bits[addr / 64] >> (addr % 64)) & 1) == 0) {
                exist_flag = false;
                break;
            }
        }
        if (exist_flag) {
            fputs(buff, fp_res);
            fputc('\n', fp_res);
            count++;
        }
    }


    // close file
    fclose(fp_dict);
    fclose(fp_string);
    fclose(fp_res);

    free(bits);

    cout << "Error rate：" << f << "  " << "string_match:" << count << endl;
}


int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(0);

    clock_t start_t = clock();

    //  f  n  save_path
    bf(0.0001, 10278375, "/home/wanglei/course/result/bupt_7_1.txt");
    bf(0.00001, 8305883, "/home/wanglei/course/result/bupt_7_2.txt");
    bf(0.000001, 8242282, "/home/wanglei/course/result/bupt_7_3.txt");

    sleep(3);
    cout << "runtime:" << "  " << (double) (clock() - start_t) / (double) (CLOCKS_PER_SEC) << endl;
    return 0;

}