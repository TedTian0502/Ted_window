import tkinter as tk
from tkinter import ttk, Toplevel, messagebox, Button
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

    def create_widgets(self):
        # 創建框架放置標籤和按鈕
        self.frame = tk.Frame(self)
        self.frame.pack(anchor="nw", padx=5, pady=5)

        # 標籤設計
        self.label = tk.Label(self.frame, text="波士頓房價", bg="lightblue", relief="raised", padx=20, pady=10)
        self.label.pack(side="left")

        # combobox設計
        self.combobox = ttk.Combobox(self.frame, values=["查看數據分佈", "選項二", "選項三"], state="readonly")
        self.combobox.set("請選擇圖表")
        self.combobox.pack(side="left", padx=(5, 0))

        # 按鈕設計，包括文字和向下箭頭圖案
        self.show_btn = tk.Button(self.frame, text="查看資料 \u21E9", pady=5,font=('Tahoma', 12,'bold'), command=self.show_data,relief="raised",borderwidth=5)
        self.show_btn.pack(side="left", padx=(5, 0))

        # 恢復初始狀態按鈕
        self.reset_btn = tk.Button(self.frame, text="恢復初始狀態", pady=5, font=('Tahoma', 12,'bold'), command=self.reset_data,relief="raised",borderwidth=5)
        self.reset_btn.pack(side="left", padx=(5, 10))

        # 新增按鈕 "評分"
        self.open_options_btn = tk.Button(self.frame, text="評分", pady=5,font=('Tahoma', 12,'bold'), command=self.show_rating_dialog,relief="raised",borderwidth=5)
        self.open_options_btn.pack(side="left")

        # 添加背景框架，並填充視窗下方
        self.background_frame = tk.Frame(self, bg="#FBF6E2")
        self.background_frame.pack(fill="both", expand=True, padx=5, pady=5)

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
        selected_option = self.combobox.get()
        if selected_option == "請選擇圖表":
            messagebox.showwarning("警告", "請先選擇一個選項")
            return
        
        if selected_option == "查看數據分佈":
            if self.tree1 is None:
                self.create_treeview1()
            if self.tree2 is None:
                self.create_treeview2()
        # 可以根據其他選項添加對應的顯示邏輯
        # elif selected_option == "選項二":
        #     pass

    def create_treeview1(self):
        self.tree_frame1 = tk.Frame(self.background_frame)
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
            df = pd.read_csv("train_dataset.csv")
            for index, row in df.head(20).iterrows():
                data = tuple(row)
                self.tree1.insert("", "end", values=data)
        except FileNotFoundError:
            print("找不到指定的 CSV 檔案。")

    def create_treeview2(self):
        self.tree_frame2 = tk.Frame(self.background_frame)
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
            df = pd.read_csv("train_dataset.csv")
            stats = df.describe()

            for stat_index, stat_name in enumerate(["count", "mean", "std", "min", "25%", "50%", "75%", "max"]):
                values = [stat_name] + [stats.loc[stat_name, col] for col in ("CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PIRATIO", "B", "LSTAT", "PRICE")]
                self.tree2.insert("", "end", values=values)
        except FileNotFoundError:
            print("找不到指定的 CSV 檔案")

    def reset_data(self):
        self.destroy_treeview1()
        self.destroy_treeview2()
        self.combobox.set("請選擇圖表")

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

    def show_rating_dialog(self):
        messagebox.showinfo("分數", "準確率為: XXX")

    def on_close(self):
        self.destroy()

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = MyWindow()
    app.run()