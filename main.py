import plotly.graph_objects as go

import pandas as pd
from datetime import datetime
import investpy
import streamlit as st
from datetime import datetime, timedelta
import pandas_ta as ta


def remove_gap_from_history(hist: pd.DataFrame, fig: go.Figure) -> None:
    begin_date, end_date = [hist.iloc[0].name, hist.iloc[-1].name]
    hist_reindex = hist.reindex(pd.date_range(begin_date, end_date, freq='D'))
    gap_datebreaks = hist_reindex['Close'][hist_reindex['Close'].isnull()].index
    fig.update_xaxes(rangebreaks=[dict(values=gap_datebreaks)])

def get_date(lookback_days: int) -> [str, str]:
    today = datetime.today()
    today_lastyear = today - timedelta(days=lookback_days)
    return today.strftime('%d/%m/%Y'), today_lastyear.strftime('%d/%m/%Y')

@st.cache
def load_stock_data(symbol: str, today: str, today_lastyear: str) -> pd.DataFrame: 
    stock_df = investpy.get_stock_historical_data(stock=symbol,
    country='Thailand',
    from_date=today_lastyear,
    to_date=today)
    return stock_df

@st.cache
def load_set_index_data(today: str, today_lastyear: str) -> pd.DataFrame:
    set_index_df = investpy.get_index_historical_data(index='SET',
    country='Thailand',
    from_date=today_lastyear,
    to_date=today)
    return set_index_df

@st.cache
def data_transformation(stock_name: str, lookback_days: int) -> pd.DataFrame:
    today, today_lastyear = get_date(lookback_days)
    stock_df = load_stock_data(stock_name, today, today_lastyear)
    set_index_df = load_set_index_data(today, today_lastyear)

    stock_df = stock_df[['Open', 'High', 'Low', 'Close']]
    set_index_df = set_index_df[['Open', 'High', 'Low', 'Close']]

    result_df = stock_df / set_index_df if option == 'Relative with SET' else stock_df
    
    result_df["EMA200"] = ta.ema(result_df["Close"], length=200)
    return result_df

title = "Stock in Thailand's relative price to SET index"

st.set_page_config(page_title=title, page_icon="💎", layout="wide", initial_sidebar_state="expanded")

st.title(title)

stocks_list = investpy.stocks.get_stocks_list('Thailand')
stocks_list.remove('MONTRIu')
stock_name = st.sidebar.selectbox('Select stock name', stocks_list)

st.header('Symbol: ' + stock_name)

option = st.sidebar.radio('Options', ['Relative with SET', 'Original'])
lookback_days = st.sidebar.number_input('Lookback days', value = 365)

st.sidebar.write("![github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)  [Project's repo](https://github.com/new5558/stock-relative-price-candlestick)")

result_df = data_transformation(stock_name, lookback_days)

fig = go.Figure(data=[go.Candlestick(x=result_df.index,
                open=result_df['Open'],
                high=result_df['High'],
                low=result_df['Low'],
                close=result_df['Close'], name="Candle stick"), 
                go.Scatter(x=result_df.index, y=result_df['EMA200'], line=dict(color='orange', width=2), name="EMA200")])

fig.update_layout(height=800)

remove_gap_from_history(result_df, fig)

st.plotly_chart(fig, use_container_width=True)

