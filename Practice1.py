import streamlit as st
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objs as go

import appdirs as ad
ad.user_cache_dir = lambda *args: "/tmp"
import yfinance as yf    

# Specify title and logo for the webpage.
# Set up your web app
st.set_page_config(layout="wide", page_title="WebApp_Demo")

# Sidebar
st.sidebar.title("Ticker")
with st.sidebar.form(key='my_form'):
    symbol = st.sidebar.text_input('Please enter the stock symbol: ', 'NVDA').upper()
    submitted = st.form_submit_button(label="Submit")
    col1, col2 = st.sidebar.columns(2, gap="medium")
    with col1:
      sdate = st.date_input('Start Date',value=datetime.date(2020,1,1))
    with col2:
      edate = st.date_input('End Date',value=datetime.date(2023,12,1))

if submitted:
   st.title(f"{symbol}")
   stock = yf.Ticker(symbol)
if stock is not None:
  # Display company's basics
  st.write(f"# Sector : {stock.info['sector']}")
  st.write(f"# Company Beta : {stock.info['beta']}")
  st.write(f"Market Cap : {stock.info['marketCap']}")
else:
  st.error("Failed to fetch historical data.")

data = yf.download(symbol,start=sdate,end=edate)
if data is not None:
  fig = go.Figure(data=[go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'])])
  fig.update_layout(title=f"{symbol}", yaxis_title="Price", xaxis_title="Date")
  st.plotly_chart(fig)
else:
  st.error("Failed to fetch historical data.")
