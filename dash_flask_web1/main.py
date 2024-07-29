from flask import Flask, render_template, request, send_from_directory
import pandas as pd
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
# from dashboard.board1 import app1
# from dashboard.board2 import app2
import dashboard
import os

# 設定資料集檔案的絕對路徑
absolute_path = os.path.join(os.getcwd(), 'train_dataset.csv')

# 檢查檔案是否存在
if os.path.exists(absolute_path):
    print("檔案存在")
    df = pd.read_csv(absolute_path)
else:
    print("檔案不存在")
    df = None

app = Flask(__name__, template_folder='templates')
application = DispatcherMiddleware(app, {
    # "/dashboard/app1": app1.server,
    # "/dashboard/app2": app2.server
})

# 圖標文件
# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static/favicon.io'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

# @app.route('/<path:filename>')
# def static_files(filename):
#     return send_from_directory(os.path.join(app.root_path, 'static/favicon.io'), filename)

@app.route('/')
def index():
    df_html = df.head(10).to_html(classes='table table-striped')
    desc_html = df.describe().to_html(classes='table table-striped')
    return render_template('index.html.jinja', table=df_html, desc=desc_html)

@app.route('/full_data')
def full_data():
    df_html = df.to_html(classes='table table-striped')
    return render_template('full_data.html.jinja', table=df_html)

@app.route('/approach')
def approach():
    return render_template('approach.html.jinja')

# @app.route('/index1')
# def index1():

if __name__ == "__main__":
    run_simple("localhost", 7070, application, use_debugger=True, use_reloader=True)
