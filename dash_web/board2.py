# board2.py
import dash
from dash import Dash, dcc, html, dash_table
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
import os

def create_app2():
    app2 = dash.Dash(__name__, requests_pathname_prefix='/app2/', external_stylesheets=[dbc.themes.BOOTSTRAP])
    app2.title = '模型評估'

    # 設定 matplotlib 字體
    matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    matplotlib.use('Agg')

    # 載入數據集
    df = pd.read_csv(os.path.join(os.getcwd(), 'train_dataset.csv'))

    def remove_outliers(data):
        return data[(data - data.mean()).abs() < 3 * data.std()]

    df_clean = df.apply(remove_outliers)
    df_clean.dropna(inplace=True)

    def encode_image(buf):
        encoded = base64.b64encode(buf.read()).decode('ascii')
        buf.close()
        return encoded

    app2.layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("模型評估"), width=12)
        ]),
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='model-dropdown',
                options=[
                    {'label': '線性回歸(linear-regression)', 'value': 'linear-regression'},
                    {'label': 'K近鄰回歸模型(KNN)', 'value': 'knn'},
                    {'label': 'GridSearchCV(grid-search)', 'value': 'grid-search'},
                    {'label': '決策樹(decision-tree)', 'value': 'decision-tree'},
                    {'label': '隨機森林(random-forest)', 'value': 'random-forest'}
                ],
                placeholder='請選擇模型'
            ), width=6),
            dbc.Col(dcc.Input(id='threshold-input', type='number', min=0, max=0.99, step=0.01, disabled=True), width=2),
            dbc.Col(dbc.Button("查看結果", id='evaluate-button', n_clicks=0), width='auto'),
        ]),
        dbc.Row([
            dbc.Col(html.Pre(id='evaluation-result'), width=6),
            dbc.Col(html.Pre(id='selected-features'), width=6)
        ]),
        dbc.Row([
            dbc.Col(dash_table.DataTable(
                id='evaluation-table',
                columns=[
                    {'name': '模型名稱', 'id': 'model'},
                    {'name': '閾值', 'id': 'threshold'},
                    {'name': 'MSE', 'id': 'mse'},
                    {'name': 'R-squared', 'id': 'r_squared'},
                    {'name': '20%容忍範圍內的正確比率:', 'id': 'accuracy'}
                ],
                data=[]
            ), width=12)
        ])
    ])

    results_store = []
    selected_model_store = None
    last_threshold = None

    @app2.callback(
        [Output('threshold-input', 'disabled'),
        Output('threshold-input', 'value')],
        Input('model-dropdown', 'value')
    )
    def enable_threshold_input(selected_model):
        if selected_model is None:
            return True, None
        return False, last_threshold

    @app2.callback(
        [Output('evaluation-result', 'children'),
        Output('selected-features', 'children'),
        Output('evaluation-table', 'data')],
        Input('evaluate-button', 'n_clicks'),
        [State('model-dropdown', 'value'),
        State('threshold-input', 'value')]
    )
    def manage_results(evaluate_clicks, selected_model, threshold):
        global results_store, selected_model_store, last_threshold

        invalid_thresholds = ['00', '000', '01', '0001']

        if evaluate_clicks > 0:
            if selected_model is None:
                return '請先選擇模型並輸入閾值', '查看特徵數與名稱', results_store
            if threshold is None or str(threshold) in invalid_thresholds:
                return '請重新輸入閾值', '查看特徵數與名稱', results_store

            correlation_matrix = df_clean.corr().loc[:, 'PRICE']
            selected_features = correlation_matrix[correlation_matrix.abs() > threshold].index
            
            if 'PRICE' in selected_features:
                features = df_clean[selected_features].drop(columns=['PRICE'])
            else:
                features = df_clean[selected_features]

            if features.empty or 'PRICE' not in df_clean.columns:
                return '選擇的特徵中無有效數據', '查看特徵數與名稱', results_store
            
            X = features.dropna()
            y = df_clean.loc[X.index, 'PRICE']
            
            if X.empty or y.empty or X.shape[0] != y.shape[0]:
                return '特徵或目標變量無有效數據', '查看特徵數與名稱', results_store

            if selected_model == 'linear-regression':
                model = LinearRegression()
            elif selected_model == 'knn':
                model = KNeighborsRegressor()
            elif selected_model == 'grid-search':
                param_grid = {'n_neighbors': range(1, 21)}
                model = GridSearchCV(KNeighborsRegressor(), param_grid, cv=5)
            elif selected_model == 'decision-tree':
                model = DecisionTreeRegressor()
            elif selected_model == 'random-forest':
                model = RandomForestRegressor()
            else:
                return '未知模型選擇', '查看特徵數與名稱', results_store

            model.fit(X, y)
            predictions = model.predict(X)
            mse = mean_squared_error(y, predictions)
            r_squared = r2_score(y, predictions)
            
            if selected_model in ['knn', 'grid-search']:
                accuracy = "--"
            else:
                accuracy = model.score(X, y)

            if len(results_store) >= 5:
                results_store = []

            results_store.append({
                'model': selected_model,
                'threshold': threshold,
                'mse': mse,
                'r_squared': r_squared,
                'accuracy': accuracy
            })

            selected_model_store = selected_model
            last_threshold = threshold

            return (f'評估模型: {selected_model}\n'
                    f'MSE: {mse}\n'
                    f'R-squared: {r_squared}\n'
                    f'準確度: {accuracy}\n'
                    f'選擇特徵數: {len(selected_features) - 1}\n'
                    f'特徵名稱: {", ".join(selected_features[1:])}' if selected_features.shape[0] > 1 else '選擇特徵數為 0',
                    f'選擇特徵數: {len(selected_features) - 1}\n特徵名稱: {", ".join(selected_features[1:])}',
                    results_store
            )
    return app2
