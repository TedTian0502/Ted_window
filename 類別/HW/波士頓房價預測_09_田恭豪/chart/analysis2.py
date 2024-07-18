import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# 讀取數據集
data = pd.read_csv('C:/Users/user/Documents/GitHub/Ted_window/類別/HW/波士頓房價預測_09_田恭豪/train_dataset.csv')

def plot_boxplot(data):
    # 求出四分位距(IQR)=Q3-Q1與上邊界(天花板)和下邊界(地板)
    Q1 = data['PRICE'].quantile(0.25)
    Q3 = data['PRICE'].quantile(0.75)
    IQR = Q3 - Q1
    Upper = Q3 + 1.5 * IQR
    Lower = Q1 - 1.5 * IQR
    print('Summary statistics:')
    print('Q3=', Q3, 'Q1=', Q1, 'IQR=', IQR, 'Upper=', Upper, 'Lower=', Lower)

    # 創建圖表並繪製盒鬚圖
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.boxplot(data['PRICE'], showmeans=True)
    ax.set_title('Boxplot of Price')
    ax.set_ylabel('Price')

    # 將圖表轉換為 PIL Image
    canvas = FigureCanvas(fig)
    canvas.draw()
    pil_image = Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())

    # 調整圖片大小
    pil_image = pil_image.resize((600, 400), Image.LANCZOS)

    # 將 PIL Image 轉換為 PhotoImage 對象
    photo = ImageTk.PhotoImage(image=pil_image)
    
    plt.close(fig)  # 關閉圖表，釋放資源

    return photo
