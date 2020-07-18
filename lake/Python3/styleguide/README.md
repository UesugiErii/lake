根据 [Google 开源项目风格指南 (中文版)](https://zh-google-styleguide.readthedocs.io/en/latest/), 自己进行了浓缩 

## Python语言规范

### pylint

[如何使用 Pylint 来规范 Python 代码风格](https://www.ibm.com/developerworks/cn/linux/l-cn-pylint/index.html)

### 导入

import x

from x import y

from x import y as z

例如, 模块 sound.effects.echo 可以用如下方式导入:

```Python3
from sound.effects import echo
...
echo.EchoFilter(input, output, delay=0.7, atten=4)
```

### 异常

像这样触发异常: raise MyException("Error message") 或者 raise MyException . 不要使用两个参数的形式( raise MyException, "Error message" )或者过时的字符串异常( raise "Error message" ).

模块或包应该定义自己的特定域的异常基类, 这个基类应该从内建的Exception类继承. 模块的异常基类应该叫做”Error”.

```Python3
class Error(Exception):
    pass
```

    
永远不要使用 except: 语句来捕获所有异常, 也不要捕获 Exception 或者 StandardError , 除非你打算重新触发该异常, 或者你已经在当前线程的最外层(记得还是要打印一条错误消息). 在异常这方面, Python非常宽容, except: 真的会捕获包括Python语法错误在内的任何错误. 使用 except: 很容易隐藏真正的bug.

尽量减少try/except块中的代码量. try块的体积越大, 期望之外的异常就越容易被触发. 这种情况下, try/except块将隐藏真正的错误.

使用finally子句来执行那些无论try块中有没有异常都应该被执行的代码. 这对于清理资源常常很有用, 例如关闭文件.

当捕获异常时, 使用 as 而不要用逗号. 例如

```Python3
try:
    raise Error
except Error as error:
    pass
```   
    
### 全局变量

避免使用全局变量, 用类变量来代替. 但也有一些例外:

1.脚本的默认选项.

2.模块级常量. 例如:　PI = 3.14159. 常量应该全大写, 用下划线连接.

3.有时候用全局变量来缓存值或者作为函数返回值很有用.

4.如果需要, 全局变量应该仅在模块内部可用, 并通过模块级的公共函数来访问.

### 嵌套/局部/内部类或函数

推荐使用

优点:允许定义仅用于有效范围的工具类和函数.
    
缺点:嵌套类或局部类的实例不能序列化(pickled).

**缺点我自己试了一下是可以的, 见test_pickle.py**

### 列表推导(List Comprehensions)

适用于简单情况. 每个部分应该单独置于一行: 映射表达式, for语句, 过滤器表达式. 禁止多重for语句或过滤器表达式. 复杂情况下还是使用循环.

```Python3
Yes:
  result = []
  for x in range(10):
      for y in range(5):
          if x * y > 10:
              result.append((x, y))

  for x in xrange(5):
      for y in xrange(5):
          if x != y:
              for z in xrange(5):
                  if y != z:
                      yield (x, y, z)

  return ((x, complicated_transform(x))
          for x in long_generator_function(parameter)
          if x is not None)

  squares = [x * x for x in range(10)]

  eat(jelly_bean for jelly_bean in jelly_beans
      if jelly_bean.color == 'black')
```

```Python3
No:
  result = [(x, y) for x in range(10) for y in range(5) if x * y > 10]

  return ((x, y, z)
          for x in xrange(5)
          for y in xrange(5)
          if x != y
          for z in xrange(5)
          if y != z)
```

### 默认迭代器和操作符

能用就用

```Python3
Yes:  for key in adict: ...
      if key not in adict: ...
      if obj in alist: ...
      for line in afile: ...
      for k, v in dict.iteritems(): ...
```

```Python3
No:   for key in adict.keys(): ...
      if not adict.has_key(key): ...
      for line in afile.readlines(): ...
```

### 生成器

鼓励使用, 简化代码, 使用的内存更少

### Lambda函数

适用于单行函数. 如果代码超过60-80个字符, 最好还是定义成常规(嵌套)函数.

### 条件表达式

例如: `x = 1 if cond else 2`

适用于单行函数. 在其他情况下，推荐使用完整的if语句.

### 默认参数值

鼓励使用

不要在函数或方法定义中使用可变对象作为默认值.

默认参数只在模块加载时求值一次. 如果参数是列表或字典之类的可变类型, 这可能会导致问题. 如果函数修改了对象(例如向列表追加项), 默认值就被修改了.

```Python3
Yes: def foo(a, b=None):
         if b is None:
             b = []
```

```Python3
No:  def foo(a, b=[]):
         ...
No:  def foo(a, b=time.time()):  # The time the module was loaded???
         ...
No:  def foo(a, b=FLAGS.my_thing):  # sys.argv has not yet been parsed...
         ...
```

### 属性(properties)

```Python3
class Student():
    def __init__(self):
        self._birth = 2000

    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        if value > 1800:
            self._birth = value
        else:
            print('impossible')

    @property
    def age(self):
        return 2020 - self._birth
```

`age`是只读的, 因为没有setter方法. `birth`可读可写

### True/False的求值

尽可能使用隐式的false, 例如: 使用 if foo: 而不是 if foo != []: . 不过还是有一些注意事项需要你铭记在心:

1.永远不要用==或者!=来比较单件, 比如None. 使用is或者is not.

2.注意: 当你写下 if x: 时, 你其实表示的是 if x is not None . 例如: 当你要测试一个默认值是None的变量或参数是否被设为其它值. 这个值在布尔语义下可能是false!

3.永远不要用==将一个布尔量与false相比较. 使用 if not x: 代替. 如果你需要区分false和None, 你应该用像 if not x and x is not None: 这样的语句.

4.对于序列(字符串, 列表, 元组), 要注意空序列是false. 因此 if not seq: 或者 if seq: 比 if len(seq): 或 if not len(seq): 要更好.

5.处理整数时, 使用隐式false可能会得不偿失(即不小心将None当做0来处理). 你可以将一个已知是整型(且不是len()的返回结果)的值与0比较.

6.注意‘0’(字符串)会被当做true.

```Python3
Yes: if not users:
         print 'no users'

     if foo == 0:
         self.handle_zero()

     if i % 10 == 0:
         self.handle_multiple_of_ten()
```

```Python3
No:  if len(users) == 0:
         print 'no users'

     if foo is not None and not foo:
         self.handle_zero()

     if not i % 10:
         self.handle_multiple_of_ten()
```

### 过时的语言特性

用新的方式

```Python3
Yes: words = foo.split(':')

     [x[1] for x in my_list if x[2] == 5]

     map(math.sqrt, data)    # Ok. No inlined lambda expression.

     fn(*args, **kwargs)
```

```Python3
No:  words = string.split(foo, ':')

     map(lambda x: x[1], filter(lambda x: x[2] == 5, my_list))

     apply(fn, args, kwargs)
```

### 词法作用域(Lexical Scoping)

嵌套的Python函数可以引用外层函数中定义的变量, 但是不能够对它们赋值

对一个块中的某个名称的任何赋值都会导致Python将对该名称的全部引用当做局部变量, 甚至是赋值前的处理

如果碰到global声明, 该名称就会被视作全局变量

```Python3
i = 4
def foo(x):
    def bar():
        print i,
    # ...
    # A bunch of code here
    # ...
    for i in x:  # Ah, i *is* local to Foo, so this is what Bar sees
        print i,
    bar()
```

`foo([1, 2, 3])` 会打印 `1 2 3 3` , 不是 `1 2 3 4`

解释, x是一个列表, for循环其实是将x中的值依次赋给i.这样对i的赋值就隐式的发生了, 整个foo函数体中的i都会被当做局部变量, 包括bar()中的那个

### 函数与方法装饰器

这里不谈, 有兴趣自己看原文

### 线程

不要依赖内建类型的原子性

尽量使用专用库

### 威力过大的特性

在你的代码中避免这些特性

诸如元类(metaclasses), 字节码访问, 任意编译(on-the-fly compilation), 动态继承, 对象父类重定义(object reparenting), 导入黑客(import hacks), 反射, 系统内修改(modification of system internals), 等等.

## Python风格规范

### 分号, 行长度, 括号

pycharm有提示

### 缩进, 空行, 空格

ctrl+alt+l

### Shebang

大部分.py文件不必以#!作为文件的开始. 根据 PEP-394 , 程序的main文件应该以 #!/usr/bin/python2或者 #!/usr/bin/python3开始

在计算机科学中, Shebang (也称为Hashbang)是一个由井号和叹号构成的字符串行(#!), 其出现在文本文件的第一行的前两个字符. 在文件中存在Shebang的情况下, 类Unix操作系统的程序载入器会分析Shebang后的内容, 将这些内容作为解释器指令, 并调用该指令, 并将载有Shebang的文件路径作为该解释器的参数. 例如, 以指令#!/bin/sh开头的文件在执行时会实际调用/bin/sh程序

\#!先用于帮助内核找到Python解释器, 但是在导入模块时, 将会被忽略. 因此只有被直接执行的文件中才有必要加入#!

### 注释

#### 文档字符串

三重双引号”“”, 首先是一行概述, 接着是一个空行. 接着是文档字符串剩下的部分, 它应该与文档字符串的第一行的第一个引号对齐

#### 模块

每个文件应该包含一个许可样板. 根据项目使用的许可(例如, Apache 2.0, BSD, LGPL, GPL), 选择合适的样板.

#### 函数和方法

文档字符串应该包含函数做什么, 以及输入和输出的详细描述. 通常, 不应该描述”怎么做”, 除非是一些复杂的算法.

关于函数的几个方面应该在特定的小节中进行描述记录, 这几个方面如下文所述. 每节应该以一个标题行开始. 标题行以冒号结尾. 除标题行外, 节的其他内容应被缩进2个空格.

##### Args

列出每个参数的名字, 并在名字后使用一个冒号和一个空格, 分隔对该参数的描述.如果描述太长超过了单行80字符,使用2或者4个空格的悬挂缩进(与文件其他部分保持一致). 描述应该包括所需的类型和含义. 如果一个函数接受*foo(可变长度参数列表)或者**bar (任意关键字参数), 应该详细列出*foo和**bar.

##### Returns: (或者 Yields: 用于生成器)

描述返回值的类型和语义. 如果函数返回None, 这一部分可以省略.

##### Raises

列出与接口有关的所有异常.

##### 举例

```Python3
def fetch_bigtable_rows(big_table, keys, other_silly_variable=None):
    """Fetches rows from a Bigtable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by big_table.  Silly things may happen if
    other_silly_variable is not None.

    Args:
        big_table: An open Bigtable Table instance.
        keys: A sequence of strings representing the key of each table row
            to fetch.
        other_silly_variable: Another optional variable, that has a much
            longer name than the other args, and which does nothing.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {'Serak': ('Rigel VII', 'Preparer'),
         'Zim': ('Irk', 'Invader'),
         'Lrrr': ('Omicron Persei 8', 'Emperor')}

        If a key from the keys argument is missing from the dictionary,
        then that row was not found in the table.

    Raises:
        IOError: An error occurred accessing the bigtable.Table object.
    """
    pass
```

#### 类

类应该在其定义下有一个用于描述该类的文档字符串. 如果你的类有公共属性(Attributes), 那么文档中应该有一个属性(Attributes)段. 并且应该遵守和函数参数相同的格式.

##### 举例

```Python3
class SampleClass(object):
    """Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, likes_spam=False):
        """Inits SampleClass with blah."""
        self.likes_spam = likes_spam
        self.eggs = 0

    def public_method(self):
        """Performs operation blah."""
```

#### 块注释和行注释

最需要写注释的是代码中那些技巧性的部分. 如果你在下次[代码审查](https://zh.wikipedia.org/wiki/%E4%BB%A3%E7%A0%81%E5%AE%A1%E6%9F%A5 )的时候必须解释一下, 那么你应该现在就给它写注释. 对于复杂的操作, 应该在其操作开始前写上若干行注释. 对于不是一目了然的代码, 应在其行尾添加注释.

```Python3
# We use a weighted dictionary search to find out where i is in
# the array.  We extrapolate position based on the largest num
# in the array and the array size and then do binary search to
# get the exact number.

if i & (i-1) == 0:        # True if i is 0 or a power of 2.
```

为了提高可读性, 注释应该至少离开代码2个空格(pycharm有提示, 可直接使用ctrl+alt+l).

另一方面, 绝不要描述代码. 假设阅读代码的人比你更懂Python, 他只是不知道你的代码要做什么.

```Python3
# BAD COMMENT: 遍历b数组确保i的下一个元素是i+1
```

### 类

存疑, Python3已经不用object了

### 字符串

```Python3
Yes: x = a + b
     x = '%s, %s!' % (imperative, expletive)
     x = '{}, {}!'.format(imperative, expletive)
     x = 'name: %s; score: %d' % (name, n)
     x = 'name: {}; score: {}'.format(name, n)
```

```Python3
No: x = '%s%s' % (a, b)  # use + in this case
    x = '{}{}'.format(a, b)  # use + in this case
    x = imperative + ', ' + expletive + '!'
    x = 'name: ' + name + '; score: ' + str(n)
```

避免在循环中用+和+=操作符来累加字符串. 由于字符串是不可变的, 这样做会创建不必要的临时对象, 并且导致二次方而不是线性的运行时间. 作为替代方案, 你可以将每个子串加入列表, 然后在循环结束后用 .join 连接列表

在同一个文件中, 保持使用字符串引号的一致性

为多行字符串使用三重双引号”“”而非三重单引号’‘’. 当且仅当项目中使用单引号’来引用字符串时, 才可能会使用三重’‘’为非文档字符串的多行字符串来标识引用. 文档字符串必须使用三重双引号”“”. 不过要注意, 通常用隐式行连接更清晰, 因为多行字符串与程序其他部分的缩进方式不一致.

### 文件和sockets

推荐使用 “with”语句

```Python3
with open("hello.txt") as hello_file:
    for line in hello_file:
        print(line)
```

对于不支持使用”with”语句的类似文件的对象,使用 contextlib.closing():

```Python3
import contextlib
with contextlib.closing(urllib.urlopen("http://www.python.org/")) as front_page:
    for line in front_page:
        print(line)
```

### TODO注释

开头处包含”TODO”字符串, 紧跟着是用括号括起来的你的名字, email地址或其它标识符. 然后是一个可选的冒号. 接着必须有一行注释, 解释要做什么

```Python3
# TODO(kl@gmail.com): Use a "*" here for string repetition.
# TODO(Zeke) Change this to use relations.
```

如果你的TODO是”将来做某事”的形式, 那么请确保你包含了一个指定的日期(“2009年11月解决”)或者一个特定的事件(“等到所有的客户都可以处理XML请求就移除这些代码”)

### 导入格式

每个导入应该独占一行, pycharm有提示

导入总应该放在文件顶部, 位于模块注释和文档字符串之后, 模块全局变量和常量之前. 导入应该按照从最通用到最不通用的顺序分组:

1.标准库导入

2.第三方库导入

3.应用程序指定导入

每种分组中, 应该根据每个模块的完整包路径按字典序排序, 忽略大小写.

```Python3
import foo
from foo import bar
from foo.bar import baz
from foo.bar import Quux
from Foob import ar
```

### 语句

通常每个语句应该独占一行

不过, 如果测试结果与测试语句在一行放得下, 你也可以将它们放在同一行. 如果是if语句, 只有在没有else时才能这样做. 特别地, 绝不要对 try/except 这样做, 因为try和except不能放在同一行.

### 访问控制

在Python中, 对于琐碎又不太重要的访问函数, 你应该直接使用公有变量来取代它们, 这样可以避免额外的函数调用开销. 当添加更多功能时, 你可以用属性(property)来保持语法的一致性.

(译者注: 重视封装的面向对象程序员看到这个可能会很反感, 因为他们一直被教育: 所有成员变量都必须是私有的! 其实, 那真的是有点麻烦啊. 试着去接受Pythonic哲学吧)

另一方面, 如果访问更复杂, 或者变量的访问开销很显著, 那么你应该使用像 get_foo() 和 set_foo() 这样的函数调用. 如果之前的代码行为允许通过属性(property)访问 , 那么就不要将新的访问函数与属性绑定. 这样, 任何试图通过老方法访问变量的代码就没法运行, 使用者也就会意识到复杂性发生了变化.

### 命名

`module_name, package_name, ClassName, method_name, ExceptionName, function_name, GLOBAL_VAR_NAME, instance_var_name, function_parameter_name, local_var_name`

#### 应该避免的名称

1.单字符名称, 除了计数器和迭代器.

2.包/模块名中的连字符(-)

3.双下划线开头并结尾的名称(Python保留, 例如__init__)

#### 命名约定

1.所谓”内部(Internal)”表示仅模块内可用, 或者, 在类内是保护或私有的.

2.用单下划线(_)开头表示模块变量或函数是protected的(使用from module import *时不会包含).

3.用双下划线(__)开头的实例变量或方法表示类内私有.

4.将相关的类和顶级函数放在同一个模块里. 不像Java, 没必要限制一个类一个模块.

5.对类名使用大写字母开头的单词(如CapWords, 即Pascal风格), 但是模块名应该用小写加下划线的方式(如lower_with_under.py). 尽管已经有很多现存的模块使用类似于CapWords.py这样的命名, 但现在已经不鼓励这样做, 因为如果模块名碰巧和类名一致, 这会让人困扰.

### Main

`if __name__ == '__main__'`, 这样当模块被导入时主程序就不会被执行.