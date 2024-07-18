import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

# # 創建主視窗
# root = tk.Tk()
# root.title("Matplotlib in Tkinter Demo")

# # 創建第一個Matplotlib圖表
# fig1 = Figure(figsize=(5, 4), dpi=100)
# ax1 = fig1.add_subplot(111)
# ax1.plot([1, 2, 3, 4], [10, 20, 25, 30], color='lightblue', linewidth=2)
# ax1.set_xlabel('X軸')
# ax1.set_ylabel('Y軸')
# ax1.set_title('圖表1')

# # 創建第二個Matplotlib圖表
# fig2 = Figure(figsize=(4, 3), dpi=100)
# ax2 = fig2.add_subplot(111)
# ax2.plot([1, 2, 3, 4], [30, 25, 20, 10], color='lightgreen', linewidth=2)
# ax2.set_xlabel('X軸')
# ax2.set_ylabel('Y軸')
# ax2.set_title('圖表2')

# # 1.計算兩張圖的大小來設置視窗大小
# # width = max(fig1.get_figwidth(), fig2.get_figwidth())
# # height = fig1.get_figheight() + fig2.get_figheight()

# # # 1.設置視窗大小
# # root.geometry(f"{int(width * 100)}x{int(height * 100)}")  # 放大倍率乘以100，方便視窗看到

# # 2.計算兩張圖的寬度來設置視窗大小()
# width = fig1.get_figwidth() + fig2.get_figwidth()
# root.geometry(f"{int(width * 100)}x400")  # 設置高度為 400 像素，寬度根據兩張圖表的總寬度來決定

# # 2.在視窗中放置第一張圖
# frame1 = ttk.Frame(root, padding=(5, 5, 5, 5))
# frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
# canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
# canvas1.draw()
# canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# # 在視窗中放置第二張圖
# frame2 = ttk.Frame(root, padding=(5, 5, 5, 5))
# frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
# canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
# canvas2.draw()
# canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# # 開始主迴圈
# root.mainloop()
# Example data (replace with your actual data)
data = pd.DataFrame({'PRICE': [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]})

# Calculate quartiles and IQR
Q1 = data['PRICE'].quantile(0.25)
Q3 = data['PRICE'].quantile(0.75)
IQR = Q3 - Q1

# Calculate upper and lower bounds
Upper = Q3 + 1.5 * IQR
Lower = Q1 - 1.5 * IQR

print('Q1 =', Q1)
print('Q3 =', Q3)
print('IQR =', IQR)
print('Upper bound (天花板) =', Upper)
print('Lower bound (地板) =', Lower)

# Create boxplot
plt.figure(figsize=(5, 8))
plt.boxplot(data['PRICE'], showmeans=True)
plt.title('PRICE')
plt.show()