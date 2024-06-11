import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def calculate_bmi(username, height, weight, result_label):
    try:
        height_value = float(height.get())
        weight_value = float(weight.get())
        bmi = weight_value / ((height_value / 100) ** 2)
        username_value = username.get()
        result_label.config(text=f"{username_value} 的BMI為: {bmi:.2f}")
        
        # BMI計算公式
        if bmi < 18.5:
            status = "過輕"
            suggestion = f"建議增重 {18.5*(height_value/100)**2 - weight_value:.2f} 公斤"
        elif bmi >= 18.5 and bmi < 24:
            status = "正常"
            suggestion = "體重正常，請保持"
        else:
            status = "過重"
            suggestion = f"建議減重 {weight_value - 24*(height_value/100)**2:.2f} 公斤"

        # Popup window to display result
        popup = tk.Toplevel()
        popup.title("BMI計算結果")
        popup.geometry("220x150")
        result_text = f"姓名: {username_value}\nBMI: {bmi:.2f}\n狀態: {status}\n建議: {suggestion}"
        result_label_popup = ttk.Label(popup, text=result_text)
        result_label_popup.pack(padx=10, pady=10)

    except ValueError:
        messagebox.showerror("錯誤", "請輸入有效的數字！")

def main():
    root = tk.Tk()
    root.title('BMI計算器')
    root.geometry("220x150")
    root.resizable(0, 0)
    root.configure(background='#DAD3BE')  # 設置背景色

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

    result_label = ttk.Label(root, text="")
    result_label.grid(column=1, row=5, sticky=tk.E, padx=5, pady=5)

    login_button = ttk.Button(root, text="開始計算", command=lambda: calculate_bmi(username_entry, height_entry, weight_entry, result_label))
    login_button.grid(column=0, row=4, columnspan=2, pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()


