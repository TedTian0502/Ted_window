import tkinter as tk
from tkinter import ttk

# root window
root = tk.Tk()
root.geometry("240x100")
root.title('BMI計算器')
root.resizable(0, 0)

# configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)


# 姓名
username_label = ttk.Label(root, text="姓名:")
username_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

username_entry = ttk.Entry(root)
username_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

# 身高
password_label = ttk.Label(root, text="身高:")
password_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

password_entry = ttk.Entry(root,  show="*")
password_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

# 體重
password_label = ttk.Label(root, text="體重:")
password_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

password_entry = ttk.Entry(root,  show="*")
password_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

# 計算
login_button = ttk.Button(root, text="開始計算")
login_button.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)


root.mainloop()
