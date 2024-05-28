## lesson1
#### open
open()至少需要一個變數

如果沒有使用 with as ，則應呼叫 f.close() 關閉檔案

文字內容不會顯示換行
如果使用print(): 將文字內容換行顯示在螢幕上

## index
```
def get_names() -> list[str]:
    with open('names.txt',encoding="utf-8") as file:
        conntent:str = file.read()
    names:list[str] = conntent.split()  #區域變數
    return names

names:list[str] = get_names()  #文件變數
```

GUI:
Graphical: 圖形介面
User 
Interface

## class tk.Tk
def init(self,xxx,xxx,xxx,xxx)

## class window
