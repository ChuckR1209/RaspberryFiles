#!/usr/bin/env python
# coding: utf-8

# ## This is to test to bring trading view signals 
# https://python-tradingview-ta.readthedocs.io/en/latest/overview.html#installation
# 
# Has all trading view signals with recommendation

# In[2]:


from __future__ import print_function


# ### Get all stock symbol tickers
# https://levelup.gitconnected.com/how-to-get-all-stock-symbols-a73925c16a1b

# #### You can search on https://tvdb.brianthe.dev to see which symbol, exchange, and screener to use.

# In[1]:
import importlib
import tradingview_ta
from tradingview_ta import TA_Handler, Interval, Exchange



# In[2]:


# Import date class from datetime module
from datetime import date


# In[3]:


today = date.today() 
print(today)


# In[4]:


import requests


# In[5]:


# to get all stock symbols from Yahoo
# pip install yahoo-fin
import pandas as pd
#yf = importlib.import_module("yahoo-finance")
#import yahoo_fin as yf
from yahoo_fin import stock_info as si


# In[6]:


tesla = TA_Handler(
    symbol="TSLA",
    screener="america",
    exchange="NASDAQ",
    interval=Interval.INTERVAL_1_DAY
)
print(tesla.get_analysis().summary)
tesla_dict = tesla.get_analysis().summary
tesla_dict['symbol'] = "TSLA"
tesla_dict['screener'] = "america"
tesla_dict['exchange'] = "NASDAQ"
tesla_dict['interval'] = "Interval.INTERVAL_1_DAY"


# Example output: {"RECOMMENDATION": "BUY", "BUY": 8, "NEUTRAL": 6, "SELL": 3}


# In[7]:


tesla_dict['RECOMMENDATION']


# In[8]:


print(type(tesla_dict))


# In[ ]:





# In[9]:


#teslaDF = pd.DataFrame.from_dict(tesla_dict, index=[0])
teslaDF = pd.DataFrame(tesla_dict,index=[0] )  
print(type(tesla_dict))


# In[10]:


teslaDF.head()


# In[11]:


# data = {'name': ['nick', 'david', 'joe', 'ross'],
#         'age': ['5', '10', '7', '6']} 
# new = pd.DataFrame.from_dict(data)


# In[12]:


drv = TA_Handler(
    symbol="DRV",
    screener="america",
    exchange="AMEX",
    interval=Interval.INTERVAL_1_DAY
)
print(drv.get_analysis().summary)


# In[13]:


print(drv.get_analysis().oscillators)


# In[14]:


print(drv.get_analysis().moving_averages)


# #### Checking the version

# In[15]:


print(tradingview_ta.__version__)
# Example output: 3.1.3


# #### You can search on https://tvdb.brianthe.dev to see which symbol, exchange, and screener to use.

# In[44]:


handler = TA_Handler(
    symbol="MATICUSDC",
    exchange="KUCOIN",
    screener="crypto",
    interval="1D",
    timeout=None
)


# In[45]:


analysis = handler.get_analysis()


# analysis.symbol

# In[46]:


analysis.indicators["RSI"]


# In[47]:


analysis.indicators["MACD.macd"]


# In[48]:


analysis.time


# In[49]:


analysis.indicators["close"]


# In[50]:


print(handler.get_analysis().summary)


# In[51]:


analysis.indicators


# In[52]:


bbHigh = analysis.indicators['BB.upper']
bbHigh


# In[25]:


close = analysis.indicators['close']
close


# In[26]:


sma30 = analysis.indicators['SMA30']
sma30


# In[27]:


sma10 = analysis.indicators['SMA10']
sma10


# In[28]:


bbLow = analysis.indicators['BB.lower']
bbLow


# In[29]:


percInc30 = (close/sma30 * 100) - 100
percInc30


# In[30]:


percInc10 = (close/sma10 * 100) - 100
percInc10


# In[31]:


handler.indicators


# ### Will try signals from here 
# https://taapi.io/indicators/pivot-points/

# import requests
# 
# api_url = "https://jsonplaceholder.typicode.com/todos/1"
# 
# response = requests.get(api_url)
# 
# response.json()

# In[32]:


#key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjM0M2I3ZDJmYzVhOGFkZmVjMGQ4ZWRkIiwiaWF0IjoxNjY1MzgyMzU0LCJleHAiOjMzMTY5ODQ2MzU0fQ.HhWHtfPHLf_dtIAjZLC1qtD49ZFpzkz-CXVJuBdwjzo'


# In[33]:


#key=....

# #### [GET] https://api.taapi.io/pivotpoints?secret=MY_SECRET&exchange=binance&symbol=BTC/USDT&interval=1h

# In[34]:


#api_url = f"https://api.taapi.io/pivotpoints?secret={key}&exchange=binance&symbol=BTC/USDT&interval=1w"


# In[35]:


#api_url


# In[36]:


#response = requests.get(api_url)
#response


# In[37]:


#response.json()


# ## get all symbols from Yahoo

# #### There are three major stock exchanges in the US. They are the Dow, NASDAQ and S&P 500. There is a fourth category of symbols called “others”. We download each category of lists to separate pandas dataframes.

# In[17]:


df1 = pd.DataFrame( si.tickers_sp500() )
df2 = pd.DataFrame( si.tickers_nasdaq() )
df3 = pd.DataFrame( si.tickers_dow() )
df4 = pd.DataFrame( si.tickers_other() )


# #### Next, we convert each dataframe to a list, then to a set.

# In[18]:


sym1 = set( symbol for symbol in df1[0].values.tolist() )
sym2 = set( symbol for symbol in df2[0].values.tolist() )
sym3 = set( symbol for symbol in df3[0].values.tolist() )
sym4 = set( symbol for symbol in df4[0].values.tolist() )


# In[19]:


#sym1


# #### Stock symbols may be listed on more than one exchange. We join the four sets into one. Because it is a set, there will be no duplicate symbols.

# In[20]:


symbols = set.union( sym1, sym2, sym3, sym4 )


# #### Most symbols are up to four letters in length, ie: MSFT for Microsoft. There are some symbols that have a fifth letter. A fifth letter is mostly added to stocks that are delinquent in certain exchange requirements. We’ll identify four of those suffixes for deletion.

# In[21]:


my_list = ['W', 'R', 'P', 'Q']


# 
# W means there are outstanding warrants. We don’t want those.
# R means there is some kind of “rights” issue. Again, not wanted.
# P means “First Preferred Issue”. Preferred stocks are a separate entity.
# Q means bankruptcy. We don’t want those, either.

# We need to initiate two sets; a save set and a delete set.

# In[22]:


del_set = set()
sav_set = set()
del_set_nasdaq = set()
sav_set_nasdaq = set()
del_set_spx = set()
sav_set_spx = set()


# Next, we find the symbols over four characters in length AND have their last letter in my_list. When found, they are added to del_set. All other symbols are added to sav_set.

# In[23]:


for symbol in symbols:
    if len( symbol ) > 4 and symbol[-1] in my_list:
        del_set.add( symbol )
    else:
        sav_set.add( symbol )


# In[24]:


# ONly SPX
for symbol in sym1:
    if len( symbol ) > 4 and symbol[-1] in my_list:
        del_set_spx.add( symbol )
    else:
        sav_set_spx.add( symbol )


# In[25]:


# ONly Nasdaq
for symbol in sym2:
    if len( symbol ) > 4 and symbol[-1] in my_list:
        del_set_nasdaq.add( symbol )
    else:
        sav_set_nasdaq.add( symbol )


# In[26]:


print( f'ALL Removed {len( del_set )} unqualified stock symbols...' )
print( f'ALL There are {len( sav_set )} qualified stock symbols...' )


# In[27]:


print( f'SPX Removed {len( del_set_spx )} unqualified stock symbols...' )
print( f'SPX There are {len( sav_set_spx )} qualified stock symbols...' )


# In[28]:


print( f'Nasdaq Removed {len( del_set_nasdaq )} unqualified stock symbols...' )
print( f'Nasdaq There are {len( sav_set_nasdaq )} qualified stock symbols...' )


# In[50]:


# for ss in sav_set_spx:
#     print(ss)

# First try NYSE and then if not NASDAQ. Else if both in error print error and move on to next symbol
spx_dict_final = {}

#column_names = ["Symbol", "RECOMMENDATION", "BUY", "SELL", "NEUTRAL", "screener", "exchange", "interval" ]
column_names = ["Symbol", "RECOMMENDATION", "BUY", "SELL", "NEUTRAL", "ClosePrice", "percInc30", "percInc10", "bbHigh", "bbLow", "screener", "exchange", "interval" ]

spx_df = pd.DataFrame(columns = column_names)

i = 0
for ss in sav_set_spx:
    i = i + 1
    print(i)
    #print(ss)
    output = TA_Handler(
    symbol=ss,
    screener="america",
    #exchange="NASDAQ",
    exchange="NYSE",
    interval=Interval.INTERVAL_1_DAY)
    print("symbol = "+ss)
    try:
        analysis = output.get_analysis()
        bbLow = analysis.indicators['BB.lower']
        bbHigh = analysis.indicators['BB.upper']
        close = analysis.indicators['close']
        sma30 = analysis.indicators['SMA30']
        sma10 = analysis.indicators['SMA10']
        percInc30 = (close/sma30 * 100) - 100
        percInc10 = (close/sma10 * 100) - 100        
        print(output.get_analysis().summary)
        dict1 = output.get_analysis().summary
        spx_df = spx_df.append({'Symbol': ss, 'RECOMMENDATION' :dict1['RECOMMENDATION'], 'BUY': dict1['BUY'], 
                               'SELL': dict1['SELL'], 'NEUTRAL': dict1['NEUTRAL'], 
                                'ClosePrice': close, 'percInc30': percInc30, 'percInc10': percInc10,'bbHigh': bbHigh, 'bbLow': bbLow,
                                'screener' : "america",
                               'exchange' : "NYSE", 'interval': "Interval.INTERVAL_1_DAY"}, ignore_index=True)

    except Exception as error_message:
        output = TA_Handler(
        symbol=ss,
        screener="america",
        exchange="NASDAQ",
        #exchange="NYSE",
        interval=Interval.INTERVAL_1_DAY)
        try:
            analysis = output.get_analysis()
            bbLow = analysis.indicators['BB.lower']
            bbHigh = analysis.indicators['BB.upper']
            close = analysis.indicators['close']
            sma30 = analysis.indicators['SMA30']
            sma10 = analysis.indicators['SMA10']
            percInc30 = (close/sma30 * 100) - 100
            percInc10 = (close/sma10 * 100) - 100            
            print(output.get_analysis().summary)
            dict1 = output.get_analysis().summary
            spx_df = spx_df.append({'Symbol': ss, 'RECOMMENDATION' :dict1['RECOMMENDATION'], 'BUY': dict1['BUY'], 
                               'SELL': dict1['SELL'], 'NEUTRAL': dict1['NEUTRAL'], 
                                'ClosePrice': close, 'percInc30': percInc30, 'percInc10': percInc10,'bbHigh': bbHigh, 'bbLow': bbLow,    
                                'screener' : "america",
                               'exchange' : "NASDAQ", 'interval': "Interval.INTERVAL_1_DAY"}, ignore_index=True)
            # spx_dict['symbol'] = ss
            # spx_dict['screener'] = "america"
            # spx_dict['exchange'] = "NYSE"
            # spx_dict['interval'] = "Interval.INTERVAL_1_DAY"
        except Exception as error_message:
            print('ERROR', error_message)
            error = 1  
    #if i == 5:
        #break


# In[51]:


# df = pd.DataFrame(columns=['A'])
# >>> for i in range(5):
# ...     df = df.append({'A': i}, ignore_index=True)


# In[52]:


spx_df.head()


# In[53]:



len(spx_df)

# for ss in sav_set_nasdaq:
#     print(ss)


# In[54]:


spx_df_strongBuy = spx_df[spx_df['RECOMMENDATION'] == "STRONG_BUY"]


# In[55]:


len(spx_df_strongBuy)


# In[56]:


spx_df_strongBuy = spx_df_strongBuy.sort_values(by='BUY', ascending=False)


# In[57]:


## Print all the dataFrame
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 4, 'expand_frame_repr', False
                       ):
    print(spx_df_strongBuy)


# In[58]:


spxStrongBuyFile = f"../RaspberryFiles/Files/spxStrongBuyFile_{today}.csv"
spxStrongBuyFile


# In[59]:


spx_df_strongBuy.to_csv(spxStrongBuyFile, index=False)


# In[60]:


spx_df_strongSell = spx_df[spx_df['RECOMMENDATION'] == "STRONG_SELL"]


# In[61]:


len(spx_df_strongSell)


# In[62]:


spx_df_strongSell = spx_df_strongSell.sort_values(by='SELL', ascending=False)


# In[63]:


spxStrongSellFile = f"../RaspberryFiles/Files/spxStrongSellFile_{today}.csv"
spxStrongSellFile


# In[64]:


spx_df_strongSell.to_csv(spxStrongSellFile, index=False)


# In[65]:


## Print all the dataFrame
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 4, 'expand_frame_repr', False
                       ):
    print(spx_df_strongSell)


# In[66]:


## Print all the dataFrame
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 4, 'expand_frame_repr', False
                       ):
    print(spx_df)


# In[67]:


spxFile = f"../RaspberryFiles/Files/spx_df_{today}.csv"
spxFile


# In[68]:


spx_df.to_csv(spxFile, index=False)


# ### NASDAQ 

# In[29]:


# for ss in sav_set_spx:
#     print(ss)



#column_names = ["Symbol", "RECOMMENDATION", "BUY", "SELL", "NEUTRAL", "screener", "exchange", "interval" ]
column_names = ["Symbol", "RECOMMENDATION", "BUY", "SELL", "NEUTRAL", "ClosePrice", "percInc30", "percInc10", "bbHigh", "bbLow", "screener", "exchange", "interval" ]

nasdaq_df = pd.DataFrame(columns = column_names)

i = 0
for ss in sav_set_nasdaq:
    i = i + 1
    print(i)
    #print(ss)
    output = TA_Handler(
    symbol=ss,
    screener="america",
    #exchange="NASDAQ",
    exchange="NYSE",
    interval=Interval.INTERVAL_1_DAY)
    print("symbol = "+ss)
    try:
        analysis = output.get_analysis()
        bbLow = analysis.indicators['BB.lower']
        bbHigh = analysis.indicators['BB.upper']
        close = analysis.indicators['close']
        sma30 = analysis.indicators['SMA30']
        sma10 = analysis.indicators['SMA10']
        percInc30 = (close/sma30 * 100) - 100
        percInc10 = (close/sma10 * 100) - 100         
        print(output.get_analysis().summary)
        dict1 = output.get_analysis().summary
        nasdaq_df = nasdaq_df.append({'Symbol': ss, 'RECOMMENDATION' :dict1['RECOMMENDATION'], 'BUY': dict1['BUY'], 
                               'SELL': dict1['SELL'], 'NEUTRAL': dict1['NEUTRAL'], 
                                      'ClosePrice': close, 'percInc30': percInc30, 'percInc10': percInc10,'bbHigh': bbHigh, 'bbLow': bbLow,
                                      'screener' : "america",
                               'exchange' : "NYSE", 'interval': "Interval.INTERVAL_1_DAY"}, ignore_index=True)

    except Exception as error_message:
        output = TA_Handler(
        symbol=ss,
        screener="america",
        exchange="NASDAQ",
        #exchange="NYSE",
        interval=Interval.INTERVAL_1_DAY)
        try:
            analysis = output.get_analysis()
            bbLow = analysis.indicators['BB.lower']
            bbHigh = analysis.indicators['BB.upper']
            close = analysis.indicators['close']
            sma30 = analysis.indicators['SMA30']
            sma10 = analysis.indicators['SMA10']
            percInc30 = (close/sma30 * 100) - 100
            percInc10 = (close/sma10 * 100) - 100             
            print(output.get_analysis().summary)
            dict1 = output.get_analysis().summary
            nasdaq_df = nasdaq_df.append({'Symbol': ss, 'RECOMMENDATION' :dict1['RECOMMENDATION'], 'BUY': dict1['BUY'], 
                               'SELL': dict1['SELL'], 'NEUTRAL': dict1['NEUTRAL'], 
                               'ClosePrice': close, 'percInc30': percInc30, 'percInc10': percInc10,'bbHigh': bbHigh, 'bbLow': bbLow,           
                                          'screener' : "america",
                               'exchange' : "NASDAQ", 'interval': "Interval.INTERVAL_1_DAY"}, ignore_index=True)
            # spx_dict['symbol'] = ss
            # spx_dict['screener'] = "america"
            # spx_dict['exchange'] = "NYSE"
            # spx_dict['interval'] = "Interval.INTERVAL_1_DAY"
        except Exception as error_message:
            print('ERROR', error_message)
            error = 1  
    #if i == 5:
        #break


# In[30]:


len(nasdaq_df)


# In[31]:


nasdaq_df_strongBuy = nasdaq_df[nasdaq_df['RECOMMENDATION'] == "STRONG_BUY"]


# In[32]:


nasdaq_df_strongBuy = nasdaq_df_strongBuy.sort_values(by=(['percInc10', 'percInc30', 'BUY']), ascending=[False, False, False])


# In[33]:


len(nasdaq_df_strongBuy)


# In[34]:


## Print all the dataFrame
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 4, 'expand_frame_repr', False
                       ):
    print(nasdaq_df_strongBuy)


# In[35]:


filename1 = f"../RaspberryFiles/Files/NasdaqStrongBuy-{today}.csv"
filename1


# In[36]:


nasdaq_df_strongBuy.to_csv(filename1,index=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


nasdaq_df_strongSell = nasdaq_df[nasdaq_df['RECOMMENDATION'] == "STRONG_SELL"]


# In[ ]:


nasdaq_df_strongSell = nasdaq_df_strongSell.sort_values(by=(['percInc10', 'percInc30', 'SELL']), ascending=[True, True, False])


# In[ ]:


len(nasdaq_df_strongSell)


# In[ ]:


## Print all the dataFrame
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 4, 'expand_frame_repr', False
                       ):
    print(nasdaq_df_strongSell)


# In[ ]:

filename2 = f"../RaspberryFiles/Files/NasdaqStrongSell-{today}.csv"

nasdaq_df_strongSell.to_csv(filename2,index=False)


# In[ ]:


## Print all the dataFrame
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 4, 'expand_frame_repr', False
                       ):
    print(nasdaq_df)


# In[ ]:


filename3 = f"../RaspberryFiles/Files/nasdaq_df-{today}.csv"
nasdaq_df.to_csv(filename3, index=False)


# In[ ]:


handlerCrypto = TA_Handler(
    symbol="ETHBTC",
    exchange="BINANCEUS",
    screener="crypto",
    interval="1d",
    timeout=None
)


# In[ ]:


print(handlerCrypto.get_analysis().summary)


# In[ ]:




