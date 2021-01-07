// bak before modify Queue

#include <iostream>
#include <unistd.h>

using namespace std;

#define N 11916  // max string length

class Queue {
    // only can store int
public:
    Queue();

    ~Queue();

    int qsize();

    void put(int v);

    int get();

private:
    typedef struct element {
        struct element *next;
        int v;
    } Element;
    int size;
    Element *head;
    Element *tail;
};

Queue::Queue() {
    Element *sentinel;
    sentinel = (Element *) malloc(sizeof(Element));
    sentinel->next = nullptr;
    head = sentinel;
    tail = sentinel;
    size = 0;
}

Queue::~Queue() {
    Element * temp;
    while (head) {
        temp = head->next;
        free(head);
        head = temp;
    }
}

int Queue::qsize() {
    return size;
}

void Queue::put(int v) {
    Element *new_element;
    new_element = (Element *) malloc(sizeof(Element));
    new_element->next = nullptr;
    new_element->v = v;
    tail->next = new_element;
    tail = new_element;
    size += 1;
}

int Queue::get() {
    // no size judgment
    Element *first = head->next;
    head->next = head->next->next;
    int temp_v = first->v;
    free(first);
    size -= 1;
    if (!size) tail = head;
    return temp_v;
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

#define SZ 4528983

class AC {
public:
    AC();

    ~AC();

    void insert(char *s, int &str_len);

    void build();

    void query(char *t, int &str_len);


    int tot;
    int id;
    int **tr, *fail, *idx;
    int *cnt;
    Queue q;

    char **data;
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
    cnt = (int *) malloc(1282552 * sizeof(int));  // count, use id as index

    data = (char **) malloc(1282552 * sizeof(char *));
    string_offset = 0;
    pattern_offset = new Queue[1282552];
    pattern_len = (int *) malloc(1282552 * sizeof(int));

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
    for (int i = 0; i < 1282552; i++) {
        cnt[i] = 0;
        pattern_len[i] = 0;
    }
}

AC::~AC() {
    for (int i = 0; i < SZ; i++)
        free(tr[i]);
    for (int i = 0; i < 1282552; i++)
        free(data[i]);
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

    data[id] = (char *) malloc(str_len * sizeof(char));
    for (int i = 0; i < str_len; i++) data[id][i] = s[i];
    pattern_len[id] = str_len;
}

void AC::build() {
    // build fail and tr
    for (int i = 0; i < 256; i++)
        if (tr[0][i]) q.put(tr[0][i]);
    while (q.qsize()) {
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

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(0);

    clock_t start_t = clock();

    // open dict file
    FILE *fp_pattern = fopen("/media/zx/22CE1C4BCE1C1A1D/pattern+string/pattern.txt", "r");
    if (fp_pattern == NULL) cout << "fail to open pattern.txt" << endl;

    // open string file
    FILE *fp_string = fopen("/media/zx/22CE1C4BCE1C1A1D/pattern+string/string.txt", "r");
    if (fp_string == NULL) cout << "fail to open string.txt" << endl;

    int str_len;
    char buff[N];
    AC ac;


    while (fgets(buff, N, fp_pattern) != nullptr) {
        str_len = strip(buff);
        ac.insert(buff, str_len);
    }

    ac.build();


    int jishu = 0;

    while (fgets(buff, N, fp_string) != nullptr) {
        str_len = strip(buff);
        ac.query(buff, str_len);
        cout << ++jishu << endl;
    }



//    //test code
    int max_ = 0;
    for (int i = 0; i < ac.id; i++) {
        if (ac.cnt[i] > max_) {
            max_ = ac.cnt[i];
        }
    }

    cout << max_ << endl;  // 2408571
    cout << ac.cnt[ac.idx[ac.tr[0][111]]] << endl;  // o  976963
    cout << ac.cnt[ac.idx[ac.tr[0][116]]] << endl;  // t  1040336


    cout << "runtime:" << "  " << (double) (clock() - start_t) / (double) (CLOCKS_PER_SEC) << endl;
}
