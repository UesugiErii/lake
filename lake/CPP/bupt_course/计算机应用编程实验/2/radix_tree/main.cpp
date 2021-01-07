#include <iostream>
#include <unistd.h>

using namespace std;

#define N 46  // max string length

typedef struct node {
    // 8
    // 4 1   so can minus 3
    struct node *next[2];  // 0 -> 0, 1 -> 1
    int valid_bits;
    // first bit is end flag , 1 means end , 0 means no end
    char data[1];  // Dynamically allocate memory
} Node;

bool get_bit(char *data, int index) {
    return data[index / 8] >> (7 - index % 8) & 1;
}

void set_bit(char *data, int index, bool v) {
    if (v) {
        data[index / 8] |= v << (7 - index % 8);
    } else {
        data[index / 8] &= (-1 ^ (v ^ 1) << (7 - index % 8));  // -1 is mask
    }
}

char get_end(Node* root) {
    return get_bit(root->data, 0);
}

void set_end(Node* root, bool v) {
    set_bit(root->data, 0, v);
}


int get_bits_len(char *buff) {
    // return number of effective bits of buff
    for (int string_len = 0; string_len < N; string_len++) {
        if (buff[string_len] == '\n') {
            buff[string_len] = '\0';
        }
        if (buff[string_len] == '\0') {
            return string_len * 8;  // 1 char -> 8 bits
        }
    }
}

Node *get_node(int bits_len) {
    // dynamic get one inited node
    Node *root;
    root = (Node *) malloc(sizeof(Node) + bits_len / 8 - 3);  // only run in x64 system
    root->valid_bits = bits_len;
    set_end(root, false);
    root->next[0] = nullptr;
    root->next[1] = nullptr;
    return root;
}

void memcpy(char *dest, int dest_start, char *src, int src_start, int bits_len) {
    // diy bit memcpy
    for (int i = 0; i < bits_len; i++) {
        set_bit(
                dest, dest_start + i,
                get_bit(src, src_start + i)
        );
    }
}

int get_prefix_bits_len(char *dest, int dest_start, int dest_bits_len,
                        char *src, int src_start, int src_bits_len) {
    int i = 0;
    for (; i < dest_bits_len
           &&
           i < src_bits_len
           &&
           get_bit(dest, dest_start + i)
           ==
           get_bit(src, src_start + i); i++);
    return i;
}

// see insert.jpg
Node *insert(Node *root, char *buff, int start, int &buff_total_bits_len) {
    if (root == nullptr) {
        Node *root = get_node(buff_total_bits_len - start);
        memcpy(root->data, 1, buff, start, buff_total_bits_len - start);
        set_end(root, true);
        return root;
    } else {
        int prefix_bits_len = get_prefix_bits_len(root->data, 1, root->valid_bits, buff, start,
                                                  buff_total_bits_len - start);
        // 4 situations
        if (prefix_bits_len == buff_total_bits_len - start && prefix_bits_len == root->valid_bits) {
            // 1
            set_end(root, true);
            return root;
        } else if (prefix_bits_len == buff_total_bits_len - start) {
            // 2
            Node *new_root = get_node(prefix_bits_len);
            set_end(new_root, true);
            memcpy(new_root->data, 1, buff, start, prefix_bits_len);
            Node *child = get_node(root->valid_bits - prefix_bits_len - 1);  // old root become new_root's child
            memcpy(child->data, 1, root->data, 1 + prefix_bits_len + 1, root->valid_bits - prefix_bits_len - 1);
            new_root->next[get_bit(root->data, prefix_bits_len+1)] = child;
            child->next[0] = root->next[0];
            child->next[1] = root->next[1];
            set_end(child, get_end(root));
            free(root);
            return new_root;
        } else if (prefix_bits_len == root->valid_bits) {
            int v = get_bit(buff, start + prefix_bits_len);
            root->next[v] = insert(root->next[v], buff,
                                   start + prefix_bits_len + 1, buff_total_bits_len);
            return root;
        } else {
            //4
            Node *new_root = get_node(prefix_bits_len);
            memcpy(new_root->data, 1, buff, start, prefix_bits_len);
            Node *child_buff = get_node(buff_total_bits_len - start - prefix_bits_len - 1);
            Node *child_root = get_node(root->valid_bits - prefix_bits_len - 1);
            memcpy(child_buff->data, 1, buff, start + prefix_bits_len + 1,
                   buff_total_bits_len - start - prefix_bits_len - 1);
            memcpy(child_root->data, 1, root->data, 1 + prefix_bits_len + 1, root->valid_bits - prefix_bits_len - 1);
            child_root->next[0] = root->next[0];
            child_root->next[1] = root->next[1];
            set_end(child_root, get_end(root));
            set_end(child_buff, true);
            int v = get_bit(buff, start + prefix_bits_len);
            new_root->next[v] = child_buff;
            new_root->next[v ^ 1] = child_root;
            free(root);
            return new_root;
        }
    }
}

bool is_bit_equal(char *dest, int dest_start, char *src, int src_start, int bits_len) {
    for (int i = 0; i < bits_len; i++) {
        if (get_bit(dest, dest_start + i) != get_bit(src, src_start + i)) return false;
    }
    return true;
}


bool find(Node *root, char *buff, int start, int &buff_total_bits_len) {
    if (!root) {
        return false;
    } else if (buff_total_bits_len - start == root->valid_bits) {
        return is_bit_equal(root->data, 1, buff, start, root->valid_bits) && get_end(root);
    } else if (buff_total_bits_len - start < root->valid_bits) {
        return false;
    } else if (is_bit_equal(root->data, 1, buff, start, root->valid_bits)) {
        return find(
                root->next[get_bit(buff, start + root->valid_bits)],
                buff,
                start + root->valid_bits + 1,
                buff_total_bits_len
        );
    } else {
        return false;
    }
}

void dfs_free(Node *root) {
    // dfs free memory
    if(!root) return;
    dfs_free(root->next[0]);
    dfs_free(root->next[1]);
    free(root);
}


int main(int argc, char *argv[]) {
    // ./radix_search /home/wanglei/course/dict.txt /home/wanglei/course/string.txt
    // ./radix_search /media/zx/22CE1C4BCE1C1A1D/计算机应用编程实验/dict.txt /media/zx/22CE1C4BCE1C1A1D/计算机应用编程实验/string.txt
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
    FILE *fp_res = fopen("/media/zx/22CE1C4BCE1C1A1D/计算机应用编程实验/bupt_7_trie.txt", "w+");
    if (fp_res == NULL) {
        cout << "fail to open result.txt" << endl;
        return 0;
    }

    // get root
    Node *root = nullptr;

    int count = 0;
    char buff[N];
    int buff_total_bits_len;

    while (fgets(buff, N, fp_dict) != nullptr) {
        buff_total_bits_len = get_bits_len(buff);
        root = insert(root, buff, 0, buff_total_bits_len);
    }


    while (fgets(buff, N, fp_string) != NULL) {
        buff_total_bits_len = get_bits_len(buff);
        if (find(root, buff, 0, buff_total_bits_len)) {
            fputs(buff, fp_res);
            fputc('\n', fp_res);
            count++;
        }
    }

    sleep(10);

    // dfs free memory
    dfs_free(root);

    // close file
    fclose(fp_dict);
    fclose(fp_string);
    fclose(fp_res);

    cout << count << endl;
    cout << "runtime:" << "  " << (double) (clock() - start_t) / (double) (CLOCKS_PER_SEC) << endl;
}