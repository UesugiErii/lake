#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define N 1800
#define SPLIT 7

typedef struct node
{
  char data[45];
  int hash;
  struct node *next;
} Node;
char *line;
Node *hashtable[N], *p = NULL, *q = NULL;
int key = -1;
unsigned int SDBMHash(char *str)
{
  unsigned int hash = 0;

  while (*str)
  {
    // equivalent to: hash = 65599*hash + (*str++);
    hash = (*str++) + (hash << 6) + (hash << 16) - hash;
  }

  return (hash & 0x7FFFFFFF);
}

// RS Hash Function
unsigned int RSHash(char *str)
{
  unsigned int b = 378551;
  unsigned int a = 63689;
  unsigned int hash = 0;

  while (*str)
  {
    hash = hash * a + (*str++);
    a *= b;
  }

  return (hash & 0x7FFFFFFF);
}

// JS Hash Function
unsigned int JSHash(char *str)
{
  unsigned int hash = 1315423911;

  while (*str)
  {
    hash ^= ((hash << 5) + (*str++) + (hash >> 2));
  }

  return (hash & 0x7FFFFFFF);
}

// P. J. Weinberger Hash Function
unsigned int PJWHash(char *str)
{
  unsigned int BitsInUnignedInt = (unsigned int)(sizeof(unsigned int) * 8);
  unsigned int ThreeQuarters = (unsigned int)((BitsInUnignedInt * 3) / 4);
  unsigned int OneEighth = (unsigned int)(BitsInUnignedInt / 8);
  unsigned int HighBits = (unsigned int)(0xFFFFFFFF) << (BitsInUnignedInt - OneEighth);
  unsigned int hash = 0;
  unsigned int test = 0;

  while (*str)
  {
    hash = (hash << OneEighth) + (*str++);
    if ((test = hash & HighBits) != 0)
    {
      hash = ((hash ^ (test >> ThreeQuarters)) & (~HighBits));
    }
  }

  return (hash & 0x7FFFFFFF);
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

// BKDR Hash Function
unsigned int BKDRHash(char *str)
{
  unsigned int seed = 131; // 31 131 1313 13131 131313 etc..
  unsigned int hash = 0;

  while (*str)
  {
    hash = hash * seed + (*str++);
  }

  return (hash & 0x7FFFFFFF);
}

// DJB Hash Function
unsigned int DJBHash(char *str)
{
  unsigned int hash = 5381;

  while (*str)
  {
    hash += (hash << 5) + (*str++);
  }

  return (hash & 0x7FFFFFFF);
}

// AP Hash Function
unsigned int APHash(char *str)
{
  unsigned int hash = 0;
  int i;

  for (i = 0; *str; i++)
  {
    if ((i & 1) == 0)
    {
      hash ^= ((hash << 7) ^ (*str++) ^ (hash >> 3));
    }
    else
    {
      hash ^= (~((hash << 11) ^ (*str++) ^ (hash >> 5)));
    }
  }

  return (hash & 0x7FFFFFFF);
}
unsigned int hash(char *str)
{
  return ELFHash(str);
}

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

int search(FILE *dictFile, FILE *wordFile, FILE *resultFile)
{
  // printf("init\n");
  //构建哈希字典
  // printf("building hashtable\n");
  while (fgets(line, 63, dictFile) != NULL)
  {
    char *find = strchr(line, '\n'); //查找换行符
    if (find)                        //如果find不为空指针
      *find = '\0';                  //就把一个空字符放在这里
    key = abs(hash(line) % N);
    // p = hashtable[key];
    p = (Node *)malloc(sizeof(Node));
    if (p == NULL)
      return 0;
    strcpy(p->data, line);
    p->next = hashtable[key];
    p->hash = SDBMHash(line);
    hashtable[key] = p;
  }
  fclose(dictFile);
  //搜索
  // printf("searching\n");
  int hit = 0;
  while (fgets(line, 63, wordFile) != NULL)
  {
    char *find = strchr(line, '\n'); //查找换行符
    if (find)                        //如果find不为空指针
      *find = '\0';                  //就把一个空字符放在这里
    key = abs(hash(line) % N);
    p = hashtable[key];
    while (p != NULL)
    {
      if (strcmp(p->data, line) == 0)
      {
        if (line[0]=='\n'||line[0]=='\0')
        {
          printf("empty\n");
          break;
        }

        fprintf(resultFile, "%s\n", line);
        hit++;
        break;
      }
      p = p->next;
    }
  }
  fclose(wordFile);
  printf("hit %d\n", hit);
  // printf("closing\n");
  for (int i = 0; i < N; i++)
  {
    p = hashtable[i];
    hashtable[i] = NULL;
    q = p;
    while (p != NULL)
    {
      q = p->next;
      free(p);
      p = q;
    }
  }
  return hit + 1;
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
*/
int main()
{
  clock_t start_t;
  start_t = clock();
  printf("start\n");
  line = (char *)malloc(127 * sizeof(char)); // buffer
  for (int i = 0; i < N; i++)
    hashtable[i] = NULL;
  //split
  FILE *file = NULL, *dictOutput[SPLIT], *wordOutput[SPLIT];
  for (int i = 0; i < SPLIT; i++)
  {
    dictOutput[i] = NULL;
    wordOutput[i] = NULL;
  }
  if ((file = fopen("dict.txt", "r")) == NULL)
  {
    printf("fail to open file %s\n", "dict.txt");
    return 0;
  }
  printf("open %s\n", "dict.txt");
  //构建哈希字典
  char filenameBuffer[12] = {0};

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

  if ((file = fopen("string.txt", "r")) == NULL)
  {
    printf("fail to open file %s\n", "string.txt");
    return 0;
  }
  printf("open %s\n", "string.txt");
  while (fgets(line, 63, file) != NULL)
  {
    char *find = strchr(line, '\n'); //查找换行符
    if (find)                        //如果find不为空指针
      *find = '\0';                  //就把一个空字符放在这里
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

  printf("split using time : %f s\n", (double)((double)(clock() - start_t) / (double)(CLOCKS_PER_SEC)));
  FILE *resultFile = NULL;
  if ((resultFile = fopen("result.txt", "w+")) == NULL)
  {
    printf("fail to open file result.txt\n");
    return 0;
  }
  printf("open file result.txt\n");
  for (int i = 0; i < SPLIT; i++)
  {
    FILE *dictFile = dictOutput[i];
    FILE *wordFile = wordOutput[i];
    rewind(dictFile);
    rewind(wordFile);
    search(dictFile, wordFile, resultFile);
    remove(key2string(i, "_dict.txt", filenameBuffer));
    remove(key2string(i, "_string.txt", filenameBuffer));
  }
  fclose(resultFile);
  free(line);
  printf("search using time : %f s\n", (double)((double)(clock() - start_t) / (double)(CLOCKS_PER_SEC)));
  return 0;
}