import tkinter as tk
from ttkthemes import ThemedTk

class Window(ThemedTk):
    def __init__(self,theme:str | None,**kwargs): #定義 init
        super().__init__(**kwargs) #呼叫 init


def main():
    window = Window(theme="arc") #最少需要一個套用theme
    window.mainloop()

if __name__ == '__main__':
    main()
