import dash
from dash import dcc, html, dash_table
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import io
import base64
import matplotlib
from scipy import stats
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 設置 matplotlib 使用的字型，選擇支持中文的字型
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 使用 'Agg' 後端
matplotlib.use('Agg')

# 從 CSV 檔案載入數據集
df = pd.read_csv('train_dataset.csv')

# 定義移除離群值的函數
def remove_outliers(data):
    return data[(data - data.mean()).abs() < 3 * data.std()]

# 移除所有特徵的離群值
df_clean = df.apply(remove_outliers)

# 移除包含 NaN 的行
df_clean.dropna(inplace=True)

# 定義將圖像緩衝區轉換為 base64 的函數
def encode_image(buf):
    encoded = base64.b64encode(buf.read()).decode('ascii')
    buf.close()
    return encoded

# 初始化 Dash 應用程序
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定義應用程序的佈局
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("波士頓房價數據分析"), width=12)
    ], style={'margin-bottom': '20px'}),  # 標題行
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='model-dropdown',
            options=[
                {'label': '線性回歸', 'value': 'linear-regression'},
                {'label': 'K近鄰回歸模型', 'value': 'knn'},
                {'label': 'GridSearchCV', 'value': 'grid-search'},
                {'label': '決策樹', 'value': 'decision-tree'},
                {'label': '隨機森林', 'value': 'random-forest'}
            ],
            placeholder='請選擇模型',
            style={'width': '100%'}
        ), width=6, style={'margin-bottom': '20px'}),  # 模型選擇下拉框
        dbc.Col(dcc.Input(id='threshold-input', type='number', min=0, max=1, step=0.01, disabled=True), width=2),
        dbc.Col(dbc.Button("查看結果", id='evaluate-button', n_clicks=0), width=2),
        dbc.Col(dbc.Button("刪除數據", id='clear-button', n_clicks=0), width=2)  # 新增刪除數據按鈕
    ]),
    dbc.Row([
        dbc.Col(html.Pre(id='evaluation-result', style={'backgroundColor': '#6EACDA', 'padding': '10px', 'border': '1px solid #dee2e6', 'font-size': '18px'}), width=6),
        dbc.Col(html.Pre(id='selected-features', style={'backgroundColor': '#E2E2B6', 'padding': '10px', 'border': '1px solid #dee2e6', 'font-size': '18px'}), width=6)
    ], style={'margin-bottom': '20px'}),  # 顯示評估結果和特徵數及名稱的區域
    dbc.Row([
        dbc.Col(html.H3("模型評估分數"), width=12)
    ], style={'margin-bottom': '20px'}),  # 模型評估分數標題
    dbc.Row([
        dbc.Col(dash_table.DataTable(
            id='evaluation-table',
            columns=[
                {'name': '模型名稱', 'id': 'model'},
                {'name': 'MSE', 'id': 'mse'},
                {'name': 'R-squared', 'id': 'r_squared'},
                {'name': '準確率', 'id': 'accuracy'}
            ],
            data=[],  # 初始數據為空
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '150px', 'maxWidth': '200px'}
        ), width=12)
    ])  # 顯示模型評估分數的數據表
])

# 儲存結果和選擇的模型
results_store = []
selected_model_store = None

@app.callback(
    [Output('threshold-input', 'disabled'),
     Output('threshold-input', 'value')],
    Input('model-dropdown', 'value')
)
def enable_threshold_input(selected_model):
    # 根據所選擇的模型來啟用或禁用閾值輸入框
    if selected_model is None:
        return True, None  # 若未選擇模型，禁用閾值輸入框
    return False, None  # 若選擇了模型，啟用閾值輸入框

@app.callback(
    [Output('evaluation-result', 'children'),
     Output('selected-features', 'children'),
     Output('evaluation-table', 'data')],
    [Input('evaluate-button', 'n_clicks'),
     Input('clear-button', 'n_clicks')],
    [State('model-dropdown', 'value'),
     State('threshold-input', 'value')]
)
def manage_results(evaluate_clicks, clear_clicks, selected_model, threshold):
    global results_store, selected_model_store

    # 當「刪除數據」按鈕被點擊時，清空結果數據
    if clear_clicks > 0:
        results_store = []
        return '請選擇模型並輸入閾值', '查看特徵數與名稱', results_store

    # 當「查看結果」按鈕被點擊
    if evaluate_clicks > 0:
        # 若未選擇模型或未輸入閾值
        if selected_model is None:
            return '請先選擇模型並輸入閾值', '查看特徵數與名稱', results_store
        if threshold is None:
            return '請輸入閾值', '查看特徵數與名稱', results_store

        # 根據選擇的模型進行評估
        selected_features = df_clean.corr().loc[:, 'PRICE'].abs() > threshold
        features = df_clean.columns[selected_features]

        X = df_clean[features].drop(columns=['PRICE']).dropna()
        y = df_clean['PRICE'].loc[X.index]

        if selected_model == 'linear-regression':
            model = LinearRegression()
            model_name = '線性回歸'
        elif selected_model == 'knn':
            model = KNeighborsRegressor()
            model_name = 'K近鄰回歸模型'
        elif selected_model == 'grid-search':
            model = GridSearchCV(LinearRegression(), param_grid={'fit_intercept': [True, False]})
            model_name = 'GridSearchCV'
        elif selected_model == 'decision-tree':
            model = DecisionTreeRegressor()
            model_name = '決策樹'
        elif selected_model == 'random-forest':
            model = RandomForestRegressor()
            model_name = '隨機森林'
        else:
            return '請選擇模型', '', results_store

        model.fit(X, y)
        y_pred = model.predict(X)
        
        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)
        accuracy = np.mean(np.abs((y - y_pred) / y) < 0.2)  # 計算20%容忍範圍內的正確比率

        evaluation_result = f"顯示評估結果:\nR^2: {r2:.3f}\nMSE: {mse:.3f}\n容忍度: {accuracy:.3f}\n"
        
        selected_features_result = f"顯示特徵數: {len(features)}\n顯示特徵名稱: {', '.join(features)}\n"

        evaluation_data = {'model': model_name, 'mse': mse, 'r_squared': r2, 'accuracy': accuracy}

        # 將新結果添加到結果儲存中，並確保數據不超過8條
        results_store.append(evaluation_data)
        if len(results_store) > 8:
            results_store.pop(0)

        # 更新模型選擇儲存
        selected_model_store = selected_model

        return evaluation_result, selected_features_result, results_store

    # 若沒有按鈕被點擊，返回預設提示信息
    return '請選擇模型並輸入閾值', '查看特徵數與名稱', results_store

if __name__ == '__main__':
    app.run_server("localhost", 8050, debug=True)
