#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "btree.h"

#define N 1800               // 哈希表大小
#define SPLIT 10             // 哈希成 7 个小的对应文件
#define MAX_STRING_LENGTH 45 // 最大字符串长度
#define FILE_LINE_BUFFER 128 // 读取一行的buffer

char *line;
int key = -1;
char *itoa(int num, char *str, int radix)
{
  char index[] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"; //索引表
  unsigned unum;                                         //存放要转换的整数的绝对值,转换的整数可能是负数
  int i = 0, j, k;                                       //i用来指示设置字符串相应位，转换之后i其实就是字符串的长度；转换后顺序是逆序的，有正负的情况，k用来指示调整顺序的开始位置;j用来指示调整顺序时的交换。

  //获取要转换的整数的绝对值
  if (radix == 10 && num < 0) //要转换成十进制数并且是负数
  {
    unum = (unsigned)-num; //将num的绝对值赋给unum
    str[i++] = '-';        //在字符串最前面设置为'-'号，并且索引加1
  }
  else
    unum = (unsigned)num; //若是num为正，直接赋值给unum

  //转换部分，注意转换后是逆序的
  do
  {
    str[i++] = index[unum % (unsigned)radix]; //取unum的最后一位，并设置为str对应位，指示索引加1
    unum /= radix;                            //unum去掉最后一位

  } while (unum); //直至unum为0退出循环

  str[i] = '\0'; //在字符串最后添加'\0'字符，c语言字符串以'\0'结束。

  //将顺序调整过来
  if (str[0] == '-')
    k = 1; //如果是负数，符号不用调整，从符号后面开始调整
  else
    k = 0; //不是负数，全部都要调整

  char temp;                         //临时变量，交换两个值时用到
  for (j = k; j <= (i - 1) / 2; j++) //头尾一一对称交换，i其实就是字符串的长度，索引最大值比长度少1
  {
    temp = str[j];               //头部赋值给临时变量
    str[j] = str[i - 1 + k - j]; //尾部赋值给头部
    str[i - 1 + k - j] = temp;   //将临时变量的值(其实就是之前的头部值)赋给尾部
  }

  return str; //返回转换后的字符串
}

// ELF Hash Function
unsigned int ELFHash(char *str)
{
  unsigned int hash = 0;
  unsigned int x = 0;

  while (*str)
  {
    hash = (hash << 4) + (*str++);
    if ((x = hash & 0xF0000000L) != 0)
    {
      hash ^= (x >> 24);
      hash &= ~x;
    }
  }

  return (hash & 0x7FFFFFFF);
}

unsigned int hash(char *str)
{
  return ELFHash(str);
}

/**
 * dictFile: 字典文件
 * wordFile: 待搜索文件
 * resultFile: 结果输出
 * m : m阶B+树
 */
int search(FILE *dictFile, FILE *wordFile, FILE *resultFile, int m)
{
  //构建哈希字典
  int k = (m + 1) / 2;
  printf("building B+ tree, m=%d, k=%d\n", m, k);
  BTree *btree = btree_init(k);
  while (fgets(line, FILE_LINE_BUFFER, dictFile) != NULL)
  {
    char *find = strchr(line, '\n'); //查找换行符，如果find不为空指针
    if (find)
      *find = '\0';
    if (strlen(line) == 0)
      continue;
    Column *c = (Column *)malloc(sizeof(Column));
    c->id = 0;
    strcpy(c->title, line);
    // printf("%s\n", line);
    btree_add(btree, c);
  }
  printf("B+树(nodes:%d leaf=%d)\n", btree_node_count(btree), btree_leaf_count(btree));
  //搜索
  int hit = 0;
  while (fgets(line, FILE_LINE_BUFFER, wordFile) != NULL)
  {
    char *find = strchr(line, '\n'); //查找换行符，如果find不为空指针
    if (find)
      *find = '\0';
    if (line[0] == '\n' || line[0] == '\0')
    {
      printf("skip an empty line\n");
      continue;
    }
    Column c;
    c.id = 1;
    strcpy(c.title, line);
    Column *result = btree_get_by_value(btree, &c);
    if (result != NULL)
    {
      fprintf(resultFile, "%s\n", line);
      hit++;
    }
  }
  fclose(wordFile);
  fclose(dictFile);
  printf("hit %d\n", hit);
  btree_clear(btree);
  return hit;
}

char *key2string(int key, char *suffix, char *buffer)
{
  char *keyString = itoa(key, buffer, 10);
  return strcat(keyString, suffix);
}

/*
dict.txt   词典串127万个
string.txt 待匹配的1.7万个字符串
result.txt 实验结果，所有查找到的串，一行一个

gcc bplus_search.c -o bplus_search.exe && ./bplus_search.exe dict.txt string.txt
*/
int main(int argc, char *argv[])
{
  // freopen("Bplus_Tree.log", "w", stdout);
  char *dictFilename = "dict.txt";
  char *wordFilename = "string.txt";
  int m = 5;

  // 命令行参数处理
  if (argc != 3)
  {
    printf("you can call me like this: \n\n    bplus_search m dict.txt string.txt\n\n");
  }
  else
  {
    m = atoi(argv[1]);
    dictFilename = argv[2];
    wordFilename = argv[3];
  }
  printf("dict: %s, word: %s\n", dictFilename, wordFilename);

  // 统计运行时间
  clock_t start_t = clock();
  printf("--- start\n");
  int i = 0;
  line = (char *)malloc(FILE_LINE_BUFFER * sizeof(char)); // 读取一行字符串的 buffer
  // 哈希成小的文件对
  char filenameBuffer[12] = {0};
  FILE *file = NULL, *dictOutput[SPLIT], *wordOutput[SPLIT];
  for (i = 0; i < SPLIT; i++)
  {
    dictOutput[i] = NULL;
    wordOutput[i] = NULL;
  }
  //构建哈希字典
  if ((file = fopen(dictFilename, "r")) == NULL)
  {
    printf("fail to open file %s\n", dictFilename);
    return 0;
  }
  printf("open %s\n", dictFilename);
  while (fgets(line, 63, file) != NULL)
  {
    char *find = strchr(line, '\n'); //查找换行符
    if (find)                        //如果find不为空指针
      *find = '\0';                  //就把一个空字符放在这里
    key = abs(hash(line) % SPLIT);
    if (dictOutput[key] == NULL)
    {
      char *targetFilename = key2string(key, "_dict.txt", filenameBuffer);
      // printf("open %s\n", targetFilename);
      if ((dictOutput[key] = fopen(targetFilename, "w+")) == NULL)
      {
        printf("fail to open file %s\n", targetFilename);
        return 0;
      }
    }
    fprintf(dictOutput[key], "%s\n", line);
  }
  fclose(file);

  if ((file = fopen(wordFilename, "r")) == NULL)
  {
    printf("fail to open file %s\n", wordFilename);
    return 0;
  }
  printf("open %s\n", wordFilename);
  while (fgets(line, 63, file) != NULL)
  {
    char *find = strchr(line, '\n'); //查找换行符，如果find不为空指针
    if (find)
      *find = '\0';
    key = abs(hash(line) % SPLIT);
    if (wordOutput[key] == NULL)
    {
      char *targetFilename = key2string(key, "_string.txt", filenameBuffer);
      // printf("open %s\n", targetFilename);
      if ((wordOutput[key] = fopen(targetFilename, "w+")) == NULL)
      {
        printf("fail to open file %s\n", targetFilename);
        return 0;
      }
    }
    fprintf(wordOutput[key], "%s\n", line);
  }
  fclose(file);

  printf("--- split using time : %f s\n", (double)((double)(clock() - start_t) / (double)(CLOCKS_PER_SEC)));

  // 生成结果
  FILE *resultFile = NULL;
  if ((resultFile = fopen("bupt_14.txt", "w+")) == NULL)
  {
    printf("fail to open file result.txt\n");
    return 0;
  }
  printf("open result.txt\n");
  int total_hits = 0;
  for (i = 0; i < SPLIT; i++)
  {
    FILE *dictFile = dictOutput[i];
    FILE *wordFile = wordOutput[i];
    rewind(dictFile);
    rewind(wordFile);
    int k = (m + 1) / 2;
  printf("building B+ tree, m=%d, k=%d\n", m, k);
  BTree *btree = btree_init(k);
  while (fgets(line, FILE_LINE_BUFFER, dictFile) != NULL)
  {
    char *find = strchr(line, '\n'); //查找换行符，如果find不为空指针
    if (find)
      *find = '\0';
    if (strlen(line) == 0)
      continue;
    Column *c = (Column *)malloc(sizeof(Column));
    c->id = 0;
    strcpy(c->title, line);
    // printf("%s\n", line);
    btree_add(btree, c);
  }
  printf("B+树(nodes:%d leaf=%d)\n", btree_node_count(btree), btree_leaf_count(btree));
  //搜索
  int hit = 0;
  while (fgets(line, FILE_LINE_BUFFER, wordFile) != NULL)
  {
    char *find = strchr(line, '\n'); //查找换行符，如果find不为空指针
    if (find)
      *find = '\0';
    if (line[0] == '\n' || line[0] == '\0')
    {
      printf("skip an empty line\n");
      continue;
    }
    Column c;
    c.id = 1;
    strcpy(c.title, line);
    Column *result = btree_get_by_value(btree, &c);
    if (result != NULL)
    {
      fprintf(resultFile, "%s\n", line);
      hit++;
    }
  }
  fclose(wordFile);
  fclose(dictFile);
  printf("hit %d\n", hit);
  // break;
  btree_clear(btree);
    total_hits += hit;//search(dictFile, wordFile, resultFile, m);
    remove(key2string(i, "_dict.txt", filenameBuffer));
    remove(key2string(i, "_string.txt", filenameBuffer));
  }
  printf("total hits: %d\n", total_hits);
  fclose(resultFile);
  free(line);
  printf("runtime: %f s, string match: %d\n", (double)((double)(clock() - start_t) / (double)(CLOCKS_PER_SEC)), total_hits);
  printf("--- total using time : %f s\n", (double)((double)(clock() - start_t) / (double)(CLOCKS_PER_SEC)));
  // sleep(3);
  return 0;
}