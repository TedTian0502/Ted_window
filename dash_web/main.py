from flask import Flask, render_template, request, send_from_directory
import pandas as pd
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dashboard.board1 import app1
from dashboard.board2 import app2
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

app = Flask(__name__)
application = DispatcherMiddleware(app,{
    "/dashboard/app1":app1.server,
    "/dashboard/app2":app2.server
})

@app.route("/")
def index():
    return render_template("index.html.jinja")

@app.route("/approach")
def approach():
    return render_template("approach.html.jinja")

@app.route('/full_data')
def full_data():
    df_html = df.to_html(classes='table table-striped')
    return render_template('full_data.html.jinja', table=df_html)

 
    
    


if __name__ == "__main__":
    run_simple("localhost", 8080, app,use_debugger=True,use_reloader=True)