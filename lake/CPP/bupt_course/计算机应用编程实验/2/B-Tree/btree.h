//
// Created by Once on 2019/7/22.
//

#ifndef TREE_BTREE_H
#define TREE_BTREE_H

// 键值数组结构
typedef struct column{
    int id; // 关键字
    char title[70];
} Column;

// B树结点
typedef struct bnode{
    int size; // 当前关键字数目
    Column **columns; // 键值数组
    struct bnode **children; // 儿子指针数组
    struct bnode *parent; //父指针
    struct bnode *next; //横向顺序查找的链表指针
    unsigned int leaf; // 是否为叶子 1是 0否
} BNode;

// B树ADT对外接口
typedef struct btree{
    unsigned int degree; // 度数
    BNode *root; // 根结点
    BNode *head; // 叶子链表的头结点
    unsigned int size; // B树结点大小
} BTree;

// B树算法操作声明
extern BTree *btree_init(unsigned int degree); //初始化
extern int btree_is_empty(BTree *btree); //空
extern int btree_add(BTree *btree, Column *column); //添加一个节点
extern int btree_delete_by_id(BTree *btree, int id); // 按id删除一个节点
extern Column *btree_max(BTree *btree); //最大值
extern Column *btree_min(BTree *btree); // 最小值
extern Column *btree_get_by_value(BTree *btree, Column * c); //按值获取一个节点
extern void btree_traverse(BTree *btree, void(*traverse)(BNode*));//遍历
extern int btree_clear(BTree *btree);//释放空间
extern void print_node_data(BNode *node);
extern void print_node(BNode *node);
extern int btree_node_count(BTree *btree);
extern int btree_leaf_count(BTree *btree);
extern void setDebug(int d);
// 最小度数t>=2，度数就是子树个数
// 根结点的关键字数最小为1
// 非叶非根结点的度数：t <= T <= 2t-1
// 非根结点的关键字数：t <= K <= 2t-1
// 关键数K和度数的关系为：K = T。
// 所有叶子结点的深度相同
// 满关键字为2t-1，分裂为两个子树
#endif //TREE_BTREE_H
