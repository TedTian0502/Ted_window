# Ted_window
這是自己建立的repo

## 這是什麼(作業繳交_markdown寫法)

標題:

- 這是第一排
- 這是第二排

1. 這是Python1
2. 這是Python2
3. 這是Python3

[markdown語法練習](./markdown練習/README.md)

家裡筆電登入


1.git fetch(更新完動作)

2.git pull(檔案抓下來)

安裝虛擬環境:影片_0516下午 ，長度_1:22:39

啟動虛擬環境:
conda activate venv2

接著打開 vscode，按下 CTRL+SHIFT+P，在 command palette 輸入 Python: Select Interpreter。

最後再一次 CTRL+SHIFT+P，輸入 Python: Create Terminal。
就可以在剛剛建立的虛擬環境操作了


安裝套件:
pip install -r requirements.txt

(conda install,很常失敗)
conda install --yes --file requirements.txt

克隆資料:

1.點開git bash

2.搜尋跟目錄，如GitHub

3.git clone (檔案的HTTPS)

### 0624
pgadmin與 render連結

### linux

crontab -l

crontab -r

### 0709
參考資料README.md

變更環境:venv2

venv1環境有問題

#### 網頁框架:
flask --app main run --debug

### 0711
專案繳交說明:  
1.放入'專案' 資料夾  
2.README.md介紹介面  
3.錄影時間不要超過3min

### 0715
--Render 2024_Ted_window建立:網頁站點搜尋  
1.+New ->Web Service ->Connect ->Ex:TedTian0502/Ted_window  
2.變更Name  
3.Start Command ->gunicorn  
4.Environments Variables ->NAME_OF_VARIABLE: POSTGRESQL_TOKEN  
->value: "Internal Database URL"  
5.Deploy Web Service等待"Live"  
6.更新內容->Events ->Delopy ->等待更新動作，直到"Live"  
7.網址可以貼到手機查看內容  

### 0718
上網搜尋更新下載:剪取工具slipping tool

重新錄製影片

[參考資料: Pyinstaller](https://medium.com/pyladies-taiwan/python-%E5%B0%87python%E6%89%93%E5%8C%85%E6%88%90exe%E6%AA%94-32a4bacbe351)

Web作業:繳交至網站上面

### 0726
1.把專案做到dash頁面，使用flask整合dash(css要做好)

2.tvdi_postgreSQL重建
2-1.建立新 postgreSQL(+NEW postgreSQL)
2-2.複製:External Database URL:
postgresql://
tvdi_6p3c_user:
password: gAPrDlskvZRHC29cZrYJoX5dBqZLRXFQ
@dpg-cqhficg8fa8c73brl3lg-a.singapore-postgres.render.com/
tvdi_6p3c
2-3.開啟pgadmin 資料夾右鍵點選"properties"重新更改資料
2-4.更改2024_07_02和之後有.env檔的:
2-4-1.將.env之POSTGRESQL_TOKEN更改成新的External Database URL

### 0730
連結至render，若需要多次修改requirements，想要一次更新完全，在Build Command設定

"檔案名稱"/$ pip install --upgrade pip && pip install -r requirements
