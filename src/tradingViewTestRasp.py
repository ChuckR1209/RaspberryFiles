#!/usr/bin/env python
# coding: utf-8

# ## Bring trading view signals 
# https://python-tradingview-ta.readthedocs.io/en/latest/overview.html#installation
# 
# Has all trading view signals with recommendation

# In[1]:


from __future__ import print_function


# ### Get all stock symbol tickers
# https://levelup.gitconnected.com/how-to-get-all-stock-symbols-a73925c16a1b

# #### You can search on https://tvdb.brianthe.dev to see which symbol, exchange, and screener to use.

# #### The importlib package provides the implementation of the import statement in Python source code portable to any Python interpreter. This also provides an implementation which is easier to comprehend than one implemented in a programming language other than Python.

# ##  https://github.com/StreamAlpha/tvdatafeed to get historical data from Trading View
# ##  https://github.com/TA-Lib/ta-lib-python
# ### indicator ADOSC similar to Chaikin Oscillator

# In[2]:


import importlib


# In[3]:


import tradingview_ta
from tradingview_ta import TA_Handler, Interval, Exchange


# In[4]:


import os
from dotenv import load_dotenv


# In[5]:


load_dotenv()


# In[6]:


# Import date class from datetime module
from datetime import date


# In[7]:


today = date.today() 
print(today)


# In[ ]:





# In[8]:


import requests


# In[9]:


# to get all stock symbols from Yahoo
# pip install yahoo-fin
import pandas as pd
from yahoo_fin import stock_info as si


# In[10]:


from tvDatafeed import TvDatafeed, Interval as TVInterval
import talib
tradingViewPassword = os.getenv("tradingViewPassword")
tradingUser = os.getenv("tradingUser")
tv = TvDatafeed(tradingUser, tradingViewPassword)


# In[ ]:





# In[11]:


# Test 1 ticker
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


# In[12]:


tesla_dict['RECOMMENDATION']


# In[13]:


print(type(tesla_dict))


# In[ ]:





# In[14]:


#teslaDF = pd.DataFrame.from_dict(tesla_dict, index=[0])
teslaDF = pd.DataFrame(tesla_dict,index=[0] )  
print(type(tesla_dict))


# In[15]:


teslaDF.head()


# In[16]:


# data = {'name': ['nick', 'david', 'joe', 'ross'],
#         'age': ['5', '10', '7', '6']} 
# new = pd.DataFrame.from_dict(data)


# In[17]:


drv = TA_Handler(
    symbol="DRV",
    screener="america",
    exchange="AMEX",
    interval=Interval.INTERVAL_1_DAY
)
print(drv.get_analysis().summary)


# In[18]:


drv.get_indicators()


# In[19]:


print(drv.get_analysis().oscillators)


# In[ ]:





# In[20]:


print(drv.get_analysis().moving_averages)


# #### Checking the version

# In[21]:


print(tradingview_ta.__version__)
# Example output: 3.1.3


# #### You can search on https://tvdb.brianthe.dev to see which symbol, exchange, and screener to use.

# In[22]:


handler = TA_Handler(
    symbol="MATICUSDC",
    exchange="KUCOIN",
    screener="crypto",
    interval="1D",
    timeout=None
)


# In[23]:


analysis = handler.get_analysis()


# analysis.symbol

# In[24]:


analysis.indicators["RSI"]


# In[25]:


analysis.indicators["MACD.macd"]


# In[26]:


analysis.time


# In[27]:


analysis.indicators["close"]


# In[28]:


print(handler.get_analysis().summary)


# In[29]:


analysis.indicators


# In[30]:


bbHigh = analysis.indicators['BB.upper']
bbHigh


# In[31]:


close = analysis.indicators['close']
close


# In[32]:


sma30 = analysis.indicators['SMA30']
sma30


# In[33]:


sma10 = analysis.indicators['SMA10']
sma10


# In[34]:


bbLow = analysis.indicators['BB.lower']
bbLow


# In[35]:


percInc30 = (close/sma30 * 100) - 100
percInc30


# In[36]:


percInc10 = (close/sma10 * 100) - 100
percInc10


# In[37]:


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

# In[ ]:





# In[38]:


#key='ccc'


# #### [GET] https://api.taapi.io/pivotpoints?secret=MY_SECRET&exchange=binance&symbol=BTC/USDT&interval=1h

# In[39]:


#api_url = f"https://api.taapi.io/pivotpoints?secret={key}&exchange=binance&symbol=BTC/USDT&interval=1w"


# In[40]:


#api_url


# In[41]:


# response = requests.get(api_url)
# response


# In[42]:


# response.json()


# ## get all symbols from Yahoo

# #### There are three major stock exchanges in the US. They are the Dow, NASDAQ and S&P 500. There is a fourth category of symbols called “others”. We download each category of lists to separate pandas dataframes.

# In[43]:


df1 = pd.DataFrame( si.tickers_sp500() )
df2 = pd.DataFrame( si.tickers_nasdaq() )
df3 = pd.DataFrame( si.tickers_dow() )
df4 = pd.DataFrame( si.tickers_other() )


# #### Next, we convert each dataframe to a list, then to a set.

# In[44]:


sym1 = set( symbol for symbol in df1[0].values.tolist() )
sym2 = set( symbol for symbol in df2[0].values.tolist() )
sym3 = set( symbol for symbol in df3[0].values.tolist() )
sym4 = set( symbol for symbol in df4[0].values.tolist() )


# In[45]:


#sym1


# #### Stock symbols may be listed on more than one exchange. We join the four sets into one. Because it is a set, there will be no duplicate symbols.

# In[46]:


symbols = set.union( sym1, sym2, sym3, sym4 )


# #### Most symbols are up to four letters in length, ie: MSFT for Microsoft. There are some symbols that have a fifth letter. A fifth letter is mostly added to stocks that are delinquent in certain exchange requirements. We’ll identify four of those suffixes for deletion.

# In[47]:


my_list = ['W', 'R', 'P', 'Q']


# 
# W means there are outstanding warrants. We don’t want those.
# R means there is some kind of “rights” issue. Again, not wanted.
# P means “First Preferred Issue”. Preferred stocks are a separate entity.
# Q means bankruptcy. We don’t want those, either.

# We need to initiate two sets; a save set and a delete set.

# In[48]:


del_set = set()
sav_set = set()
del_set_nasdaq = set()
sav_set_nasdaq = set()
del_set_spx = set()
sav_set_spx = set()


# Next, we find the symbols over four characters in length AND have their last letter in my_list. When found, they are added to del_set. All other symbols are added to sav_set.

# In[49]:


for symbol in symbols:
    if len( symbol ) > 4 and symbol[-1] in my_list:
        del_set.add( symbol )
    else:
        sav_set.add( symbol )


# In[50]:


# ONly SPX
for symbol in sym1:
    if len( symbol ) > 4 and symbol[-1] in my_list:
        del_set_spx.add( symbol )
    else:
        sav_set_spx.add( symbol )


# In[51]:


# ONly Nasdaq
for symbol in sym2:
    if len( symbol ) > 4 and symbol[-1] in my_list:
        del_set_nasdaq.add( symbol )
    else:
        sav_set_nasdaq.add( symbol )


# In[52]:


print( f'ALL Removed {len( del_set )} unqualified stock symbols...' )
print( f'ALL There are {len( sav_set )} qualified stock symbols...' )


# In[53]:


print( f'SPX Removed {len( del_set_spx )} unqualified stock symbols...' )
print( f'SPX There are {len( sav_set_spx )} qualified stock symbols...' )


# In[54]:


print( f'Nasdaq Removed {len( del_set_nasdaq )} unqualified stock symbols...' )
print( f'Nasdaq There are {len( sav_set_nasdaq )} qualified stock symbols...' )


# In[55]:


ticker_data = tv.get_hist(symbol= 'GPN',exchange="NYSE",interval=TVInterval.in_1_hour, n_bars=1000)


# In[56]:


ticker_data.head()


# In[90]:


### Function getAnalysisIndicators
# params: tickerSet   - its all the S&P or Nasdaq Tickers set for 
#                        which we want Trading View Recommendations
#         interval1   - is the first call to TradingView through the Handler
#         interval2   - this is for the history we get
#         bars        - is the # of bars for history
#         adoscCnt    - this is the last "n" volume ASDOSC we will concatenate 
#                         to see volume direction. 
#                       will get this only for Strong Buy / Strong Sell and leave others blanlk.
#
#         will return a pandas Dateframe - returnDF

def getAnalysisIndicators ( tickerSet, interval1, interval2, bars, adoscCnt):

    #column_names = ["Symbol", "RECOMMENDATION", "BUY", "SELL", "NEUTRAL", "screener", "exchange", "interval" ]
    column_names = ["Symbol", "RECOMMENDATION", "BUY", "SELL", "NEUTRAL", "ClosePrice", "percInc30", "percInc10", "bbHigh", "bbLow", "screener", "exchange", "interval", "AdoscLastN" ]

    # initialize an empty dataframe
    returnDf = pd.DataFrame(columns = column_names)

    i = 0
    for ss in tickerSet:
        i = i + 1
        print(i)
        exchange="NYSE"
        #print(ss)
        try:
            print("From Main Get Analysis 1st attempt - symbol = "+ss + " " + exchange)
            returnDf = getAnalysis ( ss, returnDf, exchange, interval1, interval2, bars, adoscCnt)
        except Exception as error_message:
            exchange="NASDAQ"
            print("From Main Get Analysis 2nd attempt - symbol = "+ss + " " + exchange)
            try:
                returnDf = getAnalysis ( ss, returnDf, exchange, interval1, interval2, bars, adoscCnt)        
            except Exception as error_message:
                print('getAnalysis ERROR', error_message)
                error = 1  
#         if i == 25:
#             break
    
    
    
    return returnDf


# In[91]:


### Function getAnalysis
# for each symbol will get analysis and then calls getHistIndicators and will append to our dataframe

# params: symb        - Symbol
#         exch        - Exchange
#         interval2   - this is for the history we get
#         bars        - is the # of bars for history
#         adoscCnt    - this is the last "n" volume ASDOSC we will concatenate 
#                         to see volume direction. 
#
#         will return concatenated last adosCnt for now


def getAnalysis ( symb, returnDf, exch, interval1, interval2, bars, adoscCnt):
    
    print("BEfORE TA HANDLER--- symbol = "+symb + " " + exch + " " + str(interval1))
    output = TA_Handler(
    symbol=symb,
    screener="america",
    exchange=exch,
    interval=interval1)
    try:
        print("inside getAnalysis- ta handler succeeded")
    except Exception as error_message:
        print('TA handler ERROR', error_message)
        error = 1     
        return returnDf
    print("symbol = "+symb + " " + exch)
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

    # get last ex. 8 (adoscCnt) ADOSC volume if strong buy or sell.
    concatAdosc = " "
    if ( dict1['RECOMMENDATION'] == "STRONG_BUY" or dict1['RECOMMENDATION'] == "STRONG_SELL"):
        try: 
            print(" from getAnalysis about to call getHistIndi first time")
            concatAdosc = getHistIndicators ( symb, "NYSE", interval2, bars, adoscCnt)
        except Exception as error_message:
            try:
                print(" from getAnalysis about to call getHistIndi 2nd time")
                concatAdosc = getHistIndicators ( symb, "NASDAQ", interval2, bars, adoscCnt)   
            except Exception as error_message:
                print('getHistIndicators ERROR', error_message)
                error = 1 
    returnDf = returnDf.append({'Symbol': symb, 'RECOMMENDATION' :dict1['RECOMMENDATION'], 'BUY': dict1['BUY'], 
                           'SELL': dict1['SELL'], 'NEUTRAL': dict1['NEUTRAL'], 
                            'ClosePrice': close, 'percInc30': percInc30, 'percInc10': percInc10,'bbHigh': bbHigh, 'bbLow': bbLow,
                            'screener' : "america",
                           'exchange' : exch, 'interval': interval1, 'AdoscLastN': concatAdosc }, ignore_index=True)
    


    return returnDf
    
    
    


# In[92]:


### Function getHistIndicators
# params: symb        - Symbol
#         exch        - Exchange
#         interval2   - this is for the history we get
#         bars        - is the # of bars for history
#         adoscCnt    - this is the last "n" volume ASDOSC we will concatenate 
#                         to see volume direction. 
#
#         will return concatenated last adosCnt for now


def getHistIndicators ( symb, exch, interval2, bars, adoscCnt):
    # get history first
    ticker_data = tv.get_hist(symbol= symb,exchange=exch,interval=interval2, n_bars=bars)
    # get ADOSC indicator for the history
    adoscTicker = talib.ADOSC(ticker_data['high'],ticker_data['low'],ticker_data['close'],ticker_data['volume'],3,10)
    #print(row['Symbol'], adoscTicker.tail(5))
    # we keep last 8 (adoscCnt) volume ADOSC historty concatenated 
    lastAdosc = adoscTicker.tail(adoscCnt)
    concatAdosc = " "
    # concatenate them into a string
    for atCntr in lastAdosc:
        concatAdosc = concatAdosc + " " + str(round(atCntr,2))   # doing 2 decimals for ADOSC
    #print(" Symbol and ADOSC = ", symb )
    return concatAdosc


# ### Get S&P tickers Trading View Recommendation and ADOSC volume from History

# In[94]:


spx_df = getAnalysisIndicators ( sav_set_spx, Interval.INTERVAL_1_DAY, TVInterval.in_1_hour, 1000, 8 )


# In[95]:


len(spx_df)


# In[96]:


# # for ss in sav_set_spx:
# #     print(ss)

# # First try NYSE and then if not NASDAQ. Else if both in error print error and move on to next symbol
# spx_dict_final = {}

# #column_names = ["Symbol", "RECOMMENDATION", "BUY", "SELL", "NEUTRAL", "screener", "exchange", "interval" ]
# column_names = ["Symbol", "RECOMMENDATION", "BUY", "SELL", "NEUTRAL", "ClosePrice", "percInc30", "percInc10", "bbHigh", "bbLow", "screener", "exchange", "interval", "AdoscLast8" ]

# spx_df = pd.DataFrame(columns = column_names)

# i = 0
# for ss in sav_set_spx:
#     i = i + 1
#     print(i)
#     exchange="NYSE"
#     #print(ss)
#     output = TA_Handler(
#     symbol=ss,
#     screener="america",
#     #exchange="NASDAQ",
#     exchange="NYSE",
#     interval=Interval.INTERVAL_1_DAY)
#     print("symbol = "+ss + " " + exchange)
#     try:
#         analysis = output.get_analysis()
#         bbLow = analysis.indicators['BB.lower']
#         bbHigh = analysis.indicators['BB.upper']
#         close = analysis.indicators['close']
#         sma30 = analysis.indicators['SMA30']
#         sma10 = analysis.indicators['SMA10']
#         percInc30 = (close/sma30 * 100) - 100
#         percInc10 = (close/sma10 * 100) - 100        
#         print(output.get_analysis().summary)
#         dict1 = output.get_analysis().summary

#         # get last 8 ADOSC volume if strong buy or sell.
#         if ( dict1['RECOMMENDATION'] == "STRONG_BUY" or dict1['RECOMMENDATION'] == "STRONG_SELL"):
#             concat8adosc = " "
#             try:
#                 ticker_data = tv.get_hist(symbol= ss,exchange="NYSE",interval=TVInterval.in_1_hour, n_bars=1000)
#                 #print(ticker_data.head())
#                 adoscTicker = talib.ADOSC(ticker_data['high'],ticker_data['low'],ticker_data['close'],ticker_data['volume'],3,10)

#                 last8adosc = adoscTicker.tail(8)
#                 concat8adosc = " "
#                 for atCntr in last8adosc:
#                     concat8adosc = concat8adosc + " " + str(round(atCntr,2)) 
#             except Exception as error_message:
#                 ticker_data = tv.get_hist(symbol= ss,exchange="NASDAQ",interval=TVInterval.in_1_hour, n_bars=1000)
#                 #print(ticker_data.head())
#                 adoscTicker = talib.ADOSC(ticker_data['high'],ticker_data['low'],ticker_data['close'],ticker_data['volume'],3,10)

#                 last8adosc = adoscTicker.tail(8)
#                 concat8adosc = " "
#                 for atCntr in last8adosc:
#                     concat8adosc = concat8adosc + " " + str(round(atCntr,2))
                    
#         spx_df = spx_df.append({'Symbol': ss, 'RECOMMENDATION' :dict1['RECOMMENDATION'], 'BUY': dict1['BUY'], 
#                                'SELL': dict1['SELL'], 'NEUTRAL': dict1['NEUTRAL'], 
#                                 'ClosePrice': close, 'percInc30': percInc30, 'percInc10': percInc10,'bbHigh': bbHigh, 'bbLow': bbLow,
#                                 'screener' : "america",
#                                'exchange' : "NYSE", 'interval': "Interval.INTERVAL_1_DAY", 'AdoscLast8': concat8adosc }, ignore_index=True)

#     except Exception as error_message:
#         exchange="NASDAQ"
#         print("2nd attempt - symbol = "+ss + " " + exchange)
#         output = TA_Handler(
#         symbol=ss,
#         screener="america",
#         exchange="NASDAQ",
#         #exchange="NYSE",
#         interval=Interval.INTERVAL_1_DAY)
#         try:
#             analysis = output.get_analysis()
#             bbLow = analysis.indicators['BB.lower']
#             bbHigh = analysis.indicators['BB.upper']
#             close = analysis.indicators['close']
#             sma30 = analysis.indicators['SMA30']
#             sma10 = analysis.indicators['SMA10']
#             percInc30 = (close/sma30 * 100) - 100
#             percInc10 = (close/sma10 * 100) - 100            
#             print(output.get_analysis().summary)
#             dict1 = output.get_analysis().summary
            
#             # get last 8 ADOSC volume if strong buy or sell.
#             concat8adosc = " "
#             try: 
#                 if ( dict1['RECOMMENDATION'] == "STRONG_BUY" or dict1['RECOMMENDATION'] == "STRONG_SELL"):
#                     ticker_data = tv.get_hist(symbol= ss,exchange="NYSE",interval=TVInterval.in_1_hour, n_bars=1000)
#                     adoscTicker = talib.ADOSC(ticker_data['high'],ticker_data['low'],ticker_data['close'],ticker_data['volume'],3,10)
#                     #print(row['Symbol'], adoscTicker.tail(5))
#                     last8adosc = adoscTicker.tail(8)
#                     concat8adosc = " "
#                     for atCntr in last8adosc:
#                         concat8adosc = concat8adosc + " " + str(round(atCntr,2))
#                     print(" Symbol and ADOSC = ", symbol, )
#             except Exception as error_message:
#                 if ( dict1['RECOMMENDATION'] == "STRONG_BUY" or dict1['RECOMMENDATION'] == "STRONG_SELL"):
#                     ticker_data = tv.get_hist(symbol= ss,exchange="NASDAQ",interval=TVInterval.in_1_hour, n_bars=1000)
#                     adoscTicker = talib.ADOSC(ticker_data['high'],ticker_data['low'],ticker_data['close'],ticker_data['volume'],3,10)
#                     #print(row['Symbol'], adoscTicker.tail(5))
#                     last8adosc = adoscTicker.tail(8)
#                     concat8adosc = " "
#                     for atCntr in last8adosc:
#                         concat8adosc = concat8adosc + " " + str(round(atCntr,2))
#                     print(" Symbol and ADOSC = ", symbol, )            

            
#             spx_df = spx_df.append({'Symbol': ss, 'RECOMMENDATION' :dict1['RECOMMENDATION'], 'BUY': dict1['BUY'], 
#                                'SELL': dict1['SELL'], 'NEUTRAL': dict1['NEUTRAL'], 
#                                 'ClosePrice': close, 'percInc30': percInc30, 'percInc10': percInc10,'bbHigh': bbHigh, 'bbLow': bbLow,    
#                                 'screener' : "america",
#                                'exchange' : "NASDAQ", 'interval': "Interval.INTERVAL_1_DAY", 'AdoscLast8': concat8adosc }, ignore_index=True)
#             # spx_dict['symbol'] = ss
#             # spx_dict['screener'] = "america"
#             # spx_dict['exchange'] = "NYSE"
#             # spx_dict['interval'] = "Interval.INTERVAL_1_DAY"
#         except Exception as error_message:
#             print('ERROR', error_message)
#             error = 1  
#     if i == 25:
#         break


# In[97]:


# df = pd.DataFrame(columns=['A'])
# >>> for i in range(5):
# ...     df = df.append({'A': i}, ignore_index=True)


# In[98]:


spx_df.tail()


# In[99]:



len(spx_df)

# for ss in sav_set_nasdaq:
#     print(ss)


# In[100]:


spx_df_strongBuy = spx_df[spx_df['RECOMMENDATION'] == "STRONG_BUY"]


# In[101]:


len(spx_df_strongBuy)


# In[102]:


spx_df_strongBuy = spx_df_strongBuy.sort_values(by='BUY', ascending=False)


# In[103]:


## Print all the dataFrame
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 4, 'expand_frame_repr', False
                       ):
    print(spx_df_strongBuy)


# In[104]:


spxStrongBuyFile = f"spxStrongBuyFile_{today}.csv"
spxStrongBuyFile


# In[105]:


################### Raspberry
spxStrongBuyFile = f"../RaspberryFiles/Files/spxStrongBuyFile_{today}.csv"
spxStrongBuyFile
################### Raspberry


# In[106]:


spx_df_strongBuy.to_csv(spxStrongBuyFile, index=False)


# In[107]:


spx_df_strongSell = spx_df[spx_df['RECOMMENDATION'] == "STRONG_SELL"]


# In[108]:


len(spx_df_strongSell)


# In[109]:


spx_df_strongSell = spx_df_strongSell.sort_values(by='SELL', ascending=False)


# In[110]:


spxStrongSellFile = f"spxStrongSellFile_{today}.csv"
spxStrongSellFile


# In[111]:


################### Raspberry
spxStrongSellFile = f"../RaspberryFiles/Files/spxStrongSellFile_{today}.csv"
spxStrongSellFile
################### Raspberry


# In[112]:


spx_df_strongSell.to_csv(spxStrongSellFile, index=False)


# In[113]:


## Print all the dataFrame
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 4, 'expand_frame_repr', False
                       ):
    print(spx_df_strongSell)


# In[114]:


## Print all the dataFrame
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 4, 'expand_frame_repr', False
                       ):
    print(spx_df.head())


# In[115]:


spxFile = f"spx_df_{today}.csv"
spxFile


# In[116]:


#################### Raspberry
spxFile = f"../RaspberryFiles/Files/spx_df_{today}.csv"
spxFile
#################### Raspberry


# In[117]:


spx_df.to_csv(spxFile, index=False)


# ### NASDAQ 

# In[137]:


#nasdaq_df = getAnalysisIndicators ( sav_set_nasdaq, Interval.INTERVAL_1_DAY, TVInterval.in_1_hour, 1000, 8 )
#
nasdaq_df = getAnalysisIndicators ( sav_set_nasdaq, Interval.INTERVAL_1_HOUR, TVInterval.in_1_hour, 1000, 8 )


# In[138]:


# # for ss in sav_set_spx:
# #     print(ss)



# #column_names = ["Symbol", "RECOMMENDATION", "BUY", "SELL", "NEUTRAL", "screener", "exchange", "interval" ]
# column_names = ["Symbol", "RECOMMENDATION", "BUY", "SELL", "NEUTRAL", "ClosePrice", "percInc30", "percInc10", "bbHigh", "bbLow", "screener", "exchange", "interval","AdoscLast8" ]

# nasdaq_df = pd.DataFrame(columns = column_names)

# i = 0
# for ss in sav_set_nasdaq:
#     i = i + 1
#     print(i)
#     #print(ss)
#     output = TA_Handler(
#     symbol=ss,
#     screener="america",
#     #exchange="NASDAQ",
#     exchange="NYSE",
#     interval=Interval.INTERVAL_1_DAY)
#     print("symbol = "+ss)
#     try:
#         analysis = output.get_analysis()
#         bbLow = analysis.indicators['BB.lower']
#         bbHigh = analysis.indicators['BB.upper']
#         close = analysis.indicators['close']
#         sma30 = analysis.indicators['SMA30']
#         sma10 = analysis.indicators['SMA10']
#         percInc30 = (close/sma30 * 100) - 100
#         percInc10 = (close/sma10 * 100) - 100         
#         print(output.get_analysis().summary)
#         dict1 = output.get_analysis().summary
#         nasdaq_df = nasdaq_df.append({'Symbol': ss, 'RECOMMENDATION' :dict1['RECOMMENDATION'], 'BUY': dict1['BUY'], 
#                                'SELL': dict1['SELL'], 'NEUTRAL': dict1['NEUTRAL'], 
#                                       'ClosePrice': close, 'percInc30': percInc30, 'percInc10': percInc10,'bbHigh': bbHigh, 'bbLow': bbLow,
#                                       'screener' : "america",
#                                'exchange' : "NYSE", 'interval': "Interval.INTERVAL_1_DAY"}, ignore_index=True)

#     except Exception as error_message:
#         output = TA_Handler(
#         symbol=ss,
#         screener="america",
#         exchange="NASDAQ",
#         #exchange="NYSE",
#         interval=Interval.INTERVAL_1_DAY)
#         try:
#             analysis = output.get_analysis()
#             bbLow = analysis.indicators['BB.lower']
#             bbHigh = analysis.indicators['BB.upper']
#             close = analysis.indicators['close']
#             sma30 = analysis.indicators['SMA30']
#             sma10 = analysis.indicators['SMA10']
#             percInc30 = (close/sma30 * 100) - 100
#             percInc10 = (close/sma10 * 100) - 100             
#             print(output.get_analysis().summary)
#             dict1 = output.get_analysis().summary
#             nasdaq_df = nasdaq_df.append({'Symbol': ss, 'RECOMMENDATION' :dict1['RECOMMENDATION'], 'BUY': dict1['BUY'], 
#                                'SELL': dict1['SELL'], 'NEUTRAL': dict1['NEUTRAL'], 
#                                'ClosePrice': close, 'percInc30': percInc30, 'percInc10': percInc10,'bbHigh': bbHigh, 'bbLow': bbLow,           
#                                           'screener' : "america",
#                                'exchange' : "NASDAQ", 'interval': "Interval.INTERVAL_1_DAY"}, ignore_index=True)
#             # spx_dict['symbol'] = ss
#             # spx_dict['screener'] = "america"
#             # spx_dict['exchange'] = "NYSE"
#             # spx_dict['interval'] = "Interval.INTERVAL_1_DAY"
#         except Exception as error_message:
#             print('ERROR', error_message)
#             error = 1  
#     if i == 15:
#         break


# In[139]:


len(nasdaq_df)


# In[140]:


nasdaq_df_strongBuy = nasdaq_df[nasdaq_df['RECOMMENDATION'] == "STRONG_BUY"]


# In[141]:


nasdaq_df_strongBuy = nasdaq_df_strongBuy.sort_values(by=(['percInc10', 'percInc30', 'BUY']), ascending=[False, False, False])


# In[142]:


len(nasdaq_df_strongBuy)


# In[143]:


## Print all the dataFrame
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 4, 'expand_frame_repr', False
                       ):
    print(nasdaq_df_strongBuy.head())


# In[144]:


# filename1 = f"NasdaqStrongBuy{today}.csv"
# filename1

nasdaqStrongBuyTodayFile = f"../RaspberryFiles/Files/NasdaqStrongBuy-{today}.csv"
nasdaqStrongBuyTodayFile


# In[145]:


nasdaq_df_strongBuy.to_csv(nasdaqStrongBuyTodayFile,index=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[146]:


nasdaq_df_strongSell = nasdaq_df[nasdaq_df['RECOMMENDATION'] == "STRONG_SELL"]


# In[147]:


nasdaq_df_strongSell = nasdaq_df_strongSell.sort_values(by=(['percInc10', 'percInc30', 'SELL']), ascending=[True, True, False])


# In[148]:


len(nasdaq_df_strongSell)


# In[149]:


## Print all the dataFrame
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 4, 'expand_frame_repr', False
                       ):
    print(nasdaq_df_strongSell)


# In[150]:


filename2 = f"../RaspberryFiles/Files/NasdaqStrongSell-{today}.csv"

nasdaq_df_strongSell.to_csv(filename2,index=False)


# In[151]:


## Print all the dataFrame
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 4, 'expand_frame_repr', False
                       ):
    print(nasdaq_df)


# In[152]:


filename3 = f"../RaspberryFiles/Files/nasdaq_df-{today}.csv"
nasdaq_df.to_csv(filename3, index=False)


# In[153]:


handlerCrypto = TA_Handler(
    symbol="ETHBTC",
    exchange="BINANCEUS",
    screener="crypto",
    interval="1d",
    timeout=None
)


# In[136]:


print(handlerCrypto.get_analysis().summary)


# In[ ]:





# ##  https://github.com/StreamAlpha/tvdatafeed to get historical data from Trading View

# ##  https://github.com/TA-Lib/ta-lib-python
# ### indicator ADOSC similar to Chaikin Oscillator

# In[ ]:





# In[ ]:


# from tvDatafeed import TvDatafeed, Interval


# In[ ]:


# import talib


# In[ ]:


# tradingViewPassword = os.getenv("tradingViewPassword")
# tradingUser = os.getenv("tradingUser")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# tv = TvDatafeed(tradingUser, tradingViewPassword)


# In[ ]:





# In[ ]:


# # index
# tsla_index_data = tv.get_hist(symbol='TSLA',exchange='NASDAQ',interval=Interval.in_1_hour,n_bars=1000)


# In[ ]:


# adoscTicker = talib.ADOSC(tsla_index_data['high'],tsla_index_data['low'],tsla_index_data['close'],tsla_index_data['volume'],3,10)
# adoscTicker.tail(8)


# In[ ]:


# tsla_index_data.head()


# In[ ]:


#nifty_index_data


# In[ ]:


# spx_df_strongBuy.head()


# In[ ]:


# RECOMMENDATION	BUY	SELL	NEUTRAL	symbol	screener	exchange	interval
# 0	SELL	3	15	8	TSLA	america	NASDAQ	Interval.INTERVAL_1_DAY


# In[ ]:


# # spx_df_strongBuy
# # for row in spx_df_strongBuy.rows:
# #df = spx_df_strongBuy.reset_index()  
# for index, row in spx_df_strongBuy.iterrows():
#     print(row['Symbol'], row['exchange'])
#     ticker_data = tv.get_hist(symbol= row['Symbol'],exchange=row['exchange'],interval=Interval.in_1_hour, n_bars=1000)
#     #print(ticker_data.head())
#     adoscTicker = talib.ADOSC(ticker_data['high'],ticker_data['low'],ticker_data['close'],ticker_data['volume'],3,10)
#     print("length of asoscTicker = ", len(adoscTicker))
#     #print(row['Symbol'], adoscTicker.tail(5))
#     last8 = adoscTicker.tail(8)
#     concat8 = " "
#     for i in last8:
#         concat8 = concat8 + " " + str(round(i,2))
#         concat8 = concat8 + " " + str(round(i,2))
#         #str(round(answer, 2))
#     print("ADOSC last8 = ", concat8)
    


# In[ ]:


# last8 = adoscTicker.tail(8)
# last8
# concat8 = " "
# for i in last8:
#     concat8 = concat8 + " " + str(i)
# concat8


# In[ ]:



# # btc_index_data = tv.get_hist(symbol='BTCUSDT',exchange='KUCOIN',interval=Interval.in_daily,n_bars=1000)
# btc_index_data = tv.get_hist(symbol='BTCUSDT',exchange='KUCOIN',interval=Interval.in_1_hour,n_bars=1000)
# btc_index_data


# In[ ]:


# adoscBTC = talib.ADOSC(btc_index_data['high'],btc_index_data['low'],btc_index_data['close'],btc_index_data['volume'],3,10)
# adoscBTC


# In[ ]:


# btc_index_data['close']


# 

# 

# In[ ]:





# In[ ]:


# smaBTC = talib.SMA(btc_index_data['close'])
# smaBTC


# In[ ]:


# adBTC = talib.AD(btc_index_data['high'],btc_index_data['low'],btc_index_data['close'],btc_index_data['volume'])
# adBTC


# In[ ]:





# In[ ]:


# # ge_index_data = tv.get_hist(symbol='GEHC',exchange='NYSE',interval=Interval.in_daily,n_bars=1000)
# ge_index_data = tv.get_hist(symbol='AAPL',exchange='NASDAQ',interval=Interval.in_1_hour,n_bars=1000)
# ge_index_data


# In[ ]:


# adoscGE = talib.ADOSC(ge_index_data['high'],ge_index_data['low'],ge_index_data['close'],ge_index_data['volume'],3,10)
# adoscGE


# In[ ]:




