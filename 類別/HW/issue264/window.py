import tkinter as tk
from tkinter import ttk, Toplevel, Checkbutton, Button, messagebox
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
        
        # 呼叫函數以居中視窗
        self.center_window(800, 600)

        self.create_widgets()

        # 初始化 Treeview 相關變量
        self.tree_frame1 = None
        self.tree1 = None
        self.tree_frame2 = None
        self.tree2 = None

        # 設置窗口關閉時的處理
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # 選項視窗的成員變量
        self.options_window = None

    def create_widgets(self):
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
        self.reset_btn = tk.Button(self.frame, text="恢復初始狀態", pady=5, font=('Tahoma', 10), command=self.reset_data)
        self.reset_btn.pack(side="left", padx=(5, 10))

        # 新增按鈕 "打開選項"
        self.open_options_btn = tk.Button(self.frame, text="打開選項", pady=5, command=self.open_options_window)
        self.open_options_btn.pack(side="left")

        # 創建 Canvas
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack()
        self.canvas.place(x=440, y=50, width=350, height=540)

        # 繪製背景色塊或圖形
        self.canvas.create_rectangle(0, 0, 800, 600, fill="#FBF6E2")

    def center_window(self, width=800, height=600):
        # 取得螢幕的寬度和高度
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 計算視窗的位置，使其位於螢幕中央
        position_x = (screen_width - width) // 2
        position_y = (screen_height - height) // 2

        # 設定視窗的寬度、高度及位置
        self.geometry(f'{width}x{height}+{position_x}+{position_y}')

    def show_data(self):
        if self.tree_frame1 is None:
            self.create_treeview1()

        if self.tree_frame2 is None:
            self.create_treeview2()

    def create_treeview1(self):
        self.tree_frame1 = tk.Frame(self)
        self.tree_frame1.pack(pady=20, padx=(10, 370))

        self.tree1 = ttk.Treeview(self.tree_frame1, columns=("CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PIRATIO", "B", "LSTAT", "PRICE"), show="headings")

        for col in ("CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PIRATIO", "B", "LSTAT", "PRICE"):
            self.tree1.heading(col, text=col, anchor="center")
            self.tree1.column(col, anchor="center", width=80, stretch=False)

        vsb1 = ttk.Scrollbar(self.tree_frame1, orient="vertical", command=self.tree1.yview)
        self.tree1.configure(yscrollcommand=vsb1.set)
        vsb1.pack(side="right", fill="y")

        hsb1 = ttk.Scrollbar(self.tree_frame1, orient="horizontal", command=self.tree1.xview)
        self.tree1.configure(xscrollcommand=hsb1.set)
        hsb1.pack(side="bottom", fill="x")

        self.tree1.pack(side="left", fill="both", expand=True)
        self.tree_frame1.grid_rowconfigure(0, weight=1)
        self.tree_frame1.grid_columnconfigure(0, weight=1)

        try:
            df = pd.read_csv("./train_dataset.csv")
            for index, row in df.head(20).iterrows():
                data = tuple(row)
                self.tree1.insert("", "end", values=data)
        except FileNotFoundError:
            print("找不到指定的 CSV 檔案。")

    def create_treeview2(self):
        self.tree_frame2 = tk.Frame(self)
        self.tree_frame2.pack(pady=20, padx=(10, 370), fill="both", expand=True)

        self.tree2 = ttk.Treeview(self.tree_frame2, columns=("Statistic", "CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PIRATIO", "B", "LSTAT", "PRICE"), show="headings")

        # 設置標題
        self.tree2.heading("Statistic", text="Statistic", anchor="center")
        self.tree2.column("Statistic", width=60, stretch=False)

        for col in ("CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PIRATIO", "B", "LSTAT", "PRICE"):
            self.tree2.heading(col, text=col, anchor="center")
            self.tree2.column(col, width=80, stretch=False)

        hsb2 = ttk.Scrollbar(self.tree_frame2, orient="horizontal", command=self.tree2.xview)
        self.tree2.configure(xscrollcommand=hsb2.set)
        hsb2.pack(side="bottom", fill="x")

        self.tree2.pack(side="left", fill="both", expand=True)
        self.tree_frame2.grid_rowconfigure(0, weight=1)
        self.tree_frame2.grid_columnconfigure(0, weight=1)

        try:
            df = pd.read_csv("./train_dataset.csv")
            stats = df.describe()

            for stat_index, stat_name in enumerate(["count", "mean", "std", "min", "25%", "50%", "75%", "max"]):
                values = [stat_name] + [stats.loc[stat_name, col] for col in ("CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PIRATIO", "B", "LSTAT", "PRICE")]
                self.tree2.insert("", "end", values=values)
        except FileNotFoundError:
            print("找不到指定的 CSV 檔案。")

    def reset_data(self):
        self.destroy_treeview1()
        self.destroy_treeview2()

    def destroy_treeview1(self):
        if self.tree_frame1:
            for widget in self.tree_frame1.winfo_children():
                widget.destroy()
            self.tree_frame1.destroy()
            self.tree1 = None
            self.tree_frame1 = None

    def destroy_treeview2(self):
        if self.tree_frame2:
            for widget in self.tree_frame2.winfo_children():
                widget.destroy()
            self.tree_frame2.destroy()
            self.tree2 = None
            self.tree_frame2 = None

    def open_options_window(self):
        if self.options_window is None or not self.options_window.winfo_exists():
            options_window = tk.Toplevel(self)
            options_window.title("選擇選項")

            # 動態計算選項視窗的大小
            option_count = len(["選項1", "選項2", "選項3"])
            window_width = 200
            window_height = 50 + (38 * option_count) + 50 + 10  # 初始高度 + 每個選項的高度 + 按鈕的高度 + 內邊距

            # 設定選項視窗的大小
            options_window.geometry(f"{window_width}x{window_height}")

            # 計算選項視窗的位置，使其位於背景顏色的區域
            parent_x = self.winfo_rootx()
            parent_y = self.winfo_rooty()
            options_window.geometry(f"+{parent_x + 440}+{parent_y + 50}")

            options = ["選項1", "選項2", "選項3"]
            checkbuttons = []
            for option in options:
                checkbutton = tk.Checkbutton(options_window, text=option)
                checkbutton.pack(pady=5)
                checkbuttons.append(checkbutton)

            # 將 options_window 設置為類的成員變量，以便後續檢查
            self.options_window = options_window

            def close_options_window():
                options_window.destroy()

            btn_finish = tk.Button(options_window, text="完成", command=close_options_window)
            btn_finish.pack(pady=10, side="bottom")
        else:
            messagebox.showinfo("提示", "請勿連續點擊")

    def on_close(self):
        self.destroy()

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = MyWindow()
    app.run()