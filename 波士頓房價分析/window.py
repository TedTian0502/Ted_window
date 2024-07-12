import tkinter as tk
from tkinter import ttk, messagebox
from dataset import getInfo
import pandas as pd

# cd 波士頓房價分析

# 使用 getInfo 函數從 dataset.py 中載入資料集
df = getInfo()

# 如果資料集為空，處理異常情況
if df.empty:
    print("無法載入資料集，請檢查文件路徑。")
    exit()
# =================================================

class MyWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Window")
        # 其他初始化設定
        
    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = MyWindow()
    app.run()