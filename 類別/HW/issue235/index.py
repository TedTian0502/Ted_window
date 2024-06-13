import data
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox

class Window(ThemedTk):
      def __init__(self,theme:str|None,**kwargs):
        super().__init__(**kwargs)
        try:
            ubike:list[dict] = data.load_data()
        # except Exception as error:
        #     print(error) 
        except Exception:
            messagebox.showwarning("出現錯誤","資料未能成功下再載")
        else:
            print(ubike)

# ===========================================================================


def main():   
    window = Window(theme='arc')
    window.mainloop()

if __name__ == '__main__':
    main()