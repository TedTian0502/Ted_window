from flask import Flask, render_template, request
import pandas as pd
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dashboard.board1 import app1
from dashboard.board2 import app2
import data
import dashboard
import os

app = Flask(__name__)
application = DispatcherMiddleware(app, {
    "/dashboard/app1": app1.server,
    "/dashboard/app2": app2.server
})

@app.route("/")
def index():
    # 檢查檔案是否存在
    absolute_path = os.path.abspath('dash_flask_web1/train_dataset.csv')
    print(f"檔案位置: {absolute_path}")
    
    # 讀取數據集
    df = pd.read_csv(absolute_path)
    # 獲取描述性統計信息
    desc = df.describe()
    # 將數據集和描述性統計信息轉換為HTML
    df_html = df.to_html(classes='table table-striped')
    desc_html = desc.to_html(classes='table table-striped')
    return render_template('index.html', table=df_html, desc=desc_html)

@app.route("/index1")
def index1():
    selected_area = request.args.get('area')
    areas = [tup[0] for tup in data.get_areas()]
    selected_area = '士林區' if selected_area is None else selected_area
    detail_snaes = data.get_snaOfArea(area=selected_area)
    
    return render_template('index1.html.jinja', areas=areas, show_area=selected_area, detail_snaes=detail_snaes)

if __name__ == "__main__":
    run_simple("localhost", 7070, application, use_debugger=True, use_reloader=True)
