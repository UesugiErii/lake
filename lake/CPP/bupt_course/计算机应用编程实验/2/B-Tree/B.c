#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "btree.h"

// ! 以下方法 return 0失败 1成功

static int debug_ = 0;
void setDebug(int d)
{
  debug_ = d;
}
int debug()
{
  return debug_;
}
//0不等 1相等
int column_is_equal(const Column *a, const Column *b)
{
  if (strcmp(a->title, b->title) == 0)
    return 1;
  return 0;
  //TODO
  // return a->id == b->id;
}
//a>b则1，否则0
int column_a_greater_than_b(const Column *a, const Column *b)
{
  if (strcmp(a->title, b->title) > 0)
    return 1;
  return 0;
  //TODO
  // return a->id > b->id;
}
//a>=b则1，否则0
int column_a_greater_or_equal_b(const Column *a, const Column *b)
{
  int r = strcmp(a->title, b->title);
  if (r >= 0)
    return 1;
  return 0;
  //TODO
  // return a->id >= b->id;
}

void print_node_data(BNode *node)
{
  if (node == NULL || node->size == 0)
  {
    printf("null");
    return;
  }
  else if (node->size == 1)
  {
    // printf("[%s]", node->columns[0]->title);
    //TODO
    printf("[%d]", node->columns[0]->id);
    return;
  }
  printf("[");
  int i;
  // for (i = 0; i < node->size - 1; i++)
  // {
  //   printf("%s, ", node->columns[i]->title);
  // }
  // printf("%s]", node->columns[node->size - 1]->title);
  //TODO
  for (i = 0; i < node->size - 1; i++)
  {
    printf("%d, ", node->columns[i]->id);
  }
  printf("%d]", node->columns[node->size - 1]->id);
}
void print_node(BNode *node)
{
  if (node == NULL || node->size == 0)
  {
    printf("null\n");
    return;
  }
  print_node_data(node);
  if (node->leaf)
  {
    printf(" (leaf)");
  }
  printf(", size: %d", node->size);
  printf(", parent:");
  print_node_data(node->parent);
  printf(", next:");
  print_node_data(node->next);
  printf("\n");
}

int node_count(BNode *node)
{
  if (node == NULL || node->size == 0)
    return 0;
  if (node->leaf)
    return node->size;
  int i = 0;
  int count = node->size;
  for (i = 0; i < node->size; i++)
    count += node_count(node->children[i]);
  return count;
}

int btree_node_count(BTree *btree)
{
  if (btree == NULL)
    return 0;
  return node_count(btree->root);
}

int leaf_count(BNode *node)
{
  if (node == NULL || node->size == 0)
    return 0;
  if (node->leaf)
    return node->size;
  int i = 0;
  int count = 0;
  for (i = 0; i < node->size; i++)
    count += leaf_count(node->children[i]);
  return count;
}

int btree_leaf_count(BTree *btree)
{
  if (btree == NULL)
    return 0;
  return leaf_count(btree->root);
}
// 顺序查找结点关键字
// 每个结点最多关键字为2t-1，时间复杂度为O(2t-1)，即O(t)
int seq_search(const Column *array[], const int len, const Column *value)
{
  int i = 0;
  while (i <= len - 1 && column_a_greater_than_b(value, array[i]))
    i++;
  return i;
}

// 二分法查找结点上相同的关键字、确定儿子访问位置
// 每个结点关键字数为2t-1，时间复杂度为O(log(2t-1))，即O(log t)
int binary_search(Column *array[], const int len, const Column *value)
{
  int start = 0, end = len - 1, index = 0, center = (start + end) / 2;
  while (start <= end)
  {
    if (column_is_equal(value, array[center]) == 1)
    {
      index = center;
      break;
    }
    else if (column_a_greater_than_b(value, array[center]) == 1)
    {
      index = center + 1;
      center += 1;
      start = center;
    }
    else
    {
      index = center;
      center -= 1;
      end = center;
    }
    center = (start + end) / 2;
  }
  return index;
}

//初始化
BTree *btree_init(unsigned int degree)
{
  BTree *btree = (BTree *)malloc(sizeof(BTree));
  if (!btree)
  {
    perror("init b tree error.");
    return NULL;
  }
  btree->root = NULL;
  btree->head = NULL;
  btree->size = 0;
  btree->degree = degree;
  return btree;
}
//空
int btree_is_empty(BTree *btree)
{
  if (btree == NULL)
    return 1;
  return btree->size == 0;
}
//结点构造器
//按BTree的设置（m叉），生成一个结点
//还没插入树中
BNode *new_node(BTree *btree)
{
  BNode *node = (BNode *)malloc(sizeof(BNode));
  if (!node)
    return NULL;
  node->columns = (Column **)malloc(sizeof(Column *) * (2 * btree->degree - 1)); //2t-1个关键字
  node->children = (BNode **)malloc(sizeof(BNode *) * (2 * btree->degree - 1));  // 2t棵子树
  node->size = 0;
  node->leaf = 0;
  node->next = NULL;
  node->parent = NULL;
  if (!node->columns)
  {
    free(node);
    return NULL;
  }
  if (!node->children)
  {
    free(node->columns);
    free(node);
    return NULL;
  }
  int i = 0;
  for (i = 0; i < 2 * btree->degree - 1; i++)
  {
    node->columns[i] = NULL;
    node->children[i] = NULL;
  }
  return node;
}

//当前结点是满的
int node_is_full(BTree *btree, BNode *node)
{
  if (node == NULL)
    return 0;
  if (node->size == 2 * btree->degree - 1)
    return 1;
  return 0;
}

// 将数据 column 复制一份，存储为 node 的第 index 个关键字
// index 从 0 开始
int replace_data_at_node(BNode *node, int index, Column *column)
{
  Column *c = (Column *)malloc(sizeof(Column));
  if (!c)
    return 0;
  c->id = column->id;
  strcpy(c->title, column->title);
  node->columns[index] = c;
  return 1;
}

//将数据 column 存储为 node 的第 index 个关键字
// index 从 0 开始
int save_data_to_node(BNode *node, int index, Column *column)
{
  if (debug())
  {
    printf("保存到 %d 到 index:%d\n", column->id, index);
    printf("保存前--\n");
    print_node(node);
  }
  replace_data_at_node(node, index, column);
  node->size++;
  if (debug())
  {
    printf("保存后--\n");
    print_node(node);
  }
  return 1;
}

// 最大值
Column *node_max(BNode *root)
{
  while (!root->leaf)
    root = root->children[root->size - 1];
  return root->columns[root->size - 1];
}
// A、子树最大值
Column *btree_max(BTree *btree)
{
  if (btree == NULL || btree->size == 0)
    return NULL;
  return node_max(btree->root);
}
// B、子树最小值
Column *node_min(BNode *root)
{
  while (!root->leaf)
    root = root->children[0];
  return root->columns[0];
}

Column *btree_min(BTree *btree)
{
  if (btree == NULL || btree->size == 0)
    return NULL;
  return node_min(btree->root);
}
// 按 id 在子树中查找
Column *btree_get(BNode *root, Column *c)
{
  int index = binary_search(root->columns, root->size, c);
  if (index >= root->size)
    index--;
  if (index < root->size && column_is_equal(root->columns[index], c) == 1)
    return root->columns[index];
  else if (root->leaf)
    return NULL;
  else
    return btree_get(root->children[index], c);
}

Column *btree_get_by_value(BTree *btree, Column *c)
{
  if (btree == NULL || btree->size == 0)
    return NULL;
  return btree_get(btree->root, c);
}

//中序遍历
// 0. 插入5个
// [1, 2, 3, 4, 5]
//
// 1. 插入6个
// [3]
// |--[1, 2]
// |--[4, 5, 6]
//
// 2. 插入30个
// [9, 18]
// |--[3, 6]
// |--|--[1, 2]
// |--|--[4, 5]
// |--|--[7, 8]
// |--[12, 15]
// |--|--[10, 11]
// |--|--[13, 14]
// |--|--[16, 17]
// |--[21, 24, 27]
// |--|--[19, 20]
// |--|--[22, 23]
// |--|--[25, 26]
// |--|--[28, 29, 30]
void traverse_tree(BNode *root, int depth, char *prefix, void (*traverse)(BNode *))
{
  //1.输出当前结点的信息
  printf("%s", prefix);
  traverse(root);
  //2.依次遍历子树
  char *prefix_plus = malloc(sizeof(char) * (depth * 3 + 1));
  int i;
  for (i = 0; i < depth * 3; i++)
  {
    prefix_plus[i] = ' ';
  }
  // strcpy(prefix_plus, prefix);

  prefix_plus[depth * 3] = '|';
  prefix_plus[depth * 3 + 1] = '-';
  prefix_plus[depth * 3 + 2] = '-';
  prefix_plus[depth * 3 + 3] = '\0';
  if (!root->leaf)
  {
    for (i = 0; i < root->size; ++i)
    {
      traverse_tree(root->children[i], depth + 1, prefix_plus, traverse);
    }
  }
  //printf("遍历完成 %d, %s\n", depth, root->columns[0]->title);
}

void traverse_node(BNode *root)
{
  traverse_tree(root, 0, "", print_node);
}
void btree_traverse(BTree *btree, void (*traverse)(BNode *))
{
  if (btree == NULL || btree->size == 0)
    return;
  traverse_tree(btree->root, 0, "", traverse);
}

//替换中间结点的最大值 last_column 为 column
int replace_max_of_intrenal_node(BTree *btree, BNode *root, Column *last_column, Column *column)
{
  if (debug())
  {

    printf("替换中间结点 ");
    print_node_data(root);
    printf(" 的最大值 %d 为 %d\n", last_column->id, column->id);
  }
  int i;
  if (root->leaf)
  {
    return 0;
  }
  else
  {
    for (i = 0; i < root->size; i++)
    {
      if (column_is_equal(root->columns[i], last_column) == 1)
      {
        // replace_data_at_node(root, i, column);
        root->columns[i] = column;
        if (i == root->size - 1 && root->parent != NULL)
        {
          replace_max_of_intrenal_node(btree, root->parent, last_column, column);
        }
        break;
      }
    }
    return 1;
  }
}

//left是满的，因需要添加column而需要分裂
//此函数将生成right树，根据index把column放在左子树或右子树
//这里处理了next, leaf, columns, children
//没有处理 column 对应的子树
BNode *generateRight(BTree *btree, BNode *left, Column *column, int index)
{
  BNode *right = new_node(btree);
  if (!right)
    return NULL;
  right->next = left->next;
  left->next = right;
  right->leaf = left->leaf;
  //index 决定了column在分裂后是位于左子树还是右子树
  int i, right_index;
  int middle_index = btree->degree;
  if (index >= middle_index)
  {
    //column将位于右子树
    if (debug())
      printf("  %d 将位于右子树，index=%d\n", column->id, index - middle_index);
    //1. 复制出右子树
    for (i = middle_index; i < left->size; i++)
    {
      //左子树复制到右子树：左结点的第i棵子树复制为右结点的第right_index棵子树
      right_index = i - middle_index;
      right->columns[right_index] = left->columns[i];
      right->children[right_index] = left->children[i];
      if (right->children[right_index] != NULL)
      {
        right->children[right_index]->parent = right;
      }
    }
    right->size = btree->degree - 1;
    left->size = btree->degree;
    //2. 插入column
    right_index = index - middle_index; //column在右子树中的位置
    for (i = right->size; i > right_index; --i)
    {
      right->columns[i] = right->columns[i - 1];
      right->children[i] = right->children[i - 1];
      if (right->children[i] != NULL)
      {
        right->children[i]->parent = right;
      }
    }
    save_data_to_node(right, right_index, column);
  }
  else
  {
    //column将位于左子树
    if (debug())
    {
      printf("  %d 将位于左子树，index=%d\n", column->id, index);
    }
    //1. 复制出右子树
    for (i = middle_index - 1; i < left->size; i++)
    {
      //左子树复制到右子树：左结点的第i棵子树复制为右结点的第right_index棵子树
      right_index = i - middle_index + 1;
      right->columns[right_index] = left->columns[i];
      right->children[right_index] = left->children[i];
      if (right->children[right_index] != NULL)
      {
        right->children[right_index]->parent = right;
      }
    }
    right->size = btree->degree;
    left->size = btree->degree - 1;
    //2. 插入column
    //column在左子树中的位置就是index
    for (i = left->size; i > index; --i)
    {
      left->columns[i] = left->columns[i - 1];
      left->children[i] = left->children[i - 1];
      if (right->children[i] != NULL)
      {
        right->children[i]->parent = right;
      }
    }
    save_data_to_node(left, index, column);
  }
  return right;
}

//root是根结点且是满的，添加 left_subtree_of_root 和 right_subtree_of_root 到 root。这将导致 root 分裂。
//left_subtree_of_root->parent == root，root的某棵子树就是 left_subtree_of_root，但没有root没有left_subtree_of_root的最大值
//right_subtree_of_root->parent == NULL, right_subtree_of_root的最大值在root中，但root没有子树指向 right_subtree_of_root
int split_root_and_add_subtree(BTree *btree, BNode *root, BNode *left_subtree_of_root, BNode *right_subtree_of_root)
{
  int i;
  Column *right_max_value = node_max(right_subtree_of_root);
  Column *left_max_value = node_max(left_subtree_of_root);
  //root中有right的max，没有left的max
  //所以这里找left的max在root中的插入点 index_in_root
  int index_in_root = binary_search(root->columns, root->size, left_max_value);

  BNode *left = root;
  BNode *right = generateRight(btree, left, left_max_value, index_in_root);
  if (right == NULL)
    return 0;
  if (debug())
  {
    printf("  分裂为两棵子树，左子树 ");
    print_node_data(left);
    printf("，右子树 ");
    print_node_data(right);
    printf("\n");
  }
  //generateRight没有处理left_subtree_of_root的子树，下面处理一下
  int middle_index = btree->degree;
  if (index_in_root >= middle_index)
  {
    //column的子树将位于右子树
    if (debug())
    {
      print_node_data(left_subtree_of_root);
      printf(" 将位于右子树 ");
      print_node_data(right);
      printf("\n");
    }
    right->children[index_in_root - middle_index] = left_subtree_of_root;
    left_subtree_of_root->parent = right;
    //由于 right_subtree_of_root 在 left_subtree_of_root 的右边，所以 right_subtree_of_root 也一定在右子树
    //且 left_subtree_of_root 的右边就是 right_subtree_of_root
    right->children[index_in_root - middle_index + 1] = right_subtree_of_root;
    right_subtree_of_root->parent = right;
    if (debug())
    {
      print_node_data(right_subtree_of_root);
      printf(" 将位于右子树 ");
      print_node_data(right);
      printf("\n");
    }
  }
  else
  {
    if (debug())
    {
      print_node_data(left_subtree_of_root);
      printf(" 将位于左子树 ");
      print_node_data(left);
      printf("\n");
    }
    //column的子树将位于左子树
    left->children[index_in_root] = left_subtree_of_root;
    left_subtree_of_root->parent = left;
    //由于 left_subtree_of_root 的右边就是 right_subtree_of_root
    //判断 index_in_root 是否超过 left->size-1 就可以知道 right_subtree_of_root 在 left 还是 right 的 0 号位
    if (index_in_root >= left->size - 1)
    {
      //right_subtree_of_root 将位于右子树
      right->children[0] = right_subtree_of_root;
      right_subtree_of_root->parent = right;
      if (debug())
      {
        print_node_data(right_subtree_of_root);
        printf(" 将位于右子树 ");
        print_node_data(right);
        printf("\n");
      }
    }
    else
    {
      //right_subtree_of_root 将位于左子树
      left->children[index_in_root + 1] = right_subtree_of_root;
      right_subtree_of_root->parent = left;
      if (debug())
      {
        print_node_data(right_subtree_of_root);
        printf(" 将位于左子树 ");
        print_node_data(left);
        printf("\n");
      }
    }
  }

  BNode *parent = new_node(btree);
  if (!parent)
    return 0;
  parent->size = 2;
  parent->children[0] = left;
  parent->children[1] = right;
  parent->columns[0] = node_max(left);
  parent->columns[1] = node_max(right);
  parent->leaf = 0;
  parent->size = 2;
  btree->root = parent;

  left->parent = parent;
  right->parent = parent;
  return 1;
}
//将 left 和 right 添加到 root，需要分裂 root
//（外部调用时保证）当前结点是满的
//（外部调用时保证）当前节点是中间节点，一定不是叶子节点
//（外部调用时保证）root->leaf == 0 && root->size == 2 * btree->degree - 1
//当前结点可能是根结点，也可能是有父结点的中间结点
int split_middle_or_root_and_add_subtree(BTree *btree, BNode *root, BNode *left_subtree_of_root, BNode *right_subtree_of_root)
{
  //由于 right_subtree_of_root 是由 left_subtree_of_root 分裂而来，left_subtree_of_root 没分裂前是 root 的子树
  //所以 root 里一定有 right_subtree_of_root 的 max 数据和指向 left_subtree_of_root 的指针
  //0. 先分割当前结点
  //root是根结点且是满的，添加 left_subtree_of_root 和 right_subtree_of_root 到 root。这将导致 root 分裂。
  //left_subtree_of_root->parent == root，root的某棵子树就是 left_subtree_of_root，但没有root没有left_subtree_of_root的最大值
  //right_subtree_of_root->parent == NULL, right_subtree_of_root的最大值在root中，但root没有子树指向 right_subtree_of_root
  int i;
  Column *right_max_value = node_max(right_subtree_of_root);
  Column *left_max_value = node_max(left_subtree_of_root);
  int index_in_root = binary_search(root->columns, root->size, left_max_value);

  BNode *left = root;
  BNode *right = generateRight(btree, left, left_max_value, index_in_root);
  if (right == NULL)
    return 0;
  if (debug())
  {
    printf("  分裂为两棵子树，左子树 ");
    print_node_data(left);
    printf("，右子树 ");
    print_node_data(right);
    printf("\n");
  }
  //generateRight没有处理left_subtree_of_root的子树，下面处理一下
  int middle_index = btree->degree;
  if (index_in_root >= middle_index)
  {
    //column的子树将位于右子树
    if (debug())
    {
      print_node_data(left_subtree_of_root);
      printf(" 将位于右子树 ");
      print_node_data(right);
      printf("\n");
    }
    right->children[index_in_root - middle_index] = left_subtree_of_root;
    left_subtree_of_root->parent = right;
    //由于 right_subtree_of_root 在 left_subtree_of_root 的右边，所以 right_subtree_of_root 也一定在右子树
    //且 left_subtree_of_root 的右边就是 right_subtree_of_root
    right->children[index_in_root - middle_index + 1] = right_subtree_of_root;
    right_subtree_of_root->parent = right;
    if (debug())
    {
      print_node_data(right_subtree_of_root);
      printf(" 将位于右子树 ");
      print_node_data(right);
      printf("\n");
    }
  }
  else
  {
    if (debug())
    {
      print_node_data(left_subtree_of_root);
      printf(" 将位于左子树 ");
      print_node_data(left);
      printf("\n");
    }
    //column的子树将位于左子树
    left->children[index_in_root] = left_subtree_of_root;
    left_subtree_of_root->parent = left;
    //由于 left_subtree_of_root 的右边就是 right_subtree_of_root
    //判断 index_in_root 是否超过 left->size-1 就可以知道 right_subtree_of_root 在 left 还是 right 的 0 号位
    if (index_in_root >= left->size - 1)
    {
      //right_subtree_of_root 将位于右子树
      right->children[0] = right_subtree_of_root;
      right_subtree_of_root->parent = right;
      if (debug())
      {
        print_node_data(right_subtree_of_root);
        printf(" 将位于右子树 ");
        print_node_data(right);
        printf("\n");
      }
    }
    else
    {
      //right_subtree_of_root 将位于左子树
      left->children[index_in_root + 1] = right_subtree_of_root;
      right_subtree_of_root->parent = left;
      if (debug())
      {
        print_node_data(right_subtree_of_root);
        printf(" 将位于左子树 ");
        print_node_data(left);
        printf("\n");
      }
    }
  }

  if (root->parent == NULL)
  {
    if (debug())
    {

      printf("当前分割结点是根结点\n");
    }
    //1. 当前结点是根结点
    BNode *parent = new_node(btree);
    if (!parent)
      return 0;
    parent->size = 2;
    parent->children[0] = left;
    parent->children[1] = right;
    parent->columns[0] = node_max(left);
    parent->columns[1] = node_max(right);
    parent->leaf = 0;
    left->parent = parent;
    right->parent = parent;
    parent->size = 2;

    btree->root = parent;
    btree->size += 2;
    return 1;
  }
  else if (node_is_full(btree, root->parent))
  {
    if (debug())
    {
      printf("当前分割结点不是根结点，但父结点是满结点\n");
    }
    //2. 当前结点不是根结点，但父结点是满结点
    return split_middle_or_root_and_add_subtree(btree, root->parent, left, right);
  }
  else
  {
    //3. 当前结点不是根结点，且父结点不是满结点
    if (debug())
    {
      printf("当前分割结点不是根结点，且父结点不是满结点\n");
    }
    BNode *parent = root->parent;
    int right_index_in_parent = binary_search(parent->columns, parent->size, node_max(right));
    for (i = parent->size; i > right_index_in_parent; i--)
    {
      parent->columns[i] = parent->columns[i - 1];
      parent->children[i] = parent->children[i - 1];
    }
    parent->columns[right_index_in_parent] = node_max(left);
    parent->children[right_index_in_parent + 1] = right;
    parent->size++;
    right->parent = parent;
    btree->size += 2;
    return 1;
  }
}
//将column添加为root的第index个数据
//（外部调用时保证）当前结点是满的叶子且必有父结点（无父结点的叶子结点视为根结点的情况，不在这里处理）
//（外部调用时保证）root->leaf == 1 && root->parent != NULL && root->size == 2 * btree->degree - 1
//添加完后，提交新结点到父结点
int split_leaf_and_add_node_to_index(BTree *btree, BNode *root, Column *column, int index)
{
  //将column插入到当前结点，会因为分裂而产生两个子树：左子树和右子树
  //因为外部调用保证了root是叶子结点
  //所以这里不处理root的子树在left到right的转移，只处理数据在left到right的转移
  //1. 先创建一个右子树，当前节点为左子树
  BNode *left = root;
  BNode *right = generateRight(btree, left, column, index);
  if (!right)
    return 0;
  if (debug())
  {
    printf("  分裂为两棵子树，左子树 ");
    print_node_data(left);
    printf("，右子树 ");
    print_node_data(right);
    printf("\n");
  }
  //2.将生成的两棵子树提交给父结点
  //外部调用保证了当前结点必有父结点
  //2.1 父结点也满，递归分裂
  //父结点可能是根结点，也可能是有父结点的中间结点
  BNode *parent = left->parent;
  if (node_is_full(btree, parent))
  {
    if (debug())
    {
      printf("父结点 ");
      print_node_data(parent);
      printf(" 也满，递归分裂\n");
    }
    btree->size += 2;
    return split_middle_or_root_and_add_subtree(btree, parent, left, right);
  }
  //2.2 父结点没满，直接提交结点到父结点并修改连接
  right->parent = parent;
  int right_index_in_parent = binary_search(parent->columns, parent->size, node_max(right)); //右子树在parent中的位置
  int i;
  for (i = parent->size; i > right_index_in_parent; --i)
  {
    parent->columns[i] = parent->columns[i - 1];
    parent->children[i] = parent->children[i - 1];
  }
  parent->columns[right_index_in_parent] = node_max(left);
  parent->children[right_index_in_parent + 1] = right;
  parent->size++;
  btree->size += 2;
  return 1;
}

//将column添加为root的第index个数据
//（外部调用时保证）当前结点为根结点且是满的 root->parent == NULL && root->size == 2 * btree->degree - 1
//新建一个根节点
int split_root_and_add_node_to_index(BTree *btree, BNode *root, Column *column, int index)
{
  if (debug())
  {
    printf("创建一个父结点\n");
  }
  BNode *left = root;
  BNode *parent = new_node(btree);
  if (!parent)
    return 0;
  parent->size = 1;
  parent->children[0] = left;
  Column *left_max = node_max(left);
  if (column_a_greater_or_equal_b(left_max, column))
  {
    parent->columns[0] = left_max;
  }
  else
  {
    parent->columns[0] = column;
  }
  parent->leaf = 0;

  left->parent = parent;

  btree->root = parent;
  btree->size++;
  //以上执行完，当前结点就有父结点了，按有父结点的情况进行处理
  return split_leaf_and_add_node_to_index(btree, root, column, index);
}

//（外部调用时保证）当前结点是满的叶子 root->leaf && root->size == 2 * btree->degree - 1
//将column添加为root的第index个数据
//然后分裂当前结点
//分裂完后，如果父结点也满了，继续分裂下去
//直到当前结点为根结点，此时新建一个根节点，结束分裂的递归
int split_and_add_node_to_index(BTree *btree, BNode *root, Column *column, int index)
{
  if (root->parent == NULL)
  {
    if (debug())
    {
      printf("分裂既是叶子也是根的结点\n");
    }
    return split_root_and_add_node_to_index(btree, root, column, index);
  }
  if (debug())
  {
    printf("分裂有父结点的结点\n");
  }
  return split_leaf_and_add_node_to_index(btree, root, column, index);
}

//（外部调用时保证）将数据添加到叶子
//将column添加为root的第index个数据
//可能需要处理分裂的情况
int add_node_to_leaf(BTree *btree, BNode *root, Column *column, int index)
{
  int i;
  if (index < root->size && column_is_equal(root->columns[index], column))
  {
    if (debug())
    {
      printf("已经存在该数据了，直接覆盖数据内容而不是另外分配空间\n");
      printf("%s == %s\n", root->columns[index]->title, column->title);
    }
    //已经存在该数据了，直接覆盖数据内容而不是另外分配空间
    strcpy(root->columns[index]->title, column->title);
    return 2;
  }
  //这是新数据
  //root结点没有该数据，需要分配空间
  if (debug())
  {
    printf("新数据，需要分配空间\n");
  }
  if (root->size == 2 * btree->degree - 1)
  {
    if (debug())
    {
      printf("叶子满了\n");
    }
    if (index >= root->size && root->parent != NULL)
    {
      if (debug())
      {
        printf("插入后是最大的，需要递归修改父结点\n");
      }
      replace_max_of_intrenal_node(btree, root->parent, root->columns[index - 1], column);
    }
    //需要递归分裂
    return split_and_add_node_to_index(btree, root, column, index);
  }
  else
  {
    if (debug())
    {
      printf("叶子没满\n");
    }
    //将 index 右边的结点往右挪一位
    for (i = root->size; i > index; --i)
    {
      root->columns[i] = root->columns[i - 1];
    }
    //保存到 index
    save_data_to_node(root, index, column);
    btree->size++;
    if (index >= root->size - 1 && root->parent != NULL)
    {
      if (debug())
      {
        printf("插入后是最大的，需要递归修改父结点\n");
      }
      return replace_max_of_intrenal_node(btree, root->parent, root->columns[index - 1], column);
    }
    return 1;
  }
}

//在BTree的定义下，将数据column插入子树root中
//btree是上下文，不参与结构构建
//root一定非空
int add_node(BTree *btree, BNode *root, Column *column)
{
  if (root == NULL)
  {
    printf("树为空\n");
    return 0;
  }
  if (debug())
  {
    printf("树不为空 ");
    print_node(root);
  }
  //树不空时，先搜索到叶子，如果叶子满了，再递归分裂，直到一个非满的子树，插入到那个子树
  //二分法搜索最佳插入点
  int index = binary_search(root->columns, root->size, column);
  if (debug())
  {
    printf("二分法搜索最佳插入点, index=%d\n", index);
  }
  if (root->leaf)
  {
    if (debug())
    {
      printf("结点是叶子\n");
    }
    //root结点是叶子
    return add_node_to_leaf(btree, root, column, index);
  }
  else
  {
    if (debug())
    {
      printf("结点不是叶子\n");
    }
    if (index == root->size)
    {
      index--;
    }
    return add_node(btree, root->children[index], column);
  }
}

//将数据colum插入B+树中
int btree_add(BTree *btree, Column *column)
{
  if (btree == NULL || column == NULL)
    return 0;
  if (!btree->root)
  {
    if (debug())
      printf("树为空，将插入的结点当作根结点\n");
    BNode *root = new_node(btree);
    if (!root)
      return 0;
    if (debug())
      printf("保存到结点\n");
    save_data_to_node(root, 0, column);
    if (debug())
      printf("保存完成\n");
    root->leaf = 1;

    btree->root = root;
    btree->head = root;
    btree->size = 1;
    return 1;
  }
  if (debug())
  {
    printf("保存到结点\n");
  }
  return add_node(btree, btree->root, column);
}
int debug_clear()
{
  return 0;
}
// 释放空间
int clear_node(BNode *root)
{
  if (!root)
    return 0;
  int i;
  if (root->leaf)
  {
    if (debug_clear())
    {
      printf("---释放叶子---");
      print_node_data(root);
      printf("\n");
    }
    for (i = 0; i < root->size; ++i)
    {
      free(root->columns[i]);
    }
    free(root->columns);
    return 1;
  }
  if (debug_clear())
  {
    printf("//释放中间结点---");
    print_node_data(root);
    printf("\n");
  }

  for (i = 0; i < root->size; ++i)
  {
    clear_node(root->children[i]);
  }
  free(root->columns);
  free(root);
  if (debug_clear())
  {

    printf("\\\\释放中间结点结束---\n");
  }
  return 1;
}

int btree_clear(BTree *btree)
{
  if (btree == NULL)
    return 0;
  clear_node(btree->root);
  free(btree);
  return 1;
}
