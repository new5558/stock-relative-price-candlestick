import plotly.graph_objects as go

import pandas as pd
from datetime import datetime
import investpy
import streamlit as st


st.set_page_config(page_title="Ex-stream-ly Cool App", page_icon="🧊", layout="wide", initial_sidebar_state="expanded", menu_items={
    'Get Help': 'https://www.extremelycoolapp.com/help',
    'Report a bug': "https://www.extremelycoolapp.com/bug",
    'About': "# This is a header. This is an *extremely* cool app!"})


def remove_gap_from_history(hist: pd.DataFrame, fig):
    begin_date, end_date = [hist.iloc[0].name, hist.iloc[-1].name]
    hist_reindex = hist.reindex(pd.date_range(begin_date, end_date, freq='D'))
    gap_datebreaks = hist_reindex['Close'][hist_reindex['Close'].isnull()].index
    fig.update_xaxes(rangebreaks=[dict(values=gap_datebreaks)])

@st.cache
def load_stock_data(symbol: str):
    stock_df = investpy.get_stock_historical_data(stock=symbol,
    country='Thailand',
    from_date='01/01/2020',
    to_date='01/01/2021')
    return stock_df

@st.cache
def load_set_index_data():
    set_index_df = investpy.get_index_historical_data(index='SET',
    country='Thailand',
    from_date='01/01/2020',
    to_date='01/01/2021')
    return set_index_df


st.title("Stock in Thailand's relative price to SET index")

stocks_list = investpy.stocks.get_stocks_list('Thailand')
stocks_list.remove('MONTRIu')
stock_name = st.selectbox('Select stock name', stocks_list)


st.write('selected stock:', stock_name)

stock_df = load_stock_data(stock_name)
set_index_df = load_set_index_data()

option = st.radio('Options', ['Relative with SET', 'Original'])
stock_df = stock_df[['Open', 'High', 'Low', 'Close']]
set_index_df = set_index_df[['Open', 'High', 'Low', 'Close']]

result_df = stock_df / set_index_df if option == 'Relative with SET' else stock_df

fig = go.Figure(data=[go.Candlestick(x=result_df.index,
                open=result_df['Open'],
                high=result_df['High'],
                low=result_df['Low'],
                close=result_df['Close'])])

fig.update_layout(height=800)

remove_gap_from_history(stock_df, fig)

st.plotly_chart(fig, use_container_width=True)
