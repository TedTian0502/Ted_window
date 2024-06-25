import requests
import pandas as pd

# Store the area names and data
sarea_list = None
data_list = None



# 能源消耗與溫室效應之間的關係
def getInfo() -> None:
    global sarea_list, data_list
    # Get data from the new URL
    url = 'https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv'
    response = requests.get(url)
    response.encoding='utf-8'
    
    if response.ok:
        file = open('a.csv',mode='w',encoding='utf-8',newline='')
        file.write(response.text)
        file.close()

    rowdata =pd.read_csv('a.csv')
    selectdata = rowdata[['country', 'year',
                          'co2', 'co2_per_capita', 'energy_per_capita', 'ghg_per_capita', 'gdp', 'population']]


    selectdata = selectdata[selectdata['year'] >= 1991]
    selectdata = selectdata.reset_index(drop=True)
    
    return selectdata




