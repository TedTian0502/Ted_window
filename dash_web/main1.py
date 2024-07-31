from dash import Dash, dcc, html, Input, Output, State, dash_table, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from scipy.stats import skew, boxcox
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import plotly.io as pio

# 讀取數據集
df = pd.read_csv('train_dataset.csv')

# 標準化 NOX 數據
nox_standardized = (df['NOX'] - df['NOX'].mean()) / df['NOX'].std()

# 創建圖表
fig = go.Figure()
fig.add_trace(go.Histogram(
    x=df['NOX'],
    name='NOX (原始數據)',
    nbinsx=20,
    marker_color='blue',
    opacity=0.75,
    histnorm='probability density'
))
fig.add_trace(go.Histogram(
    x=nox_standardized,
    name='NOX (標準化數據)',
    nbinsx=20,
    marker_color='red',
    opacity=0.75,
    histnorm='probability density'
))
fig.update_layout(
    title='NOX 分佈圖',
    xaxis_title='NOX',
    yaxis_title='頻次',
    barmode='overlay',
    template='plotly_white'
)

# 將圖表轉換為 HTML 格式
fig_html = pio.to_html(fig, full_html=False)

# 讀取數據集
df = pd.read_csv('train_dataset.csv')

# 處理離群值（例如使用四分位距法）
def remove_outliers(df):
    df = df.copy()
    for col in df.columns:
        if df[col].nunique() <= 1:
            df = df.drop(columns=[col])
    
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    df_out = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]
    return df_out

# 計算特徵轉換
def transform_feature(df, feature):
    skewness = skew(df[feature].dropna())
    if skewness > 1:
        if (df[feature] > 0).all():
            df[feature] = np.log1p(df[feature])
            method = '對數轉換'
        else:
            df[feature] = np.cbrt(df[feature])
            method = '立方根轉換'
    elif 0.5 < skewness <= 1:
        if (df[feature] >= 0).all():
            df[feature] = np.sqrt(df[feature])
            method = '平方根轉換'
        else:
            df[feature] = np.cbrt(df[feature])
            method = '立方根轉換'
    else:
        if df[feature].nunique() > 1:
            df[feature], _ = boxcox(df[feature] + 1)
            method = 'Box-Cox 轉換'
        else:
            df[feature] = df[feature]
            method = '無需轉換'

    return df, method

# 初始化Dash應用
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定義應用佈局
app.layout = html.Div([
    html.H1("房價預測互動式Dash應用"),
    
    # Open collapse 按鈕
    html.Button("查看資料分布狀況", id="collapse-button", n_clicks=0),
    
    # 可折疊的內容區域
    dbc.Collapse(
        id='collapse',
        is_open=False,
        children=[
            dash_table.DataTable(
                id='data-describe',
                columns=[{'name': i, 'id': i} for i in df.describe().columns],
                data=df.describe().reset_index().to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '150px', 'maxWidth': '200px'}
            )
        ]
    ),

    # 特徵選擇
    html.Div([
        html.Label("選擇特徵"),
        dcc.Dropdown(
            id='feature-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns if col != 'PRICE'],
            value=df.columns[0]
        ),
    ]),

    # 特徵分佈圖
    dcc.Graph(id='feature-histogram'),
    
    # 模型選擇
    html.Div([
        html.Label("選擇模型"),
        dcc.Dropdown(
            id='model-dropdown',
            options=[
                {'label': '線性回歸', 'value': 'linear'},
                {'label': 'K近鄰回歸', 'value': 'knn'},
                {'label': 'GridSearchCV調整的K近鄰回歸', 'value': 'knn_grid'},
                {'label': '決策樹回歸', 'value': 'decision_tree'},
                {'label': '隨機森林', 'value': 'random_forest'}
            ],
            value='linear'
        ),
    ]),

    # 閾值輸入框
    html.Div([
        html.Label("輸入閾值 (0~1)"),
        dcc.Input(id='threshold-input', type='number', min=0, max=1, step=0.01, value=0.5),
    ]),

    # 模型分數顯示
    html.Div([
        html.Button('評估模型', id='evaluate-button'),
        html.Div(id='model-score')
    ]),

    # 結果記錄表格
    html.H3("模型分數記錄"),
    dash_table.DataTable(id='results-table', columns=[
        {'name': '模型', 'id': 'model'},
        {'name': 'MSE', 'id': 'mse'},
        {'name': 'R-squared', 'id': 'r2'},
        {'name': '正確比率', 'id': 'correct_ratio'}
    ], data=[]),
    html.Iframe(
        srcDoc=fig_html,
        style={"width": "100%", "height": "600px", "border": "none"}
    ),
])

# 回調函數：切換折疊面板的開啟狀態並更新按鈕文本
@app.callback(
    Output('collapse', 'is_open'),
    Output('collapse-button', 'children'),
    Input('collapse-button', 'n_clicks'),
    State('collapse', 'is_open')
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks:
        is_open = not is_open
    button_text = "關閉" if is_open else "查看資料分布狀況"
    return is_open, button_text

# 回調函數：更新特徵分佈圖
@app.callback(
    Output('feature-histogram', 'figure'),
    Input('feature-dropdown', 'value')
)
def update_histogram(selected_feature):
    df_no_outliers = remove_outliers(df)
    df_transformed, method = transform_feature(df_no_outliers.copy(), selected_feature)
    
    # 使用 plotly.graph_objs 來創建直方圖
    fig = go.Figure()
    
    # 繪製直方圖
    fig.add_trace(
        go.Histogram(
            x=df_transformed[selected_feature].dropna(),
            name=selected_feature,
            marker_color='blue'
        )
    )
    
    # 更新圖表佈局
    fig.update_layout(
        title=f'{selected_feature} 的分佈圖 ({method})', 
        xaxis_title=selected_feature, 
        yaxis_title='頻次',
        template='plotly_white'
    )
    
    return fig


# 回調函數：評估模型
@app.callback(
    Output('model-score', 'children'),
    Output('results-table', 'data'),
    Input('evaluate-button', 'n_clicks'),
    State('model-dropdown', 'value'),
    State('threshold-input', 'value'),
    State('results-table', 'data')
)
def evaluate_model(n_clicks, selected_model, threshold, table_data):
    if n_clicks is None:
        return no_update, no_update

    # 資料預處理
    df_no_outliers = remove_outliers(df)
    df_no_outliers.fillna(df_no_outliers.mean(), inplace=True)
    X = df_no_outliers.drop('PRICE', axis=1)
    y = df_no_outliers['PRICE']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    #feature不能固定，重新調整
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # 選擇模型
    if selected_model == 'linear':
        model = LinearRegression()
    elif selected_model == 'knn':
        model = KNeighborsRegressor()
    elif selected_model == 'knn_grid':
        param_grid = {'n_neighbors': [3, 5, 7, 9]}
        grid_search = GridSearchCV(KNeighborsRegressor(), param_grid, cv=5)
        grid_search.fit(X_train, y_train)
        model = grid_search.best_estimator_
    elif selected_model == 'decision_tree':
        model = DecisionTreeRegressor()
    elif selected_model == 'random_forest':
        model = RandomForestRegressor()
    else:
        return no_update, no_update

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    correct_ratio = np.mean(np.abs(y_test - y_pred) < threshold)

    model_name = '線性回歸' if selected_model == 'linear' else \
                 'K近鄰回歸' if selected_model == 'knn' else \
                 'GridSearchCV調整的K近鄰回歸' if selected_model == 'knn_grid' else \
                 '決策樹回歸' if selected_model == 'decision_tree' else \
                 '隨機森林'

    new_row = {
        'model': model_name,
        'mse': mse,
        'r2': r2,
        'correct_ratio': correct_ratio
    }

    table_data.append(new_row)

    return f"均方誤差(MSE): {mse:.2f}, R-squared: {r2:.2f}, 正確比率: {correct_ratio:.2f}", table_data




if __name__ == '__main__':
    app.run_server("localhost",8040 ,debug=True)
