import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox

class Window(ThemedTk):
    def __init__(self,theme:str | None,**kwargs): #定義 init
        super().__init__(**kwargs) #呼叫 init
        self.title("BMI計算器")
        #self.configure(bg="#D3D3D3")    # 改變背景顏色
        #self.geometry("350x350+100+50") # 設置窗口初始大小
        self.resizable(False,False )     # 允許窗口大小可調
        style = ttk.Style()
        style.configure('input.TFrame',background='#ffffff')
        style.configure('press.TButton',font=('arial',10))
        #========================
        titleFrame = ttk.Frame(self)
        title_label = ttk.Label(self, text="BMI計算器", font=("Arial", 20))
        title_label.pack(pady=10)
        titleFrame.pack(padx=100,pady=(0,20))
        #========================
        input_frame = ttk.Frame(self,style='Input.TFrame')

        # 姓名
        label_name = ttk.Label(input_frame, text="姓名:")
        label_name.grid(row=0, column=0, padx=5, pady=5,sticky=tk.E)

        self.entry_name = ttk.Entry(input_frame)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        # 身高體重
        label_height = ttk.Label(input_frame, text="身高 (cm):")
        label_height.grid(row=1, column=0, padx=5, pady=5,sticky=tk.E)

        self.entry_height = ttk.Entry(input_frame)
        self.entry_height.grid(row=1, column=1, padx=5, pady=5)

        label_weight = ttk.Label(input_frame, text="體重 (kg):")
        label_weight.grid(row=2, column=0, padx=5, pady=5,sticky=tk.E)

        self.entry_weight = ttk.Entry(input_frame)
        self.entry_weight.grid(row=2, column=1, padx=5, pady=5)

        
        #視窗介面內部大小
        input_frame.pack(padx=30,pady=10)
        # =========================================================

        # 計算按鈕設計
        button_calculate = ttk.Button(self, text="計算", command=self.show_bmi_result,style='press.TButton')
        button_calculate.pack(side=tk.RIGHT,padx=(0,35),pady=10)


    def show_bmi_result(self):
        try:
            name:str = self.entry_name.get()
            height:int = int(self.entry_height.get())
            weight:int = int(self.entry_weight.get())
        
        #except UnboundLocalError:
            #messagebox.showwarning("Warning","欄位沒有填寫")
        except ValueError:
            messagebox.showwarning("Warning","格式錯誤,欄位沒有填寫")
        except Exception:
            messagebox.showwarning("Warning","不知明的錯誤")
        else:
            self.show_result(name=name,height=height,weight=weight)



    def show_result(self,name:str,height:int,weight:int):
            bmi = weight / (height / 100) ** 2
            if bmi < 18.5:
                status = "體重過輕"
                ideal_weight = 18.5 * (height / 100) ** 2
                weight_change = ideal_weight - weight
                status_color = "red"
                advice = f"您需要至少增加 {abs(weight_change):.2f} 公斤才能達到正常體重。"
            elif 18.5 <= bmi <= 24.9:
                status = "正常"
                status_color = "black"
                advice = "您的體重正常，請保持！"
            else:
                status = "體重過重"
                ideal_weight = 24.9 * (height / 100) ** 2
                weight_change = weight - ideal_weight
                status_color = "red"
                advice = f"您需要至少減少 {abs(weight_change):.2f} 公斤才能達到正常體重。"
            
            result_message = f"{name}您好:\n   bmi:{bmi:.2f}\n   體重:{status}\n   建議:{advice}"
            print(result_message)




def main():
    window = Window(theme="arc") #最少需要一個套用theme
    window.mainloop()

if __name__ == '__main__':
    main()
