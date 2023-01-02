
import time
import pandas as pd



# df = pd.read_csv("trades.csv", header=None, names=["num","time","side","lot","sym","o","c","pip","size","pips"])
df = pd.read_csv("FASTWAY.csv")
# df = pd.read_csv("FASTWAYINETH.csv")
# df = pd.read_csv("NORTHEASTWAYINBTC.csv")
df.drop(columns=["num"], inplace=True)
pd.to_datetime(df["time"])
df.sort_values(by=["time"], inplace=True)
df.set_index(pd.DatetimeIndex(df["time"]), inplace=True)
df.drop(columns=["time"], inplace=True)

pnl = df["size"].astype(float).sum()

deposit_df  = df[df["side"]=="DEPOSIT"]
deposit     = deposit_df["sym"].astype(float).sum()

withdraw_df = df[df["side"]=="WITHDRAWAL"]
withdraw    = withdraw_df["sym"].astype(int).sum()

trade_df    = df[df["side"]!="DEPOSIT"]
trade_df    = trade_df[trade_df["side"]!="WITHDRAWAL"]
n_trade_df  = trade_df[trade_df["size"]<0]
p_trade_df  = trade_df[trade_df["size"]>0]
trade_df["side"].astype(str)
monthly_pnl = trade_df["size"].resample("M").sum()
monthly_negative_pnl = n_trade_df["size"].resample("M").sum()
monthly_positive_pnl = p_trade_df["size"].resample("M").sum()

print("********************************************************************trades")
print(trade_df)
print("********************************************************************deposit")
print(deposit_df)
print("********************************************************************withdraw")
print(withdraw_df)

print("********************************************************************negative_pnl")
print(monthly_negative_pnl)
print("********************************************************************positive_pnl")
print(monthly_positive_pnl)
print("********************************************************************pnl")
print(monthly_pnl)
print("********************************************************************pnl")
print(pnl)

# print(trade_df["2022-02-28":"2022-03-31"])

# print(trade_df.dtypes)