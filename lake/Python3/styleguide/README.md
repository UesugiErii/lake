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

`age`是只读的,因为没有setter方法. `birth`可读可写

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

