## 如何建立list 
l1 = [2, 4, 6, 8, 10]
### list實體
index ---->序列,串列(sequence) --interable
[2, 4, 6, 8, 10]

attribute
property
method(實體的方法)

#回傳一個列舉 (enumerate) 物件。iterable 必須是一個序列
for item in enumerate(l1):
    print(item)

結果:(0, 2)
     (1, 4)
     (2, 6)
     (3, 8)
     (4, 10)

#tuple的拆解法:
(index,value)= (0,2)
print(index)
print(value)

結果:  0
       2

l1.attribute
l1.property
l1.實體方法

實體名稱[index]:subscript


print(l1[0],end=' ')
print(l1[1],end=' ')
print(l1[2],end=' ')
print(l1[3],end=' ')
print(l1[4])
print(l1[5])

結果: IndexError

遇到閃退(raise IndexError):
try:
->檢查程式有沒有raise Exception(任何錯誤)
except Exception:
->解決錯誤



## dict
{key:value,key:value}

d1:dict
dict實體

mapping資料


value in sequence(value)
         mapping(key)
