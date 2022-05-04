from datetime import datetime
from glob import glob
import os
from operator import index
from turtle import fillcolor
import logging
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
st.set_page_config(layout="wide",page_title="SageView")



base = "BTC"

listOfFiles = glob("marketData/*1m.csv")
coins = [x.replace(f"{base}_1m.csv", "").replace("marketData\\", "").replace("marketData/", "") for x in listOfFiles]
data = {}
for file, coin in zip(listOfFiles, coins):
    dat =  pd.read_csv(file, index_col=0)
    data[coin] = dat

# dictt = {"XLMBTC": figa, "ETHBTC": figb}
views = ["Graphs", "Dataframes"]


st.sidebar.title("SageView")
option = st.sidebar.selectbox("Choose coin to display", coins)

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

fig = go.Figure([candles])

fig.update_layout(height=800)
st.plotly_chart(fig, use_container_width=True, height=800)