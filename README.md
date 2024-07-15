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
conda activate venv1

安裝套件:
pip install -r requirements.txt

(conda install,很常失敗)
conda install --yes --file requirements.txt

克隆資料:

1.點開git bash

2.搜尋跟目錄，如GitHub

3.git clone (檔案的HTTPS)

### linux

crontab -l

crontab -r

### 0709
參考資料README.md

變更環境:venv2

venv1環境有問題

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