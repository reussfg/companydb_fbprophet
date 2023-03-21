# First we will import all libraries needed
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
from fbprophet.plot import plot_plotly
import plotly.offline as py
from bcb import currency
from datetime import datetime
plt.style.use('fivethirtyeight')


""""Here we will use FBProphet to make data serie analysis and prediction for company main products prices"""

# Reading our CSV clean file
df = pd.read_excel(r'/Users/gabrielreus/Desktop/Python/TAZ/2023/db_sales/dbnew.xlsx')

# Product name INPUT
print('In case that we want all DB just press enter and do not enter any value')
produto = input('Product name: ')

# Separate the product we want to analyze
if len(produto) != 0:
    df = df[df["produtos"].str.contains(f'{produto}') == True ] # Choosing our product

else:
    print('No product selected')
    quit()

"""Getting USD/BRL conversion rate"""
# Dataframe of BRL value in USD
today = datetime.now()
today = today.strftime("%Y-%m-%d")
cy = currency.get(['USD'], start='2010-12-01', end= today)
cy['data'] = cy.index.strftime('%Y-%m')
cy['data'] = pd.to_datetime(cy['data'], format='%Y-%m').apply(lambda x: x.strftime('%Y-%m'))
cy = cy.groupby(by=['data']).mean().reset_index()

""""We will group our Dataframe and Dolarize"""
# Setting our DF
df = df[['data','valor']]

# Removing day and leaving only Year-Month
df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d').apply(lambda x: x.strftime('%Y-%m'))

# Filter data removing 2010 and 2023
df = df[(df['data'] > '2010-12')]
df = df.dropna()

# Grouping and reset index
df = df.groupby(by=['data']).mean().reset_index()

# Merge our CY and DF and collect dollarize value
df = pd.merge(df, cy, on='data', how='left')
df['usd_valor'] = df['valor']/df['USD']

# Choose the base coin we will analyze
usd_choice = input('Choose USD or BRL for analysis.')
if usd_choice == 'USD':
    df['valor'] = df['usd_valor']
"""elif usd_choice != 'BRL' or usd_choice != 'USD':
   print('No monetary basis')
   quit()
elif usd_choice == 'BRL':
    df['valor'] = df['valor']"""""

# Removing NaN values
df = df.dropna()
print(df.tail(20))

"""We will create our functions"""
def general(dataframe):
    dataframe = dataframe[['data','valor']]
    total_value = dataframe.groupby(by=['data'])['valor'].mean()
    plt.plot(total_value)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Price over time')
    plt.show()

# Bollinger bands function
def bollinger (dataframe, p, m):
    # Set up dataframe
    dataframe1 = dataframe[['data', 'valor']]
    dataframe1 = dataframe1.groupby(by=['data']).mean()
    print(dataframe1.head())

    # Bollinger
    dataframe1['UpperBand'] = dataframe1['valor'].rolling(p).mean() + dataframe1['valor'].rolling(p).std() * m
    dataframe1['LowerBand'] = dataframe1['valor'].rolling(p).mean() - dataframe1['valor'].rolling(p).std() * m

    # Plot
    dataframe1['valor'].plot()
    dataframe1['UpperBand'].plot()
    dataframe1['LowerBand'].plot()
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Price over time')
    plt.show()

def predict_fb(df):
    # Getting data needed, make it in pattern and plot it
    dataframe1 = df[['data','valor']]
    #dataframe1 = dataframe1[(dataframe1['data'] < '2020-03')]
    dataframe1 = dataframe1.groupby(by=['data']).mean().reset_index()
    dataframe1['data'] = pd.DatetimeIndex(dataframe1['data'])
    dataframe1 = dataframe1.rename(columns={'data': 'ds','valor': 'y'})
    ax = dataframe1.set_index('ds').plot(figsize=(12, 8))
    ax.set_ylabel('Value over Time')
    ax.set_xlabel('Date')
    #plt.show()

    # Prophet modeling
    my_model = Prophet(interval_width=0.95)
    my_model.fit(dataframe1)
    future_dates = my_model.make_future_dataframe(periods=6, freq='MS')
    forecast = my_model.predict(future_dates)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head()
    my_model.plot(forecast, uncertainty=True)
    my_model.plot_components(forecast)
    plt.show()

predict_fb(df)