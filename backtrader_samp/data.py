import os
import pandas as pd
import numpy as np
from pymongo import MongoClient


BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
GammaCSV_DIR = os.path.join(BASE_DIR, "Gamma_data.csv")

"""to connect FuturesDataOHLCV-database and return OHLCV dataframe for Futures Data"""
def getOHLCV(fromts:int,        # ms
            tots:int,           # ms
            time_scale:str,     # '1min','15min','1H'
            symbol: str):       # 'BTCUSDT'   

    client  = MongoClient(host  ='192.168.11.66',
                        port    =27017,
                        username='ayat',
                        password='amir1374')
    db      = client['FuturesDataOHLCV']
    col     = db['OHLCV']
    query   = [
        {
            '$match': {
                'timestamp': {
                    '$gte'                      : fromts, 
                    '$lte'                      : tots
                }, 
                'time_scale'                    : time_scale,
                'symbol'                        : symbol
            }
        }, {
            '$sort': {
                'timestamp'                     : 1
            }
        }, {
            '$project': {
                '_id'                           : 0,
                'symbol'                        : 0,
                'time_scale'                    : 0,
                'volume'                        : 0,
                'Quote_asset_volume'            : 0,
                'Number_of_trades'              : 0,
                'Taker_buy_base_asset_volume'   : 0,
                'Taker_buy_quote_asset_volume'  : 0,
                'Ignore'                        : 0
            }
        }
    ]
    df = pd.DataFrame(list(col.aggregate(query)))
    return df

"""to get signal from db"""
def getforesightPredict(fromts:int,tots:int):
    client  = MongoClient(host  ='192.168.11.81',
                        port    =27017,
                        username='ayat',
                        password='r7f6H5nS3bA63w2')
    db      = client['foresight']
    col     = db['bitcoin_results']

    query   = [
        {
            '$match': {
                'timestamp_predict': {
                    '$gte'                      : fromts, 
                    '$lte'                      : tots
                }
            }
        }, {
            '$sort': {
                'timestamp_predict'             : 1
            }
        }, {
            '$project': {
                '_id'                           : 0, 
                'symbol'                        : 0, 
                'time_scale'                    : 0, 
                'timestamp_runat'               : 0,
                'open_prediction'               : 0,
                'close_prediction'              : 0
            }
        }
    ]

    df      = pd.DataFrame(list(col.aggregate(query)))
    columns = [
        'timestamp_predict',
        'high_prediction',
        'low_prediction',
    ]
    dftypes={
        'timestamp_predict'  : int,
        'high_prediction'    : float,
        'low_prediction'     : float,
    }
    df = df[columns]
    df = df.astype(dftypes)
    return df


"""to get signal from db"""
def dataPrepration( fromts : int, 
                    tots   : int,
                    symbol : int):
    minute_df = getOHLCV(fromts,
                        tots+3540000,
                        "1min",
                        symbol)
    columns   = {'timestamp'	    : 'datetime',
                'open_price'        : 'open',
                'high_price'        : 'high',
                'low_price'         : 'low',
                'close_price'       : 'close',}
    minute_df = minute_df.rename(columns=columns)
    minute_df['datetime'] = minute_df['datetime'].map(lambda x: int(x/1000))

    HpLp_df   = getforesightPredict(fromts,tots)
    HpLp_df   = HpLp_df.drop(columns=['timestamp_predict'])
    columns   = {'high_prediction'	: 'Hp',
                'low_prediction'    : 'Lp'}
    HpLp_df   = HpLp_df.rename(columns=columns)
    HpLp_df   = pd.DataFrame(np.repeat(HpLp_df.values, 60, axis=0), columns=HpLp_df.columns)

    df        = pd.concat([minute_df, HpLp_df], axis=1)
    return df

if __name__=="__main__":
    df = dataPrepration(1630490400000,1631700000000,"BTCUSDT")
    df.to_csv(GammaCSV_DIR,index=False)