import tkinter as tk
from tkinter import ttk

def get_names() -> list[str]:
    with open('names.txt',encoding="utf-8") as file:
        conntent:str = file.read()
    names:list[str] = conntent.split()  #區域變數
    return names

# names:list[str] = get_names()  #文件變數

# if __name__ == '__main__':
#     names:list[str] = get_names()
#     print(names)

class Window(tk.Tk):
    def __init__(self,title:str="Hello! Tkinter!",**kwargs):
        super().__init__(**kwargs)
        #多做一些事
        self.title(title)
        label:ttk.Label = ttk.Label(self,
                                    text="Hello World!!",
                                    font=('Arial',20,'bold'),
                                    foreground = '#f00')
        label.pack(padx=100,pady=40)  #左右100,上下40

if __name__ == '__main__':
    names:list[str] = get_names()
    # window:tk.Tk = tk.Tk()
    # window.title("我的第一個GUI程式")
    window:Window = Window()
    window.mainloop()  #建立視窗軟體(在終端機打python index.py)
