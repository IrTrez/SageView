import streamlit as st
import matplotlib.pyplot as plt


figa, ax1 = plt.subplots(1,1)
figb, ax2 = plt.subplots(1,1)

ax1.plot([1,2,3,4,5])
ax2.plot([5,4,3,2,1])

coins = "XLMBTC", "ETHBTC", "NANOBTC"


dictt = {"XLMBTC": figa, "ETHBTC": figb}

st.sidebar.write("hello")
option = st.sidebar.selectbox("coin", coins)

st.header(f"Coin: {option}")
st.pyplot(dictt[option])