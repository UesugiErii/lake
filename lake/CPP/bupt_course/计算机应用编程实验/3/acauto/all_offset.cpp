#include <iostream>
#include <unistd.h>

using namespace std;

#define N 11916  // max string length
#define QNSZ 60 // queue node size
#define SZ 4528983  // number of trie's nodes
#define PSZ 1282552  // pattern nums + 1

//#define N 20000  // max string length
//#define QNSZ 60 // queue node size
//#define SZ 6000000  // number of trie's nodes
//#define PSZ 2000000  // pattern nums + 1

class Queue {
    // only can store int
public:
    Queue();

    ~Queue();

    bool empty();

    void put(int v);

    int get();

private:
    typedef struct node {
        struct node *next;
        int v[QNSZ];
        int r_index;
        int w_index;
    } Node;
    Node *head;
    Node *tail;
};

Queue::Queue() {
    head = nullptr;
    tail = nullptr;
}

Queue::~Queue() {
    Node *temp;
    while (head) {
        temp = head->next;
        free(head);
        head = temp;
    }
}

bool Queue::empty() {
    return head ? false : true;
}

void Queue::put(int v) {
    if (!tail) {
        Node *new_node = (Node *) malloc(sizeof(Node));
        new_node->v[0] = v;
        new_node->r_index = 0;
        new_node->w_index = 1;
        new_node->next = nullptr;

        head = new_node;
        tail = new_node;
    } else if (tail->w_index == QNSZ) {
        Node *new_node = (Node *) malloc(sizeof(Node));
        new_node->v[0] = v;
        new_node->r_index = 0;
        new_node->w_index = 1;
        new_node->next = nullptr;

        tail->next = new_node;
        tail = new_node;
    } else {
        tail->v[tail->w_index++] = v;
    }
}

int Queue::get() {
    // no empty judgment
    int ret;
    if (head == tail) {
        ret = head->v[head->r_index++];
        if (head->r_index == head->w_index) {
            head = nullptr;
            tail = nullptr;
        }
    } else {
        ret = head->v[head->r_index++];
        if (head->r_index == head->w_index) head = head->next;
    }
    return ret;
};


int strip(char *buff) {
    for (int i = 0; i < N; i++) {
        if (buff[i] == '\n') {
            buff[i] = '\0';
        }
        if (buff[i] == '\0') {
            return i;
        }
    }
    return 0;
}


class AC {
public:
    AC();

    ~AC();

    void insert(char *s, int &str_len);

    void build();

    void query(char *t, int &str_len);

    void sort();

    void quick_sort(int low, int high);

    void insert_sort(int *arr, int len);

    bool small_than(int x, int y);


    int tot;
    int id;
    int **tr, *fail, *idx;
    int *cnt;
    int *sorted_id;

    Queue q;

    char **pattern;
    int string_offset;
    Queue *pattern_offset;
    int *pattern_len;
};

AC::AC() {
    tr = (int **) malloc(SZ * sizeof(int *));
    for (int i = 0; i < SZ; i++)
        tr[i] = (int *) malloc(256 * sizeof(int));  // transfer
    fail = (int *) malloc(SZ * sizeof(int));
    idx = (int *) malloc(SZ * sizeof(int));  // map tot to id
    cnt = (int *) malloc(PSZ * sizeof(int));  // count, use id as index
    sorted_id = (int *) malloc(PSZ * sizeof(int));  // sorted id

    pattern = (char **) malloc(PSZ * sizeof(char *));
    string_offset = 0;
    pattern_offset = new Queue[PSZ];
    pattern_len = (int *) malloc(PSZ * sizeof(int));

    // tot and id are start from 1
    tot = 0;  // Used as the index of the trie node
    id = 0;  // Used as the index of the trie node which is last char of string
    for (int i = 0; i < SZ; i++) {
        for (int j = 0; j < 256; j++) {
            tr[i][j] = 0;
        }
        fail[i] = 0;
        idx[i] = 0;
    }
    for (int i = 0; i < PSZ; i++) {
        cnt[i] = 0;
        pattern_len[i] = 0;
        sorted_id[i] = i;
    }
}

AC::~AC() {
    for (int i = 0; i < SZ; i++)
        free(tr[i]);
    for (int i = 0; i < PSZ; i++)
        free(pattern[i]);
    free(tr);
    free(fail);
    free(idx);
    free(cnt);
    free(pattern_len);

    delete[] pattern_offset;
}

void AC::insert(char *s, int &str_len) {
    int u = 0;
    for (int i = 0; s[i]; i++) {
        if (!tr[u][(unsigned char) s[i]]) tr[u][(unsigned char) s[i]] = ++tot;
        u = tr[u][(unsigned char) s[i]];
    }
    idx[u] = ++id;

    pattern[id] = (char *) malloc(str_len * sizeof(char));
    for (int i = 0; i < str_len; i++) pattern[id][i] = s[i];
    pattern_len[id] = str_len;
}

void AC::build() {
    // build fail and tr
    for (int i = 0; i < 256; i++)
        if (tr[0][i]) q.put(tr[0][i]);
    while (!q.empty()) {
        int u = q.get();
        for (int i = 0; i < 256; i++) {
            if (tr[u][i])
                fail[tr[u][i]] = tr[fail[u]][i], q.put(tr[u][i]);
            else
                tr[u][i] = tr[fail[u]][i];
        }
    }
}

void AC::query(char *t, int &str_len) {
    // dont return anything, only add cnt
    int u = 0;
    int id;
    for (int i = 0; t[i]; i++) {
        u = tr[u][(unsigned char) t[i]];
        for (int j = u; j; j = fail[j]) {
            id = idx[j];
            if (id) {
                cnt[id]++;
                pattern_offset[id].put(string_offset + i - pattern_len[id] + 1);
            }
        }
    }
    string_offset += str_len;
    string_offset += 1;  // \n
}

/*
 * Don't use this, bubble_sort takes about 11 and a half hours to run
 * Use the following quick_sort
 */
//void AC::bubble_sort() {
//    // 0 index dont sort
//    for (int i = 1; i < PSZ; i++) {
//        cout << "sort: " << i << endl;
//        for (int j = 1; j < PSZ - 1; j++) {
//            if (small_than(sorted_id[j], sorted_id[j + 1])) {
//                sorted_id[j] = sorted_id[j] ^ sorted_id[j + 1];
//                sorted_id[j + 1] = sorted_id[j] ^ sorted_id[j + 1];
//                sorted_id[j] = sorted_id[j] ^ sorted_id[j + 1];
//            }
//        }
//    }
//}


void swap(int *arr, int i, int j) {
    // swap arr[i] and arr[j]
    if (i != j)
        arr[i] ^= arr[j] ^= arr[i] ^= arr[j];
}

void AC::sort() {
    quick_sort(1, id);
    insert_sort(sorted_id + 1, id);
}

void AC::quick_sort(int low, int high) {  // arr is sorted_id
    if (high - low > 31) {
//    if (low < high) {
        int i = low;
        int j = high - 1;
        int mid = (high - low) / 2 + low;

        if (small_than(sorted_id[low], sorted_id[high])) swap(sorted_id, low, high);
        if (small_than(sorted_id[low], sorted_id[mid])) swap(sorted_id, low, mid);
        if (small_than(sorted_id[mid], sorted_id[high])) swap(sorted_id, mid, high);
        swap(sorted_id, mid, high - 1);

        int k = sorted_id[high - 1];

        while (true) {
            while (small_than(k, sorted_id[++i]));
            while (small_than(sorted_id[--j], k));
            if (i < j) swap(sorted_id, i, j);
            else break;
        }
        swap(sorted_id, i, high - 1);

        quick_sort(low, i - 1);
        quick_sort(i + 1, high);
    }
}

void AC::insert_sort(int *arr, int len) {
    for (int i = 1; i < len; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && small_than(arr[j], key)) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}


bool AC::small_than(int x, int y) {
    // x, y is id
    // if x == y, return false
    if (cnt[x] == cnt[y]) {
        int i = 0;
        for (; pattern[x][i] && pattern[y][i]; i++) {
            if (pattern[x][i] != pattern[y][i]) return pattern[x][i] < pattern[y][i];
        }
        if (pattern[x][i] == '\0' && pattern[y][i] == '\0') {
            return false;
        } else if (pattern[x][i] == '\0') {
            return true;
        } else {
            return false;
        }
    } else {
        return cnt[x] < cnt[y];
    }
}

int main(int argc, char *argv[]) {
    // ./acauto /media/zx/22CE1C4BCE1C1A1D/pattern+string/pattern.txt /media/zx/22CE1C4BCE1C1A1D/pattern+string/string.txt /media/zx/22CE1C4BCE1C1A1D/pattern+string/result.txt
    if (argc != 4) {
        cout << endl << "Please pass in the correct parameters" << endl;
        cout << "example:" << endl;
        cout << "acauto dict.txt string.txt result.txt" << endl;
        return 0;
    }
    std::ios::sync_with_stdio(false);
    std::cin.tie(0);

    clock_t start_t = clock();

    // open dict file
    FILE *fp_pattern = fopen(argv[1], "r");
    if (fp_pattern == NULL) {
        cout << "fail to open pattern.txt" << endl;
        return 0;
    }

    // open string file
    FILE *fp_string = fopen(argv[2], "r");
    if (fp_string == NULL) {
        cout << "fail to open string.txt" << endl;
        return 0;
    }

    FILE *fp_result = fopen(argv[3], "w+");
    if (fp_result == NULL) {
        cout << "fail to open result.txt" << endl;
        return 0;
    }


    int str_len;
    char buff[N];
    AC ac;

    while (fgets(buff, N, fp_pattern) != nullptr) {
        str_len = strip(buff);
        ac.insert(buff, str_len);
    }

    ac.build();

    while (fgets(buff, N, fp_string) != nullptr) {
        str_len = strip(buff);
        ac.query(buff, str_len);
    }

    ac.sort();

    // test sort
//    for (int i = 1; i < ac.id; i++) {
//        if (ac.small_than(ac.sorted_id[i], ac.sorted_id[i + 1])) {
//            cout << "sort error" << endl;
//            return 0;
//        }
//    }


    int id;
    for (int i = 1; i <= ac.id; i++) {
        id = ac.sorted_id[i];
        for (int j = 0; j < ac.pattern_len[id]; j++) fputc(ac.pattern[id][j], fp_result);
        fputc(' ', fp_result);
        fputs(to_string(ac.cnt[id]).c_str(), fp_result);
        for (int j = 0; j < ac.cnt[id]; j++) {
            fputc(' ', fp_result);
            fputs(to_string(ac.pattern_offset[id].get()).c_str(), fp_result);
        }
        fputc('\n', fp_result);
    }


    sleep(3);
    cout << "runtime:" << "  " << (double) (clock() - start_t) / (double) (CLOCKS_PER_SEC) << endl;
}
