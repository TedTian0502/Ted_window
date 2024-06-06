import tkinter as tk
from tkinter import ttk

def calculate_bmi():
    try:
        height = float(height_entry.get())
        weight = float(weight_entry.get())
        bmi = weight / ((height / 100) ** 2)
        result_label.config(text=f"你的BMI為: {bmi:.2f}")
    except ValueError:
        result_label.config(text="請輸入有效的數字！")

root = tk.Tk()
root.geometry("240x150")
root.title('BMI計算器')
root.resizable(0, 0)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)

username_label = ttk.Label(root, text="姓名:")
username_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

username_entry = ttk.Entry(root)
username_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

height_label = ttk.Label(root, text="身高(cm):")
height_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

height_entry = ttk.Entry(root)
height_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

weight_label = ttk.Label(root, text="體重(kg):")
weight_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

weight_entry = ttk.Entry(root)
weight_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

login_button = ttk.Button(root, text="開始計算", command=calculate_bmi)
login_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

result_label = ttk.Label(root, text="")
result_label.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

root.mainloop()
