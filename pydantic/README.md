## 0531
### pydantic

用來驗證資料，確認資料安全性與完整性

在Pydantic中，當創建了一個模型並對其進行了驗證後，可以使用dict() 方法將該模型轉換為 Python 字典結構。

### requirements.txt
pydantic下載:
pip install -r requirements.txt

requests下載:
pip install -r requirements.txt

### json
一般工程師在交換資料使用'json'


json檔轉成python的資料結構(list,dictionary)

'json'將複雜的純字格式轉換成可視化格式，根目錄清楚明瞭
參考網址:[online json viewer](https://jsonviewer.stack.hu/)

### unit_price的字串,自動轉換為int失敗.需要手動轉換,raise validation
字串為整數(15)可以，如果為(15.5)會失敗，要寫成int(float(15.5))才可以

字串一樣不需用alias
