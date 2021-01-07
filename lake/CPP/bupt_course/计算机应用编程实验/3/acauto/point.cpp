#include <iostream>
#include <unistd.h>

using namespace std;

#define N 100000  // max string length

typedef struct node {
    struct node *next[256];
    struct node *fail;
    int id;
    bool end;
} Node;

class Queue {
public:
    Queue();

    ~Queue();

    int qsize();

    void put(Node *v);

    Node *get();

private:
    typedef struct element {
        Node *v;
        struct element *next;
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
    while (head) {
        head = head->next;
        free(head);
    }
}

int Queue::qsize() {
    return size;
}

void Queue::put(Node *v) {
    Element *new_element;
    new_element = (Element *) malloc(sizeof(Element));
    new_element->next = nullptr;
    new_element->v = v;
    tail->next = new_element;
    tail = new_element;
    size += 1;
}

Node *Queue::get() {
    // no size judgment
    Element *first = head->next;
    head->next = head->next->next;
    Node *temp_v = first->v;
    free(first);
    size -= 1;
    if (!size) tail = head;
    return temp_v;
};

Queue queue;


Node *get_node() {
    // dynamic get one inited node
    Node *root;
    root = (Node *) malloc(sizeof(Node));
    for (int i = 0; i < 256; i++) {
        root->next[i] = nullptr;
    }
    root->fail = nullptr;
    root->id = -1;
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

void insert(Node *cur, char *buff, int &id) {
    for (int i = 0; buff[i] != '\0'; i++) {
        if (cur->next[(unsigned char) buff[i]] == nullptr) {
            cur->next[(unsigned char) buff[i]] = get_node();
        }
        cur = cur->next[(unsigned char) buff[i]];
    }
    cur->end = true;
    cur->id = id;
}

void build(Node *root) {
    for (int i = 0; i < 256; i++) {
        if (root->next[i]) {
            root->next[i]->fail = root;
            queue.put(root->next[i]);
        }
    }
    while (queue.qsize()) {
        Node *u = queue.get();
        for (int i = 0; i < 256; i++) {
            if (u->next[i]) {
                if (u->fail->next[i]) {  // diff
                    u->next[i]->fail = u->fail->next[i];
                } else {
                    u->next[i]->fail = root;
                }
                queue.put(u->next[i]);
            } else {
                u->next[i] = u->fail->next[i];
            }
        }
    }
}


void query(Node *root, char *t, int *count) {
    Node *cur = root;
    for (int i = 0; t[i]; i++) {
        if (cur->next[(unsigned char) t[i]]) {
            cur = cur->next[(unsigned char) t[i]];
        } else {
            cur = root;
        }
//        cur = cur->next[(unsigned char) t[i]];
//        if(!cur) cur = root;  // diff
        for (Node *t = cur; t && t != root; t = t->fail) {
            if (t->end) count[t->id] += 1;
        }
    }
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

    Node *root = get_node();


    char buff[N];
    int id = 0;


    while (fgets(buff, N, fp_pattern) != nullptr) {
        strip(buff);
        insert(root, buff, id);
        id += 1;
    }




    // TODO test delete it



    root->fail = root;
    build(root);

    int count[id];
    for (int i = 0; i < id; i++) count[i] = 0;


    cout << max_ << endl;  // 2408571
    cout << count[root->next[111]->id] << endl;  // o  976963
    cout << count[root->next[116]->id] << endl;  // t  1040336


    cout << "runtime:" << "  " << (double) (clock() - start_t) / (double) (CLOCKS_PER_SEC) << endl;
}