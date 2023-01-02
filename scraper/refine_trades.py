
import os
import time
import warnings
import pandas as pd
from datetime import datetime

warnings.filterwarnings('ignore')

pwd = "/home/amir/code/copyfx/scraper/raw-trades/"

csv_list = [pwd+s for s in os.listdir(pwd)]

symbols = list()

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    for csv in csv_list:
        print("*"*120)
        df = pd.read_csv(csv)
        df.columns = ["num", "id", "datetime", "side", "lot", "symbol",
                    "enter_price", "exit_price", "commision", "pnl", "pips", "extra"]
        df.drop(columns=["num", "extra"], inplace=True)
        df = df[df["side"] != "DEPOSIT"]
        df = df[df["side"] != "WITHDRAWAL"]
        df = df.drop_duplicates(subset='id', keep="last")
        df = df.sort_values(by=["datetime"], ascending=True).reset_index(drop=True)
        # if csv.replace(pwd, "").replace(".csv", "") == "EASY124":
        #     slice = df[(df['datetime'] > "2022-09-25") & (df['datetime'] <= "2022-09-30")]
        #     print(slice[["datetime", "side", "lot", "pnl"]], "<<<<<<<<<<<<")
        df["datetime"] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S')
        winrate = len(df[df["pnl"] > 0].index)/len(df.index)
        numoftrades = len(df.index)
        df.set_index("datetime", inplace=True)
        df = df.resample("M").sum()
        df["pnlpercent"] = df["pnl"]/df["lot"]/1000
        print(csv.replace(pwd, "").replace(".csv", ""))
        print(df[["lot", "pnl", "pnlpercent"]])
        print("winrate:", winrate)
        print("numoftrades", numoftrades, "\n")
        # symbols.extend(df["symbol"].unique().tolist())

print(set(symbols))

if __name__ == '__main__':
    """Enter your login credentials here"""
    from pprint import pprint
