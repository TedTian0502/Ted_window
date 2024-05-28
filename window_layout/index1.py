import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.title("pack1")
        self.geometry('300x200')
        
        # btn1:ttk.Button = ttk.Button(self,text="Top")
        # btn1.pack()

        # btn2:ttk.Button = ttk.Button(self,text="Middle")
        # btn2.pack()

        # btn3:ttk.Button = ttk.Button(self,text="Bottom")
        # btn3.pack()

        ttk.Button(self,text="Top").pack()  

        ttk.Button(self,text="Middle").pack()  

        ttk.Button(self,text="Bottom").pack()


if __name__ == '__main__':
    window:Window = Window()
    window.mainloop()
