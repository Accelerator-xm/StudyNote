# python 知识点补充
## 输入输出
### print()
- 输出对象：可以是多个
- 分隔符：默认空格，每个对象之间的分隔符
```python
print(1,2,3,4)      # 输出四个对象---1 2 3 4
print([ 1,2,3,4 ])  # 输出一个list对象---[ 1,2,3,4 ]
```
- 结尾符号：默认\n
- 输出文件：默认标准系统输出
- flush：默认false，是否缓存

### str.format() 格式化输出
str里的{}替换format()的参数
- 规律
    - {序号: 填充符 对齐方式 宽度 , .精度 类别}
        - 对齐方式：右对齐>，左对齐<，中间对齐^
        - ,  ：逗号分隔的数字格式，100,000,000
        - 精度：浮点数小数位数，字符串字符数
        - 类别:
            - d十进制
            - x十六进制
            - o八进制
            - b二进制
            - e/E浮点数指数形式
            - f/F浮点数标准形式
            - g/G浮点数最短表示
            - %
- 例子
    - 输出 "Tom,男,40"
    ```python
    # 按顺序
    print('{}，{}，{}'.format('Tom', '男', 40))
    # 按序号
    print('{2}，{1}，{0}'.format(40,'男','Tom'))
    # 按参数名
    -print('{name}，{gender}，{age}' .format(age=40, gender='男', name='Tom'))
    ```
    - :.mf  保留m位小数，默认补0，四舍五入（m>=0）
    - :.m%  百分数，数字部分保留m位小数
    - :.me  科学计数法，数字部分保留m位小数
    - :md   保留m位整数，默认补空格右对齐
    - :c>  右对齐补字符c，默认空格
    ```python
    print("{:x>5d}".format(5))  # "xxxx5"
    print("{:a<5d}".format(5))  # "5aaaa"
    print("{:b^5d}".format(5))  # "bb5bb"
    ```


### input() 读入一个字符串
- 字符串是严格数据可转换
    - int() 将字符串转换成整数 "50" -> 50
    - float() 将字符串转换成浮点数 "5.5" -> 5.5
    - eval() 将字符串当成表达式（单个数据也是表达式）计算 "5 + 5" -> 10
- 输入多个数据：m,n = map(int,input().split())

## 数值类型
### 数值类型
- 整数int
    - 前缀
        - 十进制：无
        - 二进制：0b或0B
        - 八进制：0o或0O
        - 十六进制：0x或0X
    - 符号：在前缀前（-0b0101表示-0101）
- 浮点数float
    - 精度
        - 默认float, 17位
        - decimal, 50位
- 布尔bool
    - True：值为1
    - False：值为0
- 复数complex
    - 虚部：j

### 数值类型转换
- int(对象[, base])：转十进制整数
    - 无参：0
    - 对象为浮点数、非十进制整数，base空：小数直接舍弃
    - 对象为字符串，base指定字符串为多少进制
- float(x)：将字符串转换成浮点数
    - 字符串：数值前后可以有空白符，可以是科学计数法，必须十进制

### 常用函数
- abs()
    - 整数、浮点数返回绝对值
    - 复数，返回它的模
- divmod(a, b)：返回元组(商, 余数) = (a//b, a%b)
- pow(x, y[, z])：x的y次方对z取余
- round(number[, n])：四舍五入
    - n：
        - 空：整数
        - n大于number的位数：直接返回number
        - n小于number位数：四舍五入
    - 5特殊考虑：向偶数舍入，保证最后一位为偶数，由于精度问题可能不能完全按这个规则
    ```python
    print(round(3.1415,3))  # 3.142
    print(round(3.24350,3)) # 3.244
    print(round(3.24450,3)) # 3.244
    ```
- max()：最大值
- min()：最小值
- eval()：计算表达式的值
```python
x=2
print(eval("x + 3"))    # 5
```
- random()随机数：
    - seed(a=None)：初始化随机种子, 让随机数生成是可重复的, 相同的种子生成的
    - random()：生成一个[0.0, 1.0)之间的随机小数
    - randint(a, b)：生成一个[a,b]之间的整数
    - choice(seq)：从序列类型(例如：列表、字符串)中随机返回一个元素
```python
import random
print(random.random())
print(random.randint(1, 10))    # 整数
print(random.uniform(1, 10))    # 小数
print(random.choice(range(10)))
```

## 控制流程
### 条件表达式
- a = x if 条件 else y
    - 条件真：a = x
    - 条件假：a = y

### for循环
- for 取值 in 序列或迭代器:
    - 序列或迭代器：
        - range(开始， 结束， 步长)
            - 范围：[开始，结束)
            - 开始默认0
            - 步长默认1
        - 文件：按行遍历
        - 字符串：按字符遍历
        - 列表：按元素遍历

### else
- else扩展：正常迭代结束才会执行else段
    - for、while相同
    - 非正常结束：break、return、异常终止
    - 正常结束：循环条件变为False退出
```python
# 正常结束：
for i in range(3):
    print(i)
else:
    print("循环正常结束")   # 正常输出

# 非正常结束
for i in range(3):
    if i == 1:
        break
    print(i)
else:
    print("循环正常结束")   # 不输出
```

## 函数
### 参数传递
- 位置传递：按顺序传递
- 关键词传递：参数名传递
- 默认值传递
    - 必须是不可变对象：数值、字符串、元组
    -  不能是可变对象：字典、列表、集合
- 包裹传递：定义函数时不确定有多少参数，可使用包裹传递
    - 参数名之前加 "*"：以元组形式传递值
    ```python
    def test1(*args):
        print(type(args))   # <class 'tuple'>
        print(args)         # (1, 2, 3, 4)
    
    test1(1,2,3,4)
    ```
    - 参数名之前加 "**"：以关键词形式传递值
    ```python
    def test2(**args):
        print(type(args))   # <class 'dict'>
        print(args)         # {'a': 1, 'b': 2, 'c': 2, 'd': 4}

    test2(a=1, b=2, c=2, d=4)
    ```

- 解包裹传递：函数规定好形参，但实际参数为元组或字典类型, 可以解除包裹
    - "*" 元组
    - "**" 字典
    ```python
    def test(a,b,c):
        print(a,b,c)

    t = (1,2,3)
    d = {'a':1, 'b':2, 'c':3}
    test(*t)    # "1 2 3"
    test(**d)   # "1 2 3"
    ```

### 变量作用域
- 局部变量：函数内定义
- 全局变量：函数外定义
    - 函数内使用全局变量用global关键字
    ```python
    n = 1

    def test1():
        n = 2

    def test2():
        global n
        n = 2
    
    test1()
    print(n)    # 1

    test2()
    print(n)    # 2
    ```

### 匿名函数
lambda 参数列表: 表达式
直接赋值给一个变量当函数用，可以传参

- 根据身份证号判断性别
```python
id = input()
gender = lambda id: "女" if int(id[-2])%2==0 else "男"
print(gender(id))
```

- 数组按绝对值排序
```python
ls = [-9, -10, 6, 3, 8]
print(sorted(ls, key=lambda x: abs(x)))
```

## 序列
### 通用序列操作
按照特定顺序排列的一组数据，每个元素都有自己的下标索引
序列类型包括：字符串str、列表list、元组tuple、range、二进制文本类型、生成器generator
- 索引：
    - 正数索引：从序列开头开始，按顺序从0依次编号
    - 负数索引，从序列结尾开始，从-1开始编号
- 切片：获取序列的一部分，生成一个新的序列
    - s[satrt: end: step]
    - 包含start，不包含end
    - start默认0，end默认序列长度，step默认1
    - 可以用负数索引
    - 正向切片：step为正数
    - 逆向切片：step为负数
```python
# 判断回文字符串
s = input()
if s == s[-1::-1]:
    print("True")
else:
    print("False")
```
- 序列相乘：序列*n = 生成新的序列，原序列重复n次
- 序列拼接：序列+序列 = 两个序列拼接
- 成员测试：
    - 是否存在：in
    - 是否不存在：not in
- 内置函数
    - len(): 序列长度
    - max(): 最大值
    - min(): 最小值
    - sorted(): 排序
    - sum(): 求和
    - reverse(): 翻转序列
    - list(): 序列转换成列表
    - str(): 序列转换成字符串
    - ord()：字符转ascii码
    - chr()：ascii码转字符
- 推导式: 通过一个数据序列构建另一个数据序列，列表推导式、字典推导式、集合推导式
    - [表达式 (for 元素 in 序列) if 条件]
        - 将所有符合条件的元素通过表达式转换成新的元素添加到新列表
        - 可以有多个for 元素 in 序列
        ```python
        ls1 = [1,2,3]
        ls2 = [1,3,4]
        ls = [(x,y) for x in ls1 for y in ls2 if x!=y]
        print(ls) # [(1, 3), (1, 4), (2, 1), (2, 3), (2, 4), (3, 1), (3, 4)]
        ```
- 生成器：一边循环一遍计算, 惰性求值
    - 概念：
        - 元素很多时列表占用的空间比较大，如果元素可以按照某算法循环推导出来，就不需要创建完整的列表
        - 生成器对象可以通过__next__()或next()进行编列，也可以当作迭代器对象使用
        - 所有元素访问结束后，生成器对象会变空，想要再次使用必须重新创建
        - 每个遍历过的元素都不在出现
        - 生成器对象不是列表或元组
        - range是惰性求值, 但不是生成器
    - 语法：把推导式最外层[]换成()
    ```python
    g = (i for i in range(10))
    for i in g:
        print(i, end=" ") # 0 1 2 3 4 5
        if i == 5:
            break
    print()
    print(list(g))  # [6, 7, 8, 9]
    print(list(g))  # []
    ```
    - map(f, list)
        - 让函数f作用于list的每一个元素，构成map生成器
    - zip(seq1[, seq2 ...])
        - 取出每个序列第i元素构成元组，作为新序列的第i元素
        - 最短的序列取完后终止
        - 构成zip生成器
        ```python
        ls1 = list(range(10))
        ls2 = list(range(3))
        z = zip(ls1, ls2)
        print(list(z))  # [(0, 0), (1, 1), (2, 2)]
        ```
    - enumerate(seq, start)
        - 为seq的每一个元素添加序号，从start开始计数，默认0开始
        ```python
        ls = ["1", "2", "3"]
        print(list(enumerate(ls, 0)))
        # [(0, '1'), (1, '2'), (2, '3')]
        ```

### 字符串str及其操作
- 字符串常量
    - 字符string.ascii_letters = abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    - 小写字符 string.ascii_lowercase = abcdefghijklmnopqrstuvwxyz
    - 大写字符 string.ascii_uppercase = ABCDEFGHIJKLMNOPQRSTUVWXYZ
    - 数字 string.digits = 0123456789
    - 十六进制字符 string.hexdigits = 0123456789abcdefABCDEF
    - 八进制字符 string.octdigits = 01234567
    - 标点符号字符 string.punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
- 字符串函数：
    - 查询：
        - find(str, start, end): 从左开始查找字符串位置,没找到返回-1。index用法相同，没找到报异常
        - rfind(str, start, end): 从右开始查找字符串位置。rindex同index
    - 大小写操作：
        - upper()：转大写
        - lowwr()：转小写
        - swapcase()：大小写交换
        - capitalize()：首字母大写，其余小写
        - title()：第一个单词首字母大写，其余小写
    - 对齐操作：
        - center(width, 填充字符)：中间对齐
        - ljust(width, 填充字符)：左对齐
        - rjust(width, 填充字符)：右对齐
        - zfill(width)：
    - 分割：
        - split(分隔符, n)：按照分隔符切割n次，即分n+1段，默认空格
        - rsplite：从右边开始
        - splitline：按行分割
        - partition：按照指定字符串分成三份
        - rpartition：从右边开始
        ```python
        s = "my name you name"
        print(s.partition("name")) # ('my ', 'name', ' you name')
        print(s.rpartition("name")) # ('my name you ', 'name', '')
        ```
    - 合并
        - join(序列)：原字符串作为分隔符，将序列拼接成字符串，元素必须是字符串
        ```python
        ls = ['a', 'b', 'c']
        print("---".join(ls)) # a---b---c
        ```
    - 替换
        - replace(old, new, max)：将字符串的old子串替换成new串，最大max次（默认不限次数）
    - 判断：
        - isidentifier：是否是标识符
        - islower：是否是小写
        - isupper：是否是大写
        - startswith：是否以给定字符串开头
        - endswith：是否以给定字符串结尾
    - 去除两端多余字符
        - strip(str)：去除两端**属于**str的字符， 默认空白字符
        - lstrip(str)：去除左边
        - rstrip(str)：去除右边
        ```python
        s = "aaacbcname"
        print(s.lstrip("abc")) # name
        ```
    - 计数
        - count(str, start, end)：记录[satrt, end)范围内str的个数
    
### 列表list及其操作
- 创建：
    - [元素1, ...]
    - list(序列)：将序列转换成列表
    - split()：将序列类型切分为列表，一般为字符串
- 更新：
    - 索引赋值：seq[i]
    - 切片赋值：
        - 连续切片: seq[i:j], 更新的数量可以不同
        ```python
        ls = [1,2,3,4,5,6]
        ls[1:3] = [7,8,9,10]
        print(ls)   # [1, 7, 8, 9, 10, 4, 5, 6]
        ```
        - 不连续切片: seq[i:j:k], 更新的数量必须相同
        ```python
        ls = [1,2,3,4,5,6]
        ls[0::2] = [7,8,9]
        print(ls)   # [7, 2, 8, 4, 9, 6]
        ```
    - append(元素): 末尾添加元素
    - extend(序列): 末尾添加序列
    - insert(i, 元素): 将元素插入位置i
- 删除:
    - pop(): 删除末尾元素
    - remove(元素): 删除第一个元素
    - clear(): 清空
- 排序: 
    - sort(key=None, reverse=False)
        - reverse=True: 翻转,默认升序翻转后为降序
        - key: 指定规则
    - reverse(): 逆序

### 元组
用()存放一组数据，可以通过索引访问
元组是不可变数据类型，不可以增删改元素
可以通过切片访问，但不能修改
- 创建：
    - (元素)
    ```python
    t1 = (1)
    t2 = (1,)
    print(t1)   # 1
    print(t2)   # (1,)
    if t1 == t2:
        print("True")
    else:
        print("False")  # False
    ```
    - 不用括号也行
    ```python
    t1 = 1,
    t2 = (1,)
    print(t1)   # (1,)
    print(t2)   # (1,)
    if t1 == t2:
        print("True")   # True
    else:
        print("False")
    ```
    - tuple(seq)
- 应用：
    - 函数包裹传递
    - 函数多个返回值
    ```python
    def demo():
        return 1,2,3
    a = demo()  
    a1,a2,a3 = a
    print(a)    # (1, 2, 3)
    print(a1,a2,a3) # 1 2 3
    ```
    - 交换数据
    ```python
    a,b = 5,10
    a,b = b,a
    print(a,b)  # 10 5
    ```

### 集合
无序不重复
**可变**的数据类型
不支持索引和切片

- 创建: 可以自动去重
    - set(seq)
    - {元素/推导式}: 不能用此方法创建空集
- 操作:
    - update(seq): 原集合并上seq
    - add(元素): 添加
    - remove(元素): 删除元素
    - disacrd(元素): 删除元素
    - pop(): 随机删除
    - clear(): 清空集合
- 集合关系:
    - s包含t:
        - s.issuperset(t)
        - s > t: 真包含
        - s >= t
    - t含于s:
        - t.issubset(s)
        - t < s: 真子集
        - t <= s
    - s等价t
        - s == t
    - s 与 t 无交集
        - s.isdisjoint(t)
- 集合运算:
    - 并集:
        - s.union(t)
        - s | t
    - 交集:
        - s.intersection(t)
        - s & t
    - 差集:
        - s.difference(t)
        - s - t
    - 对称差/异或:
        - s.symmetric_difference(t)
        - s ^ t

### 字典
无序可变, 元素是键值对
键不可重复, 必须是不可变数据类型

- 创建: 相同键, 保留最后一次的值
    - {}: 可以用此方式创建空字典
        - {键:值}
        - {推导式}
    - dict(): 
        - dict(键:值)
        - dict([(键,值)])
        - dict(zip([seq1, seq2]))
    - dict.fromkeys(seq, value): 序列元素为键,值都为value, 默认None
- 访问
    - dict[key]: 不存在key会报错
    - get(key, default): 存在key返回对应值,不存在返回default, 默认为none
    - keys(): 获取所有键
    - values(): 获取所有值
    - items(): 获取所有键值对, 元组形式
- 修改:
    - dict[key]赋值: 有相同键修改值, 无则添加
    - update(): 有相同键修改值, 无则添加
        - 可以传入字典 元组列表 等, 同创建
    - detdefault(key, value): 存在key返回值(不修改),不存在创建键值对
    - pop(key, default): 存在key删除键值对并返回值; 不存在返回default
    - popitem(): 删除最后一个键值对, 并返回
    - clear(): 清空

    




