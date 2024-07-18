import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 創建主視窗
root = tk.Tk()
root.title("Matplotlib in Tkinter Demo")

# 設置視窗大小和位置
root.geometry("600x400")

# 創建一個Frame，用於放置Matplotlib圖表
frame = ttk.Frame(root, padding=(5, 5, 5, 5))
# frame.grid(row=0, column=0, sticky="nsew")  # 使用grid佈局，sticky設置為"nsew"使其填滿整個cell
frame.grid(row=0, column=0, padx=50)  # grid方法，在這裡使用 padx 設置左邊距(無法用padx=(x,y)控制位置)
# frame.pack(padx=50)  # pack方法，在這裡使用 padx 設置左邊距

# 創建Matplotlib圖表
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax.plot([1, 2, 3, 4], [10, 20, 25, 30], color='lightblue', linewidth=2)
ax.set_xlabel('X軸')
ax.set_ylabel('Y軸')
ax.set_title('這是Matplotlib的圖表')

# 將Matplotlib圖表嵌入到Tkinter視窗中
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# 使用 place 方法來直接設置 frame 的絕對位置
# frame.place(x=-150, y=200)  # 向左移動-150，向下移動200

# 開始主迴圈
root.mainloop()
