[參考網址](https://flask.palletsprojects.com/en/3.0.x/quickstart/)

[jinja2 documentation_Template Designer Documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/)

[參考網址](https://getbootstrap.com/docs/5.3/components/navbar/)

1.註:gunicorn無法安裝

2.若要執行，必須加上"--debug"

flask --app main run --debug

3.強制關閉  
按下ctrl + c

4.Flask(__name__) #專案根目錄就在這

5.url_for 建立連結網址

6.http url寫法  
/login?name=Ted&password=1234

7.延伸模組載入: lorem，Better jinja

8.(% %) statements(敘述,不會傳出值)

9.{()} expression(運算式,傳出一段內容)

10.{%block head %}  
    block: 關鍵字  
    head: block名字

10-1.{endblock %}

11.{{ super() }}:複製架構
