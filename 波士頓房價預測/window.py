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
        self.option_add('*font', ('Tahoma', 15, 'bold'))
        self.title("波士頓房價預測")
        self.geometry("800x600")
        
        # 創建框架放置標籤和按鈕
        self.frame = tk.Frame(self)
        self.frame.pack(anchor="nw")

        # 標籤設計
        self.label = tk.Label(self.frame, text="波士頓房價", bg="lightblue", relief="raised", padx=20, pady=10)
        self.label.pack(side="left", padx=(10, 0))

        # 按鈕設計，包括文字和向下箭頭圖案
        self.show_btn = tk.Button(self.frame, text="查看數據集 \u21E9", pady=5, command=self.show_data)
        self.show_btn.pack(side="left", padx=(5, 0))

        # 恢復初始狀態按鈕
        self.reset_btn = tk.Button(self.frame, text="恢復初始狀態", pady=5, font=10, command=self.reset_data)
        self.reset_btn.pack(side="left", padx=(5, 0))

        # 獨立的框架用於放置 Treeview 和捲動軸
        self.tree_frame1 = None  # 初始時設置為空
        self.tree1 = None  # 初始時設置為空

        self.tree_frame2 = None  # 初始時設置為空
        self.tree2 = None  # 初始時設置為空

        # 設置窗口關閉時的處理
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def show_data(self):
        if self.tree_frame1 is None:
            # 創建獨立的框架來放置第一個 Treeview 和捲動軸
            self.tree_frame1 = tk.Frame(self)
            self.tree_frame1.pack(pady=20, padx=(10, 370))  # 調整大小與位置

            # 創建第一個 Treeview
            self.tree1 = ttk.Treeview(self.tree_frame1, columns=("CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PIRATIO", "B", "LSTAT", "PRICE"), show="headings")

            # 設置列標題
            for col in ("CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PIRATIO", "B", "LSTAT", "PRICE"):
                self.tree1.heading(col, text=col, anchor="center")
                self.tree1.column(col, anchor="center")

            # 設置列的最小和最大寬度
            for col in ("CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PIRATIO", "B", "LSTAT", "PRICE"):
                self.tree1.column(col, minwidth=40, width=80)

            # 垂直捲動軸
            vsb1 = ttk.Scrollbar(self.tree_frame1, orient="vertical", command=self.tree1.yview)
            self.tree1.configure(yscrollcommand=vsb1.set)
            vsb1.pack(side="right", fill="y")

            # 水平捲動軸
            hsb1 = ttk.Scrollbar(self.tree_frame1, orient="horizontal", command=self.tree1.xview)
            self.tree1.configure(xscrollcommand=hsb1.set)
            hsb1.pack(side="bottom", fill="x")

            # 設置 Treeview 的高度和寬度
            self.tree1.pack(side="left", fill="both", expand=True)
            self.tree_frame1.grid_rowconfigure(0, weight=1)
            self.tree_frame1.grid_columnconfigure(0, weight=1)

            # 從 CSV 檔案讀取數據
            try:
                df = pd.read_csv("./train_dataset.csv")

                for index, row in df.head(20).iterrows():
                    data = tuple(row)
                    self.tree1.insert("", "end", values=data)

            except FileNotFoundError:
                print("找不到指定的 CSV 檔案。")

        if self.tree_frame2 is None:
            # 創建獨立的框架來放置第二個 Treeview 和捲動軸
            self.tree_frame2 = tk.Frame(self)
            self.tree_frame2.pack(pady=20, padx=(10, 370))  # 調整大小與位置

            # 創建第二個 Treeview
            self.tree2 = ttk.Treeview(self.tree_frame2, columns=("属性", "值"), show="headings")

            # 設置列標題
            self.tree2.heading("属性", text="属性", anchor="center")
            self.tree2.heading("值", text="值", anchor="center")

            # 設置列的最小和最大寬度
            self.tree2.column("属性", minwidth=100, width=200)
            self.tree2.column("值", minwidth=100, width=200)

            # 垂直捲動軸
            vsb2 = ttk.Scrollbar(self.tree_frame2, orient="vertical", command=self.tree2.yview)
            self.tree2.configure(yscrollcommand=vsb2.set)
            vsb2.pack(side="right", fill="y")

            # 水平捲動軸
            hsb2 = ttk.Scrollbar(self.tree_frame2, orient="horizontal", command=self.tree2.xview)
            self.tree2.configure(xscrollcommand=hsb2.set)
            hsb2.pack(side="bottom", fill="x")

            # 設置 Treeview 的高度和寬度
            self.tree2.pack(side="left", fill="both", expand=True)
            self.tree_frame2.grid_rowconfigure(0, weight=1)
            self.tree_frame2.grid_columnconfigure(0, weight=1)

            # 從 CSV 檔案讀取數據
            try:
                df = pd.read_csv("./train_dataset.csv")
                stats = df.describe().transpose()
                for index, row in stats.iterrows():
                    self.tree2.insert("", "end", values=(index, row["mean"]))

            except FileNotFoundError:
                print("找不到指定的 CSV 檔案。")

    def reset_data(self):
        if self.tree_frame1:
            # 移除第一個 Treeview 和框架
            for widget in self.tree_frame1.winfo_children():
                widget.destroy()
            self.tree_frame1.destroy()
            self.tree1 = None
            self.tree_frame1 = None

        if self.tree_frame2:
            # 移除第二個 Treeview 和框架
            for widget in self.tree_frame2.winfo_children():
                widget.destroy()
            self.tree_frame2.destroy()
            self.tree2 = None
            self.tree_frame2 = None

    def on_close(self):
        # 關閉窗口時的處理，這裡只是簡單地退出應用程序
        self.destroy()

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = MyWindow()
    app.run()


