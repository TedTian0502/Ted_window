import tkinter as tk
from tkinter import ttk, Button,messagebox
from dataset import getInfo
import numpy as np       #數學處理
import pandas as pd       #資料處理
import matplotlib.pyplot as plt #繪圖
import seaborn as sns
from tkinter import filedialog

# cd 波士頓房價預測

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
        self.option_add('*font',('Tahoma', 15, 'bold'))
        self.title("波士頓房價預測")

        # 設定窗口大小
        self.geometry("600x400")

        # 創建框架放置標籤和按鈕
        frame = tk.Frame(self)
        frame.pack(anchor="nw")

        # 標籤設計
        label = tk.Label(frame, text="波士頓房價", bg="lightblue", relief="raised", padx=20, pady=10)
        label.pack(side="left",)  # 放置在框架的左側
        
        # 按鈕設計
        btn_text = "查看數據集 \u21E9" 
        btn = tk.Button(frame, text=btn_text, pady=5)
        btn.pack(side="left", padx=5)  # 放置在框架的左側

        
        
    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = MyWindow()
    app.run()


