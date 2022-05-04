from datetime import datetime
from glob import glob
import os
from operator import index
from turtle import fillcolor
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
st.set_page_config(layout="wide",page_title="SageView")


figa, ax1 = plt.subplots(1,1)
figb, ax2 = plt.subplots(1,1)

base = "BTC"
print("HELLO")
listOfTradeFiles = glob("./logData/*1m.csv")
print(listOfTradeFiles)
tradesAvailable = (len(listOfTradeFiles) != 0)
if not tradesAvailable:
    trades = pd.DataFrame(columns=["timestamp",
                                      "close",
                                      "buying",
                                      "ticker",
                                      "coinAmount",
                                      "baseAmount",
                                      "profit",
                                      "timeHeld",
                                      "strategy",
                                      "failed",
                                      "slip",
                                      "BNBAmount",
                                      "base"])
else:
    lastTradeFile = latest_file = max(listOfTradeFiles, key=os.path.getctime)
    trades = pd.read_csv(lastTradeFile, index_col = 1)


totalOriginal = len(trades)

trades = trades[trades["failed"].isin([False, "False"])]

totalFailed = totalOriginal - len(trades)
totalTransactions = len(trades)
totalTrades = totalTransactions/2

bought = (trades.iloc[-1].buying)
boughtCoin = trades.iloc[-1].ticker if bought else None

totalProfit = ((trades.query("buying == False").iloc[-1].baseAmount / trades.query("buying == False").iloc[0].baseAmount)-1) * 100

listOfFiles = glob("marketData/*1m.csv")
coins = [x.replace(f"{base}_1m.csv", "").replace("marketData\\", "") for x in listOfFiles]
data = {}
for file, coin in zip(listOfFiles, coins):
    dat =  pd.read_csv(file, index_col=0)
    data[coin] = dat

# dictt = {"XLMBTC": figa, "ETHBTC": figb}
views = ["Graphs", "Dataframes"]


st.sidebar.title("SageView")
option = st.sidebar.selectbox("Choose coin to display", coins)
view = st.sidebar.radio("View Mode", views)

st.sidebar.metric(f"Base", base)
st.sidebar.metric(f"Total Profit", f"{round(totalProfit, 2)}%")
st.sidebar.metric(f"Bought", boughtCoin)
st.sidebar.metric(f"Total Transactions", totalTransactions)
st.sidebar.metric(f"Total Trades",  totalTrades)
st.sidebar.metric(f"Total Failed", totalFailed)
# print(trades.index)
# st.sidebar.metric(f"First Trade", trades.index[0])
# st.sidebar.metric(f"Last Trade", trades.index[-1])


if view == "Graphs":
    st.header(f"Coin: {option}")


    candles = go.Candlestick(x=data[option].index,
                    open=data[option]['open'],
                    high=data[option]['high'],
                    low=data[option]['low'],
                    close=data[option]['close'])

    optionTicker = option+base
    markerStyleBuy = dict(color='white',
                    size=8,
                    line=None
    )
    markerStyleSell = dict(color='black',
                    size=8,
                    line=None
    )
    if tradesAvailable:            
        buys = trades.query("ticker == @optionTicker").query("buying == True")
        sells = trades.query("ticker == @optionTicker").query("buying == False")
        buysDots = go.Scatter(x=buys.index, y=buys.close, name="buys", mode='markers', marker=markerStyleBuy)
        sellsDots = go.Scatter(x=sells.index, y=sells.close, name="sells", mode='markers', marker=markerStyleSell)
        fig = go.Figure([candles, buysDots, sellsDots])
    else:
        fig = go.Figure([candles])

    fig.update_layout(height=800)
    st.plotly_chart(fig, use_container_width=True, height=800)

else:
    # if tradesAvailable
    with st.expander(f"{option} Trades", True):
        st.dataframe(trades[trades["ticker"] == f"{option}BTC"])
    with st.expander("All Trades"):
        st.dataframe(trades)