from datetime import datetime, timedelta
import time
import plotly.graph_objects as go

import pandas as pd

from pricewebsocket import priceDataWS


# fig = go.Figure()
fig = go.Candlestick()

df = pd.DataFrame()
coins = ["XLM"]
intervals = ["1m"]
ws = priceDataWS(coins, intervals)
fig.add_candlestick()
# # fig
fig.show()
while True:
    time.sleep(0.1)
    if ws.updated["1m"]:
        print(f"update {datetime.now()}")
        update = ws.histData
        ws.updated["1m"] = False

        temp = update[f"XLMBTC_1m"]

        df = pd.concat([df, temp])
        fig.add_candlestick(x=temp.index,
            open=temp['open'],
            high=temp['high'],
            low=temp['low'],
            close=temp['close'])
