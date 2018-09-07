import pandas as pd
from pathlib import Path
import random
import os
data_path  = Path('nate_ad_data.csv')
col_names = ['ad_id', 'price', 'is_get']

defaultPrice = 0.1
up_rate = 1.08
down_rate = 0.95
time_window = 5

def checkFile():
    print("[checkFile]")
    print("file:" , os.path.abspath(data_path))
    if not data_path.exists():
        df  = pd.DataFrame(columns = col_names)
        df.to_csv(data_path , index=False)

def insertRecord(ad_id, price, is_get = False):
    checkFile()
    
    ad_id = int(ad_id)
    s = pd.Series({'ad_id': ad_id, 'price': price, 'is_get': is_get })

    df = pd.read_csv(data_path)
    df = df.append(s, ignore_index = True)
    #print(df)
    df.to_csv(data_path , index = False)


def handleRequest(ad_id):
    print('[handleRequest]  enter')
    price =  decidePrice()
    insertRecord(ad_id, price)
    print('[handleRequest] end')
    return price


def updateRecord(ad_id, is_get = True):
    ad_id = int(ad_id)
    checkFile()
    df = pd.read_csv(data_path)
    df.loc[df['ad_id'] == ad_id, 'is_get'] = is_get
    df.to_csv(data_path , index = False)


def decidePrice():
    checkFile()
    
    df = pd.read_csv(data_path)
    look_df = df.tail(time_window)
    print("==")
    
    if  look_df.size < time_window :
        result_price = defaultPrice
            
    elif look_df[look_df.is_get.isin([True])].empty:
        currect_tail_max = look_df.price.max()
        result_price = currect_tail_max * up_rate
        
        print("up" , result_price)

    else:
        currect_tail_max = look_df.price.max()
        result_price = currect_tail_max * down_rate
        print("down" , result_price) 

    
    return round(result_price , 3)

