import dash
from dash import dcc, html
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import io
import base64
import matplotlib
from scipy import stats
import numpy as np

# 設置 matplotlib 使用的字型，選擇支持中文的字型
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']  # 或其他支持中文的字型
matplotlib.rcParams['axes.unicode_minus'] = False  # 顯示負號

# 使用 'Agg' 後端
matplotlib.use('Agg')

# Load the dataset from CSV
df = pd.read_csv('train_dataset.csv')

# Function to remove outliers
def remove_outliers(data):
    return data[(data - data.mean()).abs() < 3 * data.std()]

# Function to create figure for the given feature with various transformations
def create_figure(feature, transformation):
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # 移除離群值
    data = df[feature].copy()
    data = remove_outliers(data)

    # 原始數據
    sns.histplot(df[feature], kde=True, ax=axes[0])
    axes[0].set_title(f'{feature} 分佈圖 (原始數據)')
    axes[0].set_xlabel(feature)
    axes[0].set_ylabel('Count')

    # 根據選擇的修正方法處理數據
    if transformation == '對數轉換':
        if (data > 0).all():
            transformed_data = np.log(data)
            title = f'{feature} 分佈圖 (對數轉換)'
            xlabel = f'Log({feature})'
        else:
            transformed_data = data
            title = f'{feature} 分佈圖 (對數轉換)'
            xlabel = '資料中包含非正數'
    elif transformation == '平方根轉換':
        if (data >= 0).all():
            transformed_data = np.sqrt(data)
            title = f'{feature} 分佈圖 (平方根轉換)'
            xlabel = f'Sqrt({feature})'
        else:
            transformed_data = data
            title = f'{feature} 分佈圖 (平方根轉換)'
            xlabel = '資料中包含負數'
    elif transformation == '立方根轉換':
        transformed_data = np.cbrt(data)
        title = f'{feature} 分佈圖 (立方根轉換)'
        xlabel = f'Cbrt({feature})'
    elif transformation == '次方轉換':
        if data.skew() < 0:
            power = 0.25
            transformed_data = np.power(data, power)
            title = f'{feature} 分佈圖 (次方轉換)'
            xlabel = f'Power({feature}, {power})'
        else:
            transformed_data = data
            title = f'{feature} 分佈圖 (次方轉換)'
            xlabel = '資料無左偏'
    elif transformation == 'Box-Cox 轉換':
        if (data > 0).all():
            transformed_data, _ = stats.boxcox(data)
            title = f'{feature} 分佈圖 (Box-Cox 轉換)'
            xlabel = f'Box-Cox({feature})'
        else:
            transformed_data = data
            title = f'{feature} 分佈圖 (Box-Cox 轉換)'
            xlabel = '資料中包含非正數'
    else:
        transformed_data = data
        title = '未選擇修正方法'
        xlabel = '選擇修正方法'

    sns.histplot(transformed_data, kde=True, ax=axes[1])
    axes[1].set_title(title)
    axes[1].set_xlabel(xlabel)
    axes[1].set_ylabel('Count')

    # Save the figure to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf

# Function to convert image buffer to base64
def encode_image(buf):
    encoded = base64.b64encode(buf.read()).decode('ascii')
    buf.close()  # 確保在使用後關閉緩衝區
    return encoded

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("波士頓房價數據分析"), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.Div([
            html.Label("選擇特徵"),
            dcc.Dropdown(
                id='feature-dropdown',
                options=[{'label': col, 'value': col} for col in df.columns if col != 'PRICE'],
                value=df.columns[0]
            ),
        ]), width=6),
        dbc.Col(html.Div([
            html.Label("選擇修正方法"),
            dcc.Dropdown(
                id='transformation-dropdown',
                options=[
                    {'label': '對數轉換 (資料不能有0或負數)', 'value': '對數轉換'},
                    {'label': '平方根轉換 (資料不能是負數)', 'value': '平方根轉換'},
                    {'label': '立方根轉換', 'value': '立方根轉換'},
                    {'label': '次方轉換 (只能處理左偏)', 'value': '次方轉換'},
                    {'label': 'Box-Cox 轉換', 'value': 'Box-Cox 轉換'}
                ],
                value='對數轉換'
            ),
        ]), width=6)
    ]),
    dbc.Row([
        dbc.Col(html.Img(id='feature-image'), width=12)
    ])
])

# Callback to update image based on selected feature and transformation
@app.callback(
    Output('feature-image', 'src'),
    [Input('feature-dropdown', 'value'),
     Input('transformation-dropdown', 'value')]
)
def update_image(selected_feature, selected_transformation):
    try:
        buf = create_figure(selected_feature, selected_transformation)
        encoded_image = encode_image(buf)
        return 'data:image/png;base64,{}'.format(encoded_image)
    except Exception as e:
        print(f"Error: {e}")
        return "data:image/png;base64,"  # 返回空圖像以顯示錯誤

# Run the app
if __name__ == "__main__":
    app.run_server("localhost", 8060, debug=True)
