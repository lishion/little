`crange`可以让你像使用`range`一样生成字母的序列:

```python
from chrange import crange
print(list(crange('t','z'))) # crange生成的是一个迭代器，因此你需要使用list转换才能输出
#['T', 'U', 'V', 'W', 'X', 'Y', 'Z']
for x in crange('AS','AZ',lower=True):
    print(x,end=' ')
# t u v w x y z
```

使用`to_num_index`将对应的序列转化为10进制:

```python
from chrange import to_num_index
print( to_num_index('a') )
print( to_num_index('z') )
# 1
# 26
```

如果你苦恼于每次都需要更改excel的设置以便使用数字现实列，现在你可以:

```python
from chrange import to_num_index as tni
from chrange import crange
print( [tni(x,-1) for x in crange('P','AA')] )
# [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
```

