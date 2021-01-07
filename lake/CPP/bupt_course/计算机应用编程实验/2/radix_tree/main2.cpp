#include <iostream>

using namespace std;

#define N 46  // max string length

typedef struct node {
    struct node *next[2];  // 0 -> 0, 1 -> 1
    int valid_bits;
    bool end;
    char data[1];  // Dynamically allocate memory
} Node;

char get_bit(char *data, int index) {
    return data[index / 8] >> (7 - index % 8) & 1;
}

void set_bit(char *data, int index, char &v) {
    if (v) {
        data[index / 8] |= v << (7 - index % 8);
    } else {
        data[index / 8] &= (-1 ^ (v ^ 1) << (7 - index % 8));  // -1 is mask
    }
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
    root = (Node *) malloc(sizeof(Node) + (bits_len - 1) / 8);
    root->valid_bits = bits_len;
    root->end = false;
    root->next[0] = nullptr;
    root->next[1] = nullptr;
    return root;
}

void memcpy(char *dest, int dest_start, char *src, int src_start, int bits_len) {
    // diy bit memcpy
    char v;
    for (int i = 0; i < bits_len; i++) {
        v = get_bit(src, src_start + i);
        set_bit(dest, dest_start + i, v);
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
        memcpy(root->data, 0, buff, start, buff_total_bits_len - start);
        root->end = true;
        return root;
    } else {
        int prefix_bits_len = get_prefix_bits_len(root->data, 0, root->valid_bits, buff, start,
                                                  buff_total_bits_len - start);
        // 4 situations
        if (prefix_bits_len == buff_total_bits_len - start && prefix_bits_len == root->valid_bits) {
            // 1
            root->end = true;
            return root;
        } else if (prefix_bits_len == buff_total_bits_len - start) {
            // 2
            Node *new_root = get_node(prefix_bits_len);
            new_root->end = true;
            memcpy(new_root->data, 0, buff, start, prefix_bits_len);
            Node *child = get_node(root->valid_bits - prefix_bits_len - 1);  // old root become new_root's child
            memcpy(child->data, 0, root->data, prefix_bits_len + 1, root->valid_bits - prefix_bits_len - 1);
            new_root->next[get_bit(root->data, prefix_bits_len)] = child;
            child->next[0] = root->next[0];
            child->next[1] = root->next[1];
            child->end = root->end;
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
            memcpy(new_root->data, 0, buff, start, prefix_bits_len);
            Node *child_buff = get_node(buff_total_bits_len - start - prefix_bits_len - 1);
            Node *child_root = get_node(root->valid_bits - prefix_bits_len - 1);
            memcpy(child_buff->data, 0, buff, start + prefix_bits_len + 1,
                   buff_total_bits_len - start - prefix_bits_len - 1);
            memcpy(child_root->data, 0, root->data, prefix_bits_len + 1, root->valid_bits - prefix_bits_len - 1);
            child_root->next[0] = root->next[0];
            child_root->next[1] = root->next[1];
            child_root->end = root->end;
            child_buff->end = true;
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
        return is_bit_equal(root->data, 0, buff, start, root->valid_bits) and root->end;
    } else if (buff_total_bits_len - start < root->valid_bits) {
        return false;
    } else if (is_bit_equal(root->data, 0, buff, start, root->valid_bits)) {
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


int main() {
    // speed cout and cin
    std::ios::sync_with_stdio(false);
    std::cin.tie(0);

    // timing
    clock_t start_t = clock();

    // open dict file
    FILE *fp_dict = fopen("/home/wanglei/course/dict.txt", "r");
    if (fp_dict == NULL) cout << "fail to open dict.txt" << endl;

    // open string file
    FILE *fp_string = fopen("/home/wanglei/course/string.txt", "r");
    if (fp_string == NULL) cout << "fail to open string.txt" << endl;

    // open res file
    FILE *fp_res = fopen("/home/wanglei/course/result/bupt_7_trie.txt", "w+");
    if (fp_res == NULL) cout << "fail to open result.txt" << endl;

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


    // close file
    fclose(fp_dict);
    fclose(fp_string);
    fclose(fp_res);

    cout << count << endl;
    cout << "runtime:" << "  " << (double) (clock() - start_t) / (double) (CLOCKS_PER_SEC) << endl;
}