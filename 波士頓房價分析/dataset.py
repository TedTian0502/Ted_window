import pandas as pd

def getInfo() -> pd.DataFrame:
    # 讀取 CSV 文件
    file_path = 'C:/Git hub/Ted_window/波士頓房價分析/train_dataset.csv'
    try:
        rowdata = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"無法找到文件: {file_path}")
        return pd.DataFrame()  # 如果找不到文件，返回一個空的 DataFrame

    # 修正選擇特定的列，直接使用列名的列表
    selected_columns = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PIRATIO', 'B', 'LSTAT', 'PRICE']
    selectdata = rowdata[selected_columns]

    return selectdata

# 範例使用
selected_data = getInfo()
print(selected_data)




