import pandas as pd
from pathlib import Path
import random
import os
data_path  = Path('nate_ad_data.csv')
col_names = ['ad_id', 'price', 'is_get']

defaultPrice = 0.1
up_rate_m = 1.1
up_rate_s = 1.05
down_rate = 0.95
time_window_s = 5
time_window_m = 10

def checkFile():
    #print("check file:" , os.path.abspath(data_path))
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
    #print('[handleRequest]  enter')
    price =  decidePrice()
    insertRecord(ad_id, price)
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
    df_window_s = df.tail(time_window_s)
    print("==total record length:" , len(df))
    
    print(df_window_s)
    # total record is too small, use default price
    if  len(df) < time_window_s :
        result_price = defaultPrice
        print("init stage , use default price" , result_price)
            
    # time window record did not get any ads, up price
    elif df_window_s[df_window_s.is_get.isin([True])].empty:
        currect_tail_max = df_window_s.price.max()
        result_price = currect_tail_max * up_rate_m
        
        print("up" , result_price)

    # small time window has gotten at least one  ad, down price
    else:
        df_window_m = df.tail(time_window_m)
        
        middle_True_count = len(df_window_m[df_window_m.is_get.isin([True])])
        
        if middle_True_count / time_window_m > 0.5: #half can get
            result_price = df_window_s.price.mean()
            print("half can get , use mean" , result_price)
        else: #half can not get
            result_price = df_window_s.price.mean() * up_rate_s
            print("half can not get" , middle_True_count)

    return round(result_price , 3)



for i in range(0,5):
    handleRequest(i)
