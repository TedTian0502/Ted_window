import pandas as pd
import matplotlib.pyplot as plt

# 讀取數據集
data = pd.read_csv('train_dataset.csv')

def plot_boxplot(data):
    # 求出四分位距(IQR)=Q3-Q1與上邊界(天花板)和下邊界(地板)
    Q1 = data['PRICE'].quantile(0.25)
    Q3 = data['PRICE'].quantile(0.75)
    IQR = Q3 - Q1
    Upper = Q3 + 1.5 * IQR
    Lower = Q1 - 1.5 * IQR
    print('Q3=', Q3, 'Q1=', Q1, 'IQR=', IQR, 'Upper=', Upper, 'Lower=', Lower)

    plt.figure(figsize=(3, 5))
    plt.boxplot(data['PRICE'], showmeans=True)
    plt.title('PRICE')
    plt.show()
