import requests
from requests import Response
from pydantic import BaseModel, RootModel, Field,field_validator,ConfigDict

def __download_json():
    url = "	https://data.moenv.gov.tw/api/v2/wqx_p_01?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate desc&format=JSON"

    try:
        res:Response = requests.get(url)
    except Exception:
        raise Exception("連線失敗")
    else:
        all_data:dict[any] = res.json()
        return all_data
    

class Info(BaseModel):
    sitename:str #站點中文名稱
    county:str   #所在縣市
    basin:str    #河川流域
    river:str    #河流名稱
    sampledate:str #取樣日期和時間
    itemname:str   #測量項目中文名稱
    itemvalue:float #測量值
    itemunit:str  #測量單位
    

    model_config = ConfigDict(
        populate_by_name=True,
    )

    @field_validator("sitename",mode='before')
    @classmethod
    def flex_string(cls, value:str)->str:
        return value.split(sep="_")[-1]

class Water_Data(RootModel):
    root:list[Info]

def load_data()->list[dict]:
    all_data:dict[any] = __download_json()
    Water_Data_data:Water_Data = Water_Data.model_validate(all_data)
    data = Water_Data_data.model_dump()
    return data



class FilterData(object):
    @staticmethod
    def get_selected_coordinate(sitename:str,data:list[dict]) -> Info:    
        right_list:list[dict] = list(filter(lambda item:True if item['sitename']==sitename else False ,data))
        data:dict = right_list[0]
        return Info.model_validate(data)