from flask import Flask, render_template, request
import pandas as pd
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dashboard.board1 import app1
from dashboard.board2 import app2
import data
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
    "/dashboard/app1": app1.server,
    "/dashboard/app2": app2.server
})

@app.route('/')
def index():
    df_html = df.head(10).to_html(classes='table table-striped')
    desc_html = df.describe().to_html(classes='table table-striped')
    return render_template('index.html.jinja', table=df_html, desc=desc_html)

@app.route('/full_data')
def full_data():
    df_html = df.to_html(classes='table table-striped')
    return render_template('full_data.html.jinja', table=df_html)

@app.route('/index1')
def index1():
    selected_area = request.args.get('area')
    areas = [tup[0] for tup in data.get_areas()]
    selected_area = '士林區' if selected_area is None else selected_area
    detail_snaes = data.get_snaOfArea(area=selected_area)
    
    return render_template('index1.html.jinja', areas=areas, show_area=selected_area, detail_snaes=detail_snaes)

if __name__ == "__main__":
    run_simple("localhost", 7070, application, use_debugger=True, use_reloader=True)