import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask import Flask, render_template
import os
import pandas as pd

# 從 dashboard 目錄中引入應用程式
from dashboard.board import app1  # 引入第一個 Dash 應用程式
from dashboard.board1 import app2  # 引入第二個 Dash 應用程式

# 創建 Flask 應用程式實例
application = Flask(__name__)

# 創建主 Dash 應用程式
app = dash.Dash(__name__, server=application,suppress_callback_exceptions=True)

# 定義 Dash 應用程式的佈局
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='應用程式 1', value='app1'),
        dcc.Tab(label='應用程式 2', value='app2'),
    ],
    id='tabs'
    ),
    html.Div(id='tabs-content')
])

# 定義回調函數來切換應用程式頁面
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_page(tab_name):
    if tab_name == 'app1':
        return dcc.Location(pathname='/app1', id='app1')
    elif tab_name == 'app2':
        return dcc.Location(pathname='/app2', id='app2')

# 使用 DispatcherMiddleware 將 Dash 應用程式和 Flask 應用程式結合在一起
app_server = DispatcherMiddleware(application, {
    '/app1': app1.server,
    '/app2': app2.server
})

# 設定資料集檔案的絕對路徑
absolute_path = os.path.join(os.getcwd(), 'train_dataset.csv')

# 檢查檔案是否存在
if os.path.exists(absolute_path):
    print("檔案存在")
    df = pd.read_csv(absolute_path)
else:
    print("檔案不存在")
    df = None

# 使用 Flask 定義路由
@application.route("/")
def index():
    return render_template("index.html.jinja")

@application.route("/approach")
def approach():
    return render_template("approach.html.jinja")

@application.route('/full_data')
def full_data():
    df_html = df.to_html(classes='table table-striped')
    return render_template('full_data.html.jinja', table=df_html)

if __name__ == '__main__':
    # 啟動伺服器
    run_simple('localhost', 8050, app_server, use_reloader=True, use_debugger=True)
