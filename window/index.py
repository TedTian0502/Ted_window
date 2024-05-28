import tkinter as tk
def get_names() -> list[str]:
    with open('names.txt',encoding="utf-8") as file:
        conntent:str = file.read()
    names:list[str] = conntent.split()  #區域變數
    return names

# names:list[str] = get_names()  #文件變數

# if __name__ == '__main__':
#     names:list[str] = get_names()
#     print(names)

if __name__ == '__main__':
    names:list[str] = get_names()
    window:tk.Tk = tk.Tk()
    window.title("我的第一個GUI程式")
    window.mainloop()  #建立視窗軟體
