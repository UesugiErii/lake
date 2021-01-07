#include <iostream>
#include <unistd.h>

using namespace std;

#define M 7   // M should less than or equal to 256
#define N 64  // max string length

typedef struct node {
    struct node *next[M];
    bool end;
} Node;

Node *get_node() {
    // dynamic get one inited node
    Node *root;
    root = (Node *) malloc(sizeof(Node));
    for (int i = 0; i < M; i++) {
        root->next[i] = nullptr;
    }
    root->end = false;
    return root;
}

void strip(char *buff) {
    // delete \n
    for (int i = 0; i < N; i++) {
        if (buff[i] == '\n') {
            buff[i] = '\0';
        }
        if (buff[i] == '\0') {
            return;
        }
    }
}

void dfs_free(Node *root) {
    // dfs free memory
    for (int i = 0; i < M; i++) {
        if (root->next[i]) {
            dfs_free(root->next[i]);
        }
    }
    free(root);
}

void insert(Node *cur_node, char *buff) {
    //  除    移除低位  保留高位信息
    //  取余  用低位确定地址
    int i = 0;
    int addr;
    unsigned short info = 0;  // Information 用来确定到底已经处理了多少信息
    unsigned short cur_value = 0;  //
    while (buff[i] != '\0'){
        if (info < M){
            info = M * 256 + info;
            cur_value = M * (unsigned char)buff[i] + cur_value;
            i ++;
        }
        while (info >= M){
            addr = cur_value % M;
            cur_value /= M;
            info /= M;
            if (cur_node->next[addr] == nullptr) {
                cur_node->next[addr] = get_node();
            }
            cur_node = cur_node->next[addr];
        }
    }
    addr = cur_value;
    if (cur_node->next[addr] == nullptr) {
        cur_node->next[addr] = get_node();
    }
    cur_node = cur_node->next[addr];
    cur_node->end = true;
}

bool find(Node *cur_node, char *buff) {
    bool exist_flag = true;
    int i = 0;
    int addr;
    unsigned short info = 0;  // Information
    unsigned short cur_value = 0;
    while (buff[i] != '\0'){
        if (info < M){
            info = M * 256 + info;
            cur_value = M * (unsigned char)buff[i] + cur_value;
            i ++;
        }
        while (info >= M){
            addr = cur_value % M;
            cur_value /= M;
            info /= M;
            if (cur_node->next[addr] == nullptr) {
                return false;
            }
            cur_node = cur_node->next[addr];
        }
    }
    addr = cur_value;
    if (cur_node->next[addr] == nullptr) {
        exist_flag = false;
    }else{
        cur_node = cur_node->next[addr];
        if (!cur_node->end) exist_flag = false;
    }
    return exist_flag;
}

int main(int argc, char *argv[]) {
    // ./mtrie /home/wanglei/course/dict.txt /home/wanglei/course/string.txt
    if (argc != 3){
        cout << "Please pass in the correct parameters" << endl;
        return 0;
    }

//    M = argc;
//    cout << M << endl;

    // speed cout and cin
    std::ios::sync_with_stdio(false);
    std::cin.tie(0);

    // timing
    clock_t start_t = clock();

    // open dict file
    FILE *fp_dict = fopen(argv[1], "r");
    if (fp_dict == NULL) cout << "fail to open dict.txt" << endl;

    // open string file
    FILE *fp_string = fopen(argv[2], "r");
    if (fp_string == NULL) cout << "fail to open string.txt" << endl;

    // open res file
    FILE *fp_res = fopen("/home/wanglei/course/result/bupt_7_mtrie.txt", "w+");
    if (fp_res == NULL) cout << "fail to open result.txt" << endl;

    // get root
    Node *root = get_node();

    int count = 0;
    char buff[N];

    // insert according to dict.txt
    while (fgets(buff, N, fp_dict) != nullptr) {
        strip(buff);
        insert(root, buff);
    }

    // search according to string.txt
    while (fgets(buff, N, fp_string) != nullptr) {
        strip(buff);
        if (find(root, buff)) {
            fputs(buff, fp_res);
            fputc('\n', fp_res);
            count++;
        }
    }

    sleep(3);

    // dfs free memory
    dfs_free(root);

    // close file
    fclose(fp_dict);
    fclose(fp_string);
    fclose(fp_res);


    cout << count << endl;
    cout << "runtime:" << "  " << (double) (clock() - start_t) / (double) (CLOCKS_PER_SEC) << endl;
}
