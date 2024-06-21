import requests
import pandas as pd

# Store the area names and data
sarea_list = None
data_list = None


def getInfo() -> None:
    global sarea_list, data_list

    rowdata =pd.read_csv('GHG_2.csv')
    # selectdata = rowdata[['country', 'year',
    #                       'co2', 'coal_co2', 'gas_co2', 'oil_co2', 'trade_co2']]
    
    # selectdata = selectdata[selectdata['year'] >= 1991]
    # selectdata = selectdata.reset_index(drop=True)
    
    return rowdata


a=getInfo()
print(a)