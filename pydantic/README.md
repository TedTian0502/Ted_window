## pydantic
pydantic下載:
pip install -r requirements.txt

用來驗證資料，確認資料安全性

## requirements
requests下載:
pip install -r requirements.txt

## json
一般工程師在交換資料使用'json'


json檔轉成python的資料結構(list,dictionary)

## unit_price的字串,自動轉換為int失敗.需要手動轉換,raise validation
字串為整數(15)可以，如果為(15.5)會失敗，要寫成int(float(15.5))才可以

字串一樣不需用alias
