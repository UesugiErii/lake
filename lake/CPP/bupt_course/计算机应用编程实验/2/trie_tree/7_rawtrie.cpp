#include <iostream>
#include <unistd.h>

using namespace std;

#define N 64  // max string length

typedef struct node {
    struct node *next[256];
    bool end;
} Node;

Node *get_node() {
    // dynamic get one inited node
    Node *root;
    root = (Node *) malloc(sizeof(Node));
    for (int i = 0; i < 256; i++) {
        root->next[i] = nullptr;
    }
    root->end = false;
    return root;
}

void strip(char *buff) {
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
    for (int i = 0; i < 256; i++) {
        if (root->next[i]) {
            dfs_free(root->next[i]);
        }
    }
    free(root);
}

void insert(Node *cur, char *buff) {
    for (int i = 0; buff[i] != '\0'; i++) {
        if (cur->next[(unsigned char)buff[i]] == nullptr) {
            cur->next[(unsigned char)buff[i]] = get_node();
        }
        cur = cur->next[(unsigned char)buff[i]];
    }
    cur->end = true;
}

bool find(Node *cur, char *buff) {
    bool exist_flag = true;
    for (int i = 0; buff[i] != '\0'; i++) {
        if (cur->next[(unsigned char)buff[i]] == nullptr) {
            exist_flag = false;
            break;
        }
        cur = cur->next[(unsigned char)buff[i]];
    }
    if (!cur->end) exist_flag = false;
    return exist_flag;
}


int main(int argc, char *argv[]) {
    // ./rawtrie /home/wanglei/course/dict.txt /home/wanglei/course/string.txt
    if (argc != 3){
        cout << "Please pass in the correct parameters" << endl;
        return 0;
    }

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
    FILE *fp_res = fopen("/home/wanglei/course/result/bupt_7_rawtrie.txt", "w+");
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
