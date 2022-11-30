# -*- coding: utf-8 -*-
###############################################################################
# FINANCIAL DASHBOARD #2 - v2.1
###############################################################################

#==============================================================================
# Initiating
#==============================================================================

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yfinance as yf
import pandas_datareader.data as web
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# start and end date of the plot data 
today = datetime.today().date()

st.set_option('deprecation.showPyplotGlobalUse', False)

#==============================================================================
# Tab 1
#==============================================================================

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

def tab1():

    
    # Add dashboard title and description
    st.title("Yahoo Financial Dashboard")
    st.write("Data source: Yahoo Finance. URL: https://finance.yahoo.com/")
    st.header('Summary')
    
    
    # Add table to show stock data
    @st.cache
    def GetCompanyInfo(ticker):
        return yf.Ticker(ticker).info
    
    if ticker != '':
        # Get the company information in list format
        info = GetCompanyInfo(ticker)
        
        col1, col2 = st.columns([2,5])
        
        with col1:
            
            # Show some statistics
            keys = {'Previous Close' : 'previousClose', 'Open' : 'open', 'Market Cap' : 'marketCap', 'Volume' : 'volume'}
            keys2 = ['dayLow', 'dayHigh']
            
            company_stats = {}  # Dictionary
            for key in keys:
                company_stats.update({key:info[keys[key]]})
            
            company_stats.update({"Day's Range":str(info[keys2[0]]) + " - " + str(info[keys2[1]])})
            
            for i in company_stats:
                st.metric(label = i, value = company_stats[i])
            
            
        with col2:
            
            st.subheader('**Closing Price** ' + str(ticker))
            
            # Add table to show stock data
            @st.cache
            def GetStockData(tickers, start_date, end_date):
                stock_price = pd.DataFrame()
                for tick in tickers:
                    stock_df = yf.Ticker(tick).history(start=start_date, end=end_date)
                    stock_df['Ticker'] = tick  # Add the column ticker name
                    stock_price = pd.concat([stock_price, stock_df], axis=0)  # Comebine results
                return stock_price.loc[:, ['Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']]
            
            
            def SummaryChart():
                    
                stock_price = yf.Ticker(ticker).history(start=start_date,end=end_date)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=stock_price.index, y=stock_price['Close'], fill='tozeroy')) # fill down to xaxis
 
                # Updating layout
                fig.update_layout(
                    width=500,
                    height=500,
                    xaxis_title='Date',
                    yaxis_title='Price',
                    template='plotly_white',
                    xaxis_rangeslider_visible=True,
                    hovermode='x'
                    )
                
                fig.update_xaxes(
                    rangeslider_visible=True,
                    rangeselector=dict(
                        buttons=list([
                            dict(count=1, label="1d", step="day", stepmode="backward"),
                            dict(count=5, label="5d", step="day", stepmode="backward"),
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=3, label="3m", step="month", stepmode="backward"),
                            dict(count=6, label="6m", step="month", stepmode="backward"),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(count=2, label="2y", step="year", stepmode="backward"),
                            dict(count=5, label="5y", step="year", stepmode="backward"),
                            dict(count=10, label="10y", step="year", stepmode="backward"),
                            dict(step="all")
                            ])
                        )
                    )
                
                fig.update_layout(xaxis_rangeslider_visible=False)
                
                
                st.plotly_chart(fig, use_container_width=True)
                
            SummaryChart() #call the function
        
    # Show the company description
    st.write('**Business Summary**')
    st.write(info['longBusinessSummary'])
    
    
    col1, col2 = st.columns([2,5])
    
    with col1:
    
        if ticker != '': # Get the company major shareholders
            
            st.subheader('Major Shareholders')
        
            st.dataframe(yf.Ticker(ticker).major_holders)
            
    
    with col2:
        
        if ticker != '': # Get the company major shareholders
            
            st.subheader('Institutional Shareholders')
        
            st.dataframe(yf.Ticker(ticker).institutional_holders)
            

#==============================================================================
# Tab 2
#==============================================================================

def tab2():
    
    
    # Add dashboard title and description
    st.title("Chart")
    st.write("Data source: Yahoo Finance. URL: https://finance.yahoo.com/")
    st.header('Tab 2 - Chart')
    
    c1, c2, c3, = st.columns((1,1,1))
         
    with c1: durationtab2 = st.selectbox("Select duration if you want to see the prices from today until", ['max','ytd', '10y', '5y', '2y', '1y', '6mo', '3mo', '1mo', '5d', '1d', ''])       
            

    with c2: inter = st.selectbox("Select interval", ['1d', '1wk', '1mo'])
        
    with c3: plot = st.radio("Select Plot", options=["Line", "Candle"])

    st.write('Or choose a date range on the left (and change the duration directly on the graph')
    
    # Add table to show stock data
    @st.cache
    def GetStockData(tickers, interval, start_date, end_date, period=None):
        stock_price = pd.DataFrame()
        for tick in tickers:
            stock_df = yf.Ticker(tick).history(period=period,interval=interval, start=start_date, end=end_date)
            stock_df['Ticker'] = tick  # Add the column ticker name
            stock_price = pd.concat([stock_price, stock_df], axis=0)  # Comebine results
        return stock_price.loc[:, ['Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']]
    
    # Add a check box
    show_data = st.checkbox("Show data table")
    
    def SMA(data, period=50, column='Close'):
        return data[column].rolling(window=period).mean()
    
    if ticker != '':
        stock_price = GetStockData([ticker],inter, start_date, end_date)
        if show_data:
            st.write('Stock price data')
            st.dataframe(stock_price) 
            
    # Add a line plot
    if ticker != '':
       
        if plot == 'Line':  
            def LineTab2():
                
                if durationtab2 != '':
                #x = end_date-timedelta(periods.loc[periods['DurationText']==durationtab2,'DurationN'].iloc[0].item())
            
                    stock_price = yf.Ticker(ticker).history(period=durationtab2,interval=inter)
                    stock_price['SMA50']=SMA(stock_price)
                    
                    # Creating figure with second y-axis
                    fig = make_subplots(specs=[[{"secondary_y": True}]])

                    # Adding line plot with close prices and bar plot with trading volume
                    fig.add_trace(go.Scatter(x=stock_price.index, y=stock_price['Close'], name='Closing Price'), secondary_y=False)
                    fig.add_trace(go.Bar(x=stock_price.index, y=stock_price['Volume'], name='Volume', opacity=0.5), secondary_y=True)
                    fig.add_trace(go.Scatter(x=stock_price.index, y=stock_price['SMA50'], name='SMA'), secondary_y=False)
                    
                    # Updating layout
                    fig.update_layout(
                        width=500,
                        height=800,
                        xaxis_title='Date',
                        yaxis_title='Price',
                        template='plotly_white',
                        xaxis_rangeslider_visible=True,
                        hovermode='x'
                        )

                    # Disabling grid of second y-axis
                    fig.layout.yaxis2.showgrid=False
                    
                    fig.update_xaxes(
                        rangeslider_visible=True,
                        rangeselector=dict(
                            buttons=list([
                                dict(count=1, label="1d", step="day", stepmode="backward"),
                                dict(count=5, label="5d", step="day", stepmode="backward"),
                                dict(count=1, label="1m", step="month", stepmode="backward"),
                                dict(count=3, label="3m", step="month", stepmode="backward"),
                                dict(count=6, label="6m", step="month", stepmode="backward"),
                                dict(count=1, label="YTD", step="year", stepmode="todate"),
                                dict(count=1, label="1y", step="year", stepmode="backward"),
                                dict(count=2, label="2y", step="year", stepmode="backward"),
                                dict(count=5, label="5y", step="year", stepmode="backward"),
                                dict(count=10, label="10y", step="year", stepmode="backward"),
                                dict(step="all")
                                ])
                            )
                        )
                    
                    fig.update_layout(xaxis_rangeslider_visible=False)
                    
                    
                    st.plotly_chart(fig, use_container_width=True)
                    

                else:
                    
                    stock_price = yf.Ticker(ticker).history(interval=inter, start=start_date, end=end_date)
                    stock_price['SMA50']=SMA(stock_price)
                    
                    # Creating figure with second y-axis
                    fig = make_subplots(specs=[[{"secondary_y": True}]])

                    # Adding line plot with close prices and bar plot with trading volume
                    fig.add_trace(go.Scatter(x=stock_price.index, y=stock_price['Close'], name='Closing Price'), secondary_y=False)
                    fig.add_trace(go.Bar(x=stock_price.index, y=stock_price['Volume'], name='Volume', opacity=0.5), secondary_y=True)
                    fig.add_trace(go.Scatter(x=stock_price.index, y=stock_price['SMA50'], name='SMA'), secondary_y=False)
                   
                    # Updating layout
                    fig.update_layout(
                        width=500,
                        height=800,
                        xaxis_title='Date',
                        yaxis_title='Price',
                        template='plotly_white',
                        xaxis_rangeslider_visible=True,
                        hovermode='x'
                        )

                    # Disabling grid of second y-axis
                    fig.layout.yaxis2.showgrid=False
                    
                    fig.update_xaxes(
                        rangeslider_visible=True,
                        rangeselector=dict(
                            buttons=list([
                                dict(count=1, label="1d", step="day", stepmode="backward"),
                                dict(count=5, label="5d", step="day", stepmode="backward"),
                                dict(count=1, label="1m", step="month", stepmode="backward"),
                                dict(count=3, label="3m", step="month", stepmode="backward"),
                                dict(count=6, label="6m", step="month", stepmode="backward"),
                                dict(count=1, label="YTD", step="year", stepmode="todate"),
                                dict(count=1, label="1y", step="year", stepmode="backward"),
                                dict(count=2, label="2y", step="year", stepmode="backward"),
                                dict(count=5, label="5y", step="year", stepmode="backward"),
                                dict(count=10, label="10y", step="year", stepmode="backward"),
                                dict(step="all")
                                ])
                            )
                        )
                    
                    fig.update_layout(xaxis_rangeslider_visible=False)
                    
                    
                    st.plotly_chart(fig, use_container_width=True)
        
            LineTab2()
            
            
        elif plot == 'Candle':
            def CandleStick():
           
                if durationtab2 != '':
                #x = end_date-timedelta(periods.loc[periods['DurationText']==durationtab2,'DurationN'].iloc[0].item())
            
                    stock_price = yf.Ticker(ticker).history(period=durationtab2,interval=inter)
                    stock_price['SMA50']=SMA(stock_price)
                    
                    # Creating figure with second y-axis
                    fig = make_subplots(specs=[[{"secondary_y": True}]])

                    # Adding line plot with close prices and bar plot with trading volume
                    fig.add_trace(go.Candlestick(
                                x=stock_price.index,
                                open=stock_price['Open'],
                                high=stock_price['High'],
                                low=stock_price['Low'],
                                close=stock_price['Close'],
                                name='Closing Price'), secondary_y=False)
                    
                    fig.add_trace(go.Bar(x=stock_price.index, y=stock_price['Volume'], name='Volume', opacity=0.5), secondary_y=True)
                    fig.add_trace(go.Scatter(x=stock_price.index, y=stock_price['SMA50'], name='SMA'), secondary_y=False)
                    
                    # Updating layout
                    fig.update_layout(
                        width=500,
                        height=800,
                        xaxis_title='Date',
                        yaxis_title='Price',
                        template='plotly_white',
                        xaxis_rangeslider_visible=True,
                        hovermode='x'
                        )

                    # Disabling grid of second y-axis
                    fig.layout.yaxis2.showgrid=False
                    
                    fig.update_xaxes(
                        rangeslider_visible=True,
                        rangeselector=dict(
                            buttons=list([
                                dict(count=1, label="1d", step="day", stepmode="backward"),
                                dict(count=5, label="5d", step="day", stepmode="backward"),
                                dict(count=1, label="1m", step="month", stepmode="backward"),
                                dict(count=3, label="3m", step="month", stepmode="backward"),
                                dict(count=6, label="6m", step="month", stepmode="backward"),
                                dict(count=1, label="YTD", step="year", stepmode="todate"),
                                dict(count=1, label="1y", step="year", stepmode="backward"),
                                dict(count=2, label="2y", step="year", stepmode="backward"),
                                dict(count=5, label="5y", step="year", stepmode="backward"),
                                dict(count=10, label="10y", step="year", stepmode="backward"),
                                dict(step="all")
                                ])
                            )
                        )
                    
                    fig.update_layout(xaxis_rangeslider_visible=False)
                    
                    
                    st.plotly_chart(fig, use_container_width=True)
                    

                else:
                    
                    stock_price = yf.Ticker(ticker).history(interval=inter, start=start_date, end=end_date)
                    stock_price['SMA50']=SMA(stock_price)
                    
                    #Creating figure with second y-axis
                    fig = make_subplots(specs=[[{"secondary_y": True}]])

                    #Adding line plot with close prices and bar plot with trading volume
                    fig.add_trace(go.Candlestick(
                               x=stock_price.index,
                               open=stock_price['Open'],
                               high=stock_price['High'],
                               low=stock_price['Low'],
                               close=stock_price['Close'],
                               name='Closing Price'), secondary_y=False)
                   
                    fig.add_trace(go.Bar(x=stock_price.index, y=stock_price['Volume'], name='Volume', opacity=0.5), secondary_y=True)
                    fig.add_trace(go.Scatter(x=stock_price.index, y=stock_price['SMA50'], name='SMA'), secondary_y=False)
                    
                    # Updating layout
                    fig.update_layout(
                        width=500,
                        height=800,
                        xaxis_title='Date',
                        yaxis_title='Price',
                        template='plotly_white',
                        xaxis_rangeslider_visible=True,
                        hovermode='x'
                        )

                    # Disabling grid of second y-axis
                    fig.layout.yaxis2.showgrid=False
                    
                    fig.update_xaxes(
                        rangeslider_visible=True,
                        rangeselector=dict(
                            buttons=list([
                                dict(count=1, label="1d", step="day", stepmode="backward"),
                                dict(count=5, label="5d", step="day", stepmode="backward"),
                                dict(count=1, label="1m", step="month", stepmode="backward"),
                                dict(count=3, label="3m", step="month", stepmode="backward"),
                                dict(count=6, label="6m", step="month", stepmode="backward"),
                                dict(count=1, label="YTD", step="year", stepmode="todate"),
                                dict(count=1, label="1y", step="year", stepmode="backward"),
                                dict(count=2, label="2y", step="year", stepmode="backward"),
                                dict(count=5, label="5y", step="year", stepmode="backward"),
                                dict(count=10, label="10y", step="year", stepmode="backward"),
                                dict(step="all")
                                ])
                            )
                        )
                    
                    fig.update_layout(xaxis_rangeslider_visible=False)
                    
                    
                    st.plotly_chart(fig, use_container_width=True)
    
        
        
            CandleStick()

#==============================================================================
# Tab 3
#==============================================================================

def tab3():
        
    # Add section title and description
    st.title("Financials Historic Data")
    st.header('Tab 3 - Financials Historic Data')
    
    c1, c2 = st.columns((1,1))
         
    with c1: financials = st.radio('Select between Income Statement, Balance Sheet and Cash Flow',['Income Statement', 'Balance Sheet', 'Cash Flow'])          

    with c2: frequency = st.radio('Select between Annual and Quaterly period', ['Annual','Quaterly'])
    
    
    if ticker != '':
        if financials == 'Income Statement' and frequency == 'Annual':
        
            st.dataframe(yf.Ticker(ticker).financials, use_container_width=True)
            
        elif financials == 'Income Statement' and frequency == 'Quaterly':
            
            st.dataframe(yf.Ticker(ticker).quarterly_financials, use_container_width=True)
        
        elif financials == 'Balance Sheet' and frequency == 'Annual':
            
            st.dataframe(yf.Ticker(ticker).balance_sheet, use_container_width=True)
        
        elif financials == 'Balance Sheet' and frequency == 'Quaterly':
            
            st.dataframe(yf.Ticker(ticker).quaterly_balance_sheet, use_container_width=True)
            
        elif financials == 'Cash Flow' and frequency == 'Annual':
             
            st.dataframe(yf.Ticker(ticker).cashflow, use_container_width=True)
        
        elif financials == 'Cash Flow' and frequency == 'Quaterly':
            
            st.dataframe(yf.Ticker(ticker).quaterly_cashflow, use_container_width=True)
        


#==============================================================================
# Tab 4
#==============================================================================

def tab4():
    
    # Add a title for the Monte Carlo Simulation
    st.title("Monte Carlo Simulation")
    st.header("Tab 4 - Monte Carlo Simulation")
    
    # Add columns for the simulations and time horizon selection
    c1, c2 = st.columns((1,1))
    
    with c1: nbr_simulation = st.selectbox("Select simulations", ['200', '500', '1000'])          

    with c2: t_time_horizon = st.selectbox("Select a time-horizon", ['30', '60', '90'])
    
    
    
    # The Monte Carlo Simulation
    
    class MonteCarlo(object):
        
        def __init__(self, ticker, data_source, start_date, end_date, time_horizon, simulations):
            
            # Initiate class variables
            self.ticker = ticker  # Stock ticker
            self.data_source = data_source
            self.start_date = start_date  # Text, YYYY-MM-DD
            self.end_date = end_date
            self.time_horizon = time_horizon  # Days
            self.simulations = nbr_simulation  # Number of simulations
            self.results_df = pd.DataFrame()  # Table of results
            
            # Extract stock data
            self.stock_price_tab4 = web.DataReader(self.ticker, self.data_source, self.start_date, self.end_date)
            
            # Calculate financial metrics focused on the closing price
            # Daily return (of close price)
            self.daily_return = self.stock_price_tab4['Close'].pct_change()
            # Volatility (of close price)
            self.daily_volatility = self.daily_return.std()
    
        
        def run_simulation(self):
            
    
            # DataFrame to store the results of the 1000 simulations
            self.results_df = pd.DataFrame()

            for n_time in range(int(self.simulations)):
                mu = 0
                sd = self.daily_volatility

                last_close_price = self.stock_price_tab4['Close'][-1]

                # List to store stock price
                stock_price_list = []

                # Loop for 200 days
                for day in range(int(self.time_horizon)):

                    # Generate the random pct change
                    random_pct_change = np.random.normal(mu, sd)

                    # Calculate the stock of the current day
                    stock_price_today = last_close_price * (1 + random_pct_change)

                    # Store the stock price
                    stock_price_list.append(stock_price_today)

                    # Re-adjust the last close price
                    last_close_price = stock_price_today
    
    
                self.results_df = pd.concat([self.results_df, pd.Series(stock_price_list)], axis=1)
        
        def plot_simulation(self):
            
            # Plot the simulation stock price in the future
            fig, ax = plt.subplots()
            fig.set_size_inches(15, 10, forward=True)

            plt.plot(self.results_df)
            plt.title('Monte Carlo simulation for ' + self.ticker + \
                  ' stock price in next ' + str(self.time_horizon) + ' days')
            plt.xlabel('Day')
            plt.ylabel('Price')

            plt.axhline(y=self.stock_price_tab4['Close'][-1], color='red')
            plt.legend(['Current stock price is: ' + str(np.round(self.stock_price_tab4['Close'][-1], 2))])
            ax.get_legend().legendHandles[0].set_color('red')
            
            st.pyplot(fig)
        
        def value_at_risk(self):
        # Price at 95% confidence interval
            future_price_95ci = np.percentile(self.results_df.iloc[-1:, :].values[0, ], 5)

            # Value at Risk
            VaR = self.stock_price_tab4['Close'][-1] - future_price_95ci
            st.subheader('VaR at 95% confidence interval is: ' + str(np.round(VaR, 2)) + ' USD')
            
    # Call the function
    sim = MonteCarlo(ticker=ticker,data_source='yahoo',start_date=start_date,end_date=today,
            time_horizon=t_time_horizon, simulations=nbr_simulation)
    
    sim.run_simulation()
    sim.plot_simulation()
    sim.value_at_risk()
    

#==============================================================================
# Tab 5
#==============================================================================

def tab5():
    
    # Add a title for the Monte Carlo Simulation
    st.title("The SMA strategy")
    st.header("Tab 5 - Financial Analysis")
    
    st.write('The Simple Moving Average (SMA) is one of the oldest technical indicator which calculates the average value of a set of prices over a specific period.')
    st.write('In this tab, I present to you a simple SMA strategy which basically compare the SMA and the Close Price of the same day to signal if we should either buy it or sell it.')
    
    def SMA(data, period=50, column='Close'):
        return data[column].rolling(window=period).mean()
    
    stock_price = yf.Ticker(ticker).history(start=start_date, end=end_date)
    stock_price['SMA50']=SMA(stock_price)
        
    def strategy(df):
        
        buy = [] #Create an empty list
        sell = [] #Create an empty list
        flag = 0
        buy_price = 0
        
        for i in range(0, len(df)):
            
            if df['SMA50'][i] > df['Close'][i] and flag == 0:
                buy.append(df['Close'][i])
                sell.append(np.nan)
                buy_price = df['Close'][i]
                flag = 1
            
            elif df['SMA50'][i] < df['Close'][i] and flag == 1 and buy_price < df['Close'][i]:
                sell.append(df['Close'][i])
                buy.append(np.nan)
                buy_price = 0
                flag =0
            
            else:
                sell.append(np.nan)
                buy.append(np.nan)
                
        return (buy,sell)
    
    
    #Add the buy and sell list to the stock_price dataframe
    stock_price['Buy'] = strategy(stock_price)[0]
    stock_price['Sell'] = strategy(stock_price)[1]
    
    
    # Creating figure with second y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Adding line plot with close prices and bar plot with trading volume
    fig.add_trace(go.Scatter(x=stock_price.index, y=stock_price['Close'], name='Closing Price'), secondary_y=False)
    fig.add_trace(go.Scatter(x=stock_price.index, y=stock_price['SMA50'], name='SMA'), secondary_y=False)
    
    #Visualize the buy and sell signals
    fig.add_trace(go.Scatter(x=stock_price.index, y=stock_price['Buy'], name='Buy Signal', mode='markers', marker=dict(symbol='triangle-up', size=15, color='green')), secondary_y=False)
    fig.add_trace(go.Scatter(x=stock_price.index, y=stock_price['Sell'], name='Sell Signal', mode='markers', marker=dict(symbol='triangle-down', size=15, color='blue')), secondary_y=False)
    
    
    # Updating layout
    fig.update_layout(
        width=500,
        height=800,
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_white',
        xaxis_rangeslider_visible=True,
        hovermode='x'
        )
    
    # Disabling grid of second y-axis
    fig.layout.yaxis2.showgrid=False
    
    fig.update_layout(xaxis_rangeslider_visible=False)
    
    #Show the graph
    st.plotly_chart(fig, use_container_width=True)
     
#==============================================================================
# Main body
#==============================================================================

def run():
    
    # Add the ticker selection on the sidebar
    # Get the list of stock tickers from S&P500
    ticker_list = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol']
    
    # Add selection box
    global ticker
    ticker = st.sidebar.selectbox("Select a ticker", ticker_list)
    
    
    # Add select begin-end date
    global start_date, end_date
    col1, col2 = st.sidebar.columns(2)
    start_date = col1.date_input("Start date", datetime.today().date() - timedelta(days=30))
    end_date = col2.date_input("End date", datetime.today().date())
    
    if start_date < end_date:
        st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
    else:
        st.sidebar.error('Error: End date must fall after start date.')
    
    # Add a radio box
    select_tab = st.sidebar.radio("Tabs", ['Summary', 'Chart', 'Financials', 'Monte Carlo Simulation', 'Financial Analysis'])
    
    # defining an update button:
    run_button = st.sidebar.button('Update Data')
    if run_button:
        st.experimental_rerun()
    
    # Show the selected tab
    if select_tab == 'Summary':
        # Run tab 1
        tab1()
    elif select_tab == 'Chart':
        # Run tab 2
        tab2()
    elif select_tab == 'Financials':
        # Run tab 3
        tab3()
    elif select_tab == 'Monte Carlo Simulation':
        # Run tab 4
        tab4()
    elif select_tab == 'Financial Analysis':
        # Run tab 4
        tab5()
    
        
    def GetCompanyInfo(ticker):
        return yf.Ticker(ticker).info
    
           
    if ticker != '':
        # Get the company information in list format
        info = GetCompanyInfo(ticker)
            
        st.sidebar.image(info['logo_url'], width = 300)
        
        
    
if __name__ == "__main__":
    run()
    
###############################################################################
# END
###############################################################################