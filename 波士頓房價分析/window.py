import tkinter as tk
from tkinter import Label, Entry, Button
from dataset import getInfo
import pandas as pd

# 使用 getInfo 函數從 dataset.py 中載入資料集
df = getInfo()

# 如果資料集為空，處理異常情況
if df.empty:
    print("無法載入資料集，請檢查文件路徑。")
    exit()

# 簡單的線性回歸模型函數
def simple_linear_regression(features):
    # 假設所有特徵都對房價有相同的影響力
    coefficients = [1] * len(features.columns)
    prediction = (coefficients * features).sum(axis=1)  # 簡單線性加權求和
    return prediction

# 建立視窗
window = tk.Tk()
window.title('房價預測系統')

# 輸入特徵變數的標籤和輸入框
Label(window, text='房屋特徵1:').grid(row=0, column=0)
entry_feature1 = Entry(window)
entry_feature1.grid(row=0, column=1)

Label(window, text='房屋特徵2:').grid(row=1, column=0)
entry_feature2 = Entry(window)
entry_feature2.grid(row=1, column=1)

# 顯示預測結果的標籤和內容
Label(window, text='預測房價:').grid(row=2, column=0)
label_prediction = Label(window, text='')
label_prediction.grid(row=2, column=1)

# 預測按鈕的函數
def predict_price():
    try:
        feature1 = float(entry_feature1.get())
        feature2 = float(entry_feature2.get())
        
        # 準備特徵變數
        features = pd.DataFrame({
            'CRIM': [feature1],
            'ZN': [feature2]
        })
        
        # 使用簡單的線性回歸函數來預測房價
        prediction = simple_linear_regression(features)
        
        # 顯示預測結果
        label_prediction.config(text=f'${prediction[0]:,.2f}')
    except ValueError:
        label_prediction.config(text='請輸入有效數字')

# 預測按鈕
predict_button = Button(window, text='預測房價', command=predict_price)
predict_button.grid(row=3, columnspan=2)

# 啟動視窗主迴圈
window.mainloop()
