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
    sna:str
    sarea:str
    mday:str
    ar:str
    act:str
    updateTime:str
    total:int
    rent_bikes:int = Field(alias="available_rent_bikes")
    lat:float = Field(alias="latitude")
    lng:float = Field(alias="longitude")
    retuen_bikes:int = Field(alias="available_return_bikes")

    model_config = ConfigDict(
        populate_by_name=True,
    )

    @field_validator("sna",mode='before')
    @classmethod
    def flex_string(cls, value:str)->str:
        return value.split(sep="_")[-1]

class Youbike_Data(RootModel):
    root:list[Info]

def load_data()->list[dict]:
    all_data:dict[any] = __download_json()
    youbike_data:Youbike_Data = Youbike_Data.model_validate(all_data)
    data = youbike_data.model_dump()
    return data



class FilterData(object):
    @staticmethod
    def get_selected_coordinate(sna:str,data:list[dict]) -> Info:    
        right_list:list[dict] = list(filter(lambda item:True if item['sna']==sna else False ,data))
        data:dict = right_list[0]
        return Info.model_validate(data)