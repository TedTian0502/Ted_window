import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import plotly.graph_objs as go
import plotly.figure_factory as ff

# 讀取數據集
df = pd.read_csv('train_dataset.csv')

# 設置目標變數
target_column = 'PRICE'

# 分離特徵和目標變數
X = df.drop(columns=[target_column])
y = df[target_column]

# 初始化模型
models = {
    '線性回歸': LinearRegression(),
    'K近鄰回歸': KNeighborsRegressor(),
    'GridSearchCV調整的K近鄰回歸': GridSearchCV(KNeighborsRegressor(), param_grid={'n_neighbors': range(1, 21)}),
    '決策樹回歸': DecisionTreeRegressor(random_state=42),
    '隨機森林': RandomForestRegressor(n_estimators=100, random_state=42)
}

# 初始化 Dash 應用
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Nav(children=[
        html.H1('房價預測模型比較', style={'textAlign': 'center'}),
    ]),
    
    html.Div([
        dcc.Input(
            id='threshold-input',
            type='number',
            placeholder='輸入閾值 (0~9)',
            min=0, max=9, step=1
        ),
        html.Button('提交', id='submit-button', n_clicks=0),
        dcc.Graph(id='feature-distribution'),
        html.Button('開關圖表', id='toggle-button', n_clicks=0)
    ], style={'padding': '20px'}),
    
    html.Div([
        dcc.Dropdown(
            id='model-dropdown',
            options=[{'label': name, 'value': name} for name in models.keys()],
            value='線性回歸'
        ),
        html.Div(id='model-performance'),
        dcc.Graph(id='model-comparison')
    ], style={'padding': '20px'}),
    
    html.Div([
        html.H2('性能記錄'),
        html.Button('增加欄位', id='add-column-button', n_clicks=0),
        dcc.Graph(id='performance-record')
    ], style={'padding': '20px'})
])

@app.callback(
    [Output('feature-distribution', 'figure')],
    [Input('submit-button', 'n_clicks')],
    [State('threshold-input', 'value')]
)
def update_feature_distribution(n_clicks, threshold):
    if threshold is None:
        return [{}]
    
    # 選擇特徵變數
    selected_features = [col for col in X.columns if X[col].corr(y) > threshold / 10.0]
    
    # 顯示特徵變數對房價的常態分佈圖
    fig = ff.create_distplot(
        [df[feature] for feature in selected_features], 
        selected_features, 
        show_hist=False, show_rug=False
    )
    
    return [fig]

@app.callback(
    [Output('model-performance', 'children'),
     Output('model-comparison', 'figure')],
    [Input('model-dropdown', 'value'),
     Input('threshold-input', 'value')]
)
def update_dashboard(selected_model, threshold):
    if threshold is None:
        return '', {}
    
    # 選擇特徵變數
    selected_features = [col for col in X.columns if X[col].corr(y) > threshold / 10.0]
    X_selected = X[selected_features]
    
    # 分割數據
    X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)
    
    # 訓練模型並做預測
    model = models[selected_model]
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # 計算20%容忍範圍內的正確比率
    tolerance_rate = np.mean(np.abs((y_test - y_pred) / y_test) < 0.2)
    
    performance = f"均方誤差 (MSE): {mse:.2f}<br>" \
                  f"平均絕對誤差 (MAE): {mae:.2f}<br>" \
                  f"R^2: {r2:.2f}<br>" \
                  f"20%容忍範圍內的正確比率: {tolerance_rate:.2f}"
    
    # 創建性能比較圖表
    mse_values = [mean_squared_error(y_test, model.predict(X_test)) for model in models.values()]
    mae_values = [mean_absolute_error(y_test, model.predict(X_test)) for model in models.values()]
    
    figure = {
        'data': [
            go.Bar(x=list(models.keys()), y=mse_values, name='均方誤差 (MSE)'),
            go.Bar(x=list(models.keys()), y=mae_values, name='平均絕對誤差 (MAE)')
        ],
        'layout': go.Layout(
            title='模型性能比較',
            barmode='group'
        )
    }
    
    return performance, figure

@app.callback(
    Output('performance-record', 'figure'),
    [Input('add-column-button', 'n_clicks')],
    [State('threshold-input', 'value'),
     State('model-dropdown', 'value')]
)
def update_performance_record(n_clicks, threshold, selected_model):
    if threshold is None or selected_model is None:
        return {}
    
    # 更新記錄表格
    new_record = pd.DataFrame({
        '閾值': [threshold],
        '模型名稱': [selected_model],
        'MSE': [results[selected_model]['MSE']],
        'MAE': [results[selected_model]['MAE']],
        'R^2': [results[selected_model]['R^2']],
        '20%容忍範圍內的正確比率': [results[selected_model]['tolerance_rate']]
    })
    
    performance_record = pd.concat([performance_record, new_record], ignore_index=True)
    
    figure = {
        'data': [
            go.Table(
                header=dict(values=list(performance_record.columns)),
                cells=dict(values=[performance_record[col] for col in performance_record.columns])
            )
        ]
    }
    
    return figure

if __name__ == "__main__":
    app.run_server(debug=True)

    # app.run_server(host='0.0.0.0', port=8080, debug=True) #更改主機或端口

