from datetime import datetime
import pandas as pd
import os
import pandas_ta as ta
from tqdm import tqdm as tqdm
import glob


def getLatestDataV2(priceWS, dat: dict, timeFrame: str, coins: list, base: str = "BTC"):
    """Get the last row of historical data

    Args:
        dat (dict): datadict in default format
        timeFrame (str): the time format to look at

    Returns:
        (bool, dict): callback if price retrieved, updated datadict with latest data
    """
    dataSets = list(dat.keys())
    # update = getHistWSv2(coins, timeFrame, base)
    while True:
        if priceWS.updated[timeFrame]:
            update = priceWS.histData
            priceWS.updated[timeFrame] = False
            break

    for dataSet in dataSets:
        idd = dataSet.split("_")
        iddTicker = idd[0]
        iddTimeFrame = idd[1]
        if iddTimeFrame == timeFrame:
            currentDf = dat[dataSet]
            temp = update[f"{iddTicker}_{iddTimeFrame}"]
            # delete oldest
            currentDf = currentDf.iloc[1:]
            # add latest
            currentDf = pd.concat([currentDf, temp])

            if currentDf.index[-1] == currentDf.index[-2]:
                print("duplication error")
            else:
                dat[dataSet] = currentDf

    return dat