# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 16:00:38 2022

@author: schauvin
"""

# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go


# periods to select
periodDict = {'DurationText':['1M','3M','6M','YTD','1Y','2Y','5Y','MAX'], 'DurationN':[30,90,120,335,365,730,1825,18250]}
periods= pd.DataFrame(periodDict)

######################################################################################################################################
######################################################################################################################################
######################################################################################################################################

# defining first tab1: Summary ############################################

# start and end date of the plot data 
today = datetime.today().date()
#########display pct and usd change next to the price####################
#Current= (si.get_data('AAPL', start_date=today, end_date=today))['close']
#openprice= (si.get_data('AAPL', start_date=today, end_date=today))['open']

def PageBeginning():
        #display chosen ticker name
    st.title(ticker)
        #display subheader 
    x1,x2,x3 = st.columns(3)
    with x1:
            #get live price of the chosen ticker
        st.header(round(yf.get_live_price(ticker),2))
    #with x2:
        #st.subheader(  round((((Current/openprice)-1)*100).item(),2)   )
    #with x3:
        #st.subheader(     round((Current-openprice).item()),2)
        ############ captions for date time####################
    st.caption('S&P500 Real Time Price. Currency in USD.')
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M")
    st.caption("as of " + dt_string + " CET")
    #######################################################
    return

def tab1():

    PageBeginning()
    #######################################################################################################
    #buttons to select desired period of data 
    buttons_tab1 = st.selectbox("select period",periods['DurationText'])
  
    ########################################################################################################

    #plots for each selected duration: 
    def PlotTab1(buttons_tab1): 
        x = today-timedelta(periods.loc[periods['DurationText']==buttons_tab1,'DurationN'].iloc[0].item()) #start date that varies with selected period
        closing_price= yf.get_data(ticker, start_date=x, end_date=today) #data for the plots
        fig,ax = plt.subplots(figsize=(10,5))
        ax.plot(closing_price['close'], label='Closing Price',color='green')
        #plt.fill_between(closing_price.index, closing_price['close'],color='green') #fill the color under the line
        ax2=ax.twinx() #twinning bar chart plot
        ax2.bar(closing_price.index,closing_price['volume'], label='Volume mlns',color='mediumseagreen') #plotting bar chart
        ax2.set_ylim(0,((closing_price['volume'].max())*5)) # diminishing the scale of the bar char 
        ax2.set_yticks([])  #hiding y ticks of bar chart from the plot
        ax.yaxis.tick_right() #moving ticks to the right side
        my_xticks = ax.get_xticks() #store ticks in np array
        ax.set_xticks([my_xticks[0], np.median(my_xticks),my_xticks[-1]]) # only show 1st and median ticks in the plot
        ######Legend labels for both axes shown together in one legend:########
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc=0)
        ax.set_frame_on(False) 
        ax2.set_frame_on(False)
        #######################################################################
        st.pyplot(fig)
    PlotTab1(buttons_tab1=buttons_tab1) #call the function

    ################defining columns and tables to show summary data in two columns########################
    col1, col2 = st.columns(2)
    QuoteTable = yf.get_quote_table(ticker, dict_result=False)
    QuoteTable['value'] = QuoteTable['value'].astype(str)
    QuoteTable = QuoteTable.drop(15) #dropping one of the lines from the df to divide equally into 2 cols

    with col1: 
        st.dataframe(QuoteTable.iloc[:8,:].assign(hack='').set_index('hack')) #showing df and hiding index col
    with col2:
        st.dataframe(QuoteTable.iloc[8:,].assign(hack='').set_index('hack'))
    #######################################################################################################    


######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
   
#defining tab 2
def tab2():
    PageBeginning()

    # Add select begin-end date options
    col1, col2 = st.columns(2)
    start_date = col1.date_input("Start date", datetime.today().date() - timedelta(days=30))
    end_date = col2.date_input("End date", datetime.today().date())
    # added selectbox for data intervals
    intervalDict = {'IntervalButton':['Daily','Weekly','Monthly'],'IntervalCode':['1d','1wk','1mo']}
    intervals= pd.DataFrame(intervalDict)
    time_interval_button = st.selectbox('Interval',intervals['IntervalButton'])
    #added radio boxes to choose a graph type
    plot_type = st.radio('Plot type',['Line','Candle'])
   

    if plot_type =='Line':
    #plotting 
        def PlotTab2(start_date, end_date, time_interval_button):
            # data used in tab2 for closing price
            Tab2_ClosingPrice = yf.get_data(ticker,start_date=start_date,end_date=end_date,interval=(intervals.loc[intervals['IntervalButton']==time_interval_button,'IntervalCode'].iloc[0]))
            fig,ax = plt.subplots(figsize=(10,5))
            ax.plot(Tab2_ClosingPrice['close'], label='Closing Price', color='green')
            ax2=ax.twinx() #twinning the first ax
            ax2.bar(Tab2_ClosingPrice.index,Tab2_ClosingPrice['volume'], label='Volume mlns',color='mediumseagreen') #plotting bar chart
            ax2.set_ylim(0,((Tab2_ClosingPrice['volume'].max())*5)) # diminishing the scale of the bar char 
            ax2.set_yticks([])  #hiding y ticks of bar chart from the plot
            ax.yaxis.tick_right() #moving ticks to the right side
            my_xticks = ax.get_xticks() #store ticks in np array
            ax.set_xticks([my_xticks[0], np.median(my_xticks),my_xticks[-1]]) # only show 1st and median ticks in the plot
            ######Legend labels for both axes shown together in one legend:########
            lines, labels = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax2.legend(lines + lines2, labels + labels2, loc=0)
            ax.set_frame_on(False)
            ax2.set_frame_on(False)

            return st.pyplot(fig)  
        PlotTab2(start_date=start_date,end_date=end_date, time_interval_button=time_interval_button)
    else: 
        #plotting candle chart using py plot
        Data_CandleSt = yf.get_data(ticker,start_date=start_date,end_date=end_date,interval=(intervals.loc[intervals['IntervalButton']==time_interval_button,'IntervalCode'].iloc[0]))
        fig = go.Figure(data=[go.Candlestick(x=Data_CandleSt.index,
                open=Data_CandleSt['open'],
                high=Data_CandleSt['high'],
                low=Data_CandleSt['low'],
                close=Data_CandleSt['close'])])
        #fig = go.bar(Data_CandleSt, x=Data_CandleSt.index, y=Data_CandleSt['Volume']) volume to be added 
        fig.update_layout(xaxis_rangeslider_visible=False)
        st.plotly_chart(fig)

######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
   
# tab3 Statistics: 
def tab3():
    PageBeginning()
    col1, col2 = st.columns(2) #dividing into two columns

    with col1:
        #get valuation 
        st.header('Valuation Measures')
        st.dataframe(yf.get_stats_valuation(ticker).assign(hack='').set_index('hack'))
        
        dataTab3 = yf.get_stats(ticker)
        #dataTab3.columns = [''] * len(dataTab3.columns)

        st.header('Financial Highlights')
        st.subheader('Fiscal Year')
        st.dataframe(dataTab3.iloc[29:31].assign(hack='').set_index('hack'))

        st.subheader('Profitability')
        st.dataframe(dataTab3.iloc[31:33].assign(hack='').set_index('hack'))

        st.subheader('Management Effectiveness')
        st.dataframe(dataTab3.iloc[32:34].assign(hack='').set_index('hack'))

        st.subheader('Income Statement')
        st.dataframe(dataTab3.iloc[35:43].assign(hack='').set_index('hack'))

        st.subheader('Balance Sheet')
        st.dataframe(dataTab3.iloc[43:49].assign(hack='').set_index('hack'))

        st.subheader('Cash Flow Statement')
        st.dataframe(dataTab3.iloc[49:].assign(hack='').set_index('hack'))
    with col2:
        st.header('Trading rmation')
        st.subheader('Stock Price History')
        st.dataframe(dataTab3.iloc[:7].assign(hack='').set_index('hack'))

        st.subheader('Share Statistics')
        st.dataframe(dataTab3.iloc[7:15].assign(hack='').set_index('hack'))

        st.subheader('Dividends & Splits')
        st.dataframe(dataTab3.iloc[10:29].assign(hack='').set_index('hack'))


######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
def tab4():

    FinancialReportType = st.selectbox('Show:',['Income Statement','Balance Sheet','Cash Flow']) #selectbox to select FS type
    PeriodDict = {'Report':['Annual','Quarterly'],'ReportCode':[True,False]}
    PeriodDF=pd.DataFrame(PeriodDict)
    PeriodType = st.radio('Report:',PeriodDF['Report']) #radio to select report period

    def ShowReport(FinancialReportType,PeriodType): #defining a function to display the data according to selected parameters
        if FinancialReportType == 'Income Statement': 
            st.subheader(PeriodType +' Income Statement for '+ ticker)
            x = yf.get_income_statement(ticker,yearly=(PeriodDF.loc[PeriodDF['Report']==PeriodType,'ReportCode'].iloc[0]))
            #selecting data. For yearly true or false refering to the DF PeriodDF to select True or False depending on Annual or Quarterly selection in radiobox
        elif FinancialReportType == 'Balance Sheet':
            st.subheader(PeriodType + ' Balance Sheet Statement for '+ ticker)
            x = yf.get_cash_flow(ticker,yearly=(PeriodDF.loc[PeriodDF['Report']==PeriodType,'ReportCode'].iloc[0]))
        elif FinancialReportType == 'Cash Flow':
            st.subheader(PeriodType +' Cash Flow Statement for '+ ticker)
            x= yf.get_balance_sheet(ticker,yearly=(PeriodDF.loc[PeriodDF['Report']==PeriodType,'ReportCode'].iloc[0]))
        return st.dataframe(x)
    ShowReport(FinancialReportType=FinancialReportType, PeriodType=PeriodType)
    

######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
def tab5():
     st.subheader('Analysts  for '+ ticker)
     st.dataframe(yf.get_analysts_(ticker)['Earnings Estimate'].assign(hack='').set_index('hack')) #again, assign hides index values from printing
     st.dataframe(yf.get_analysts_(ticker)['Revenue Estimate'].assign(hack='').set_index('hack'))
     st.dataframe(yf.get_analysts_(ticker)['Earnings History'].assign(hack='').set_index('hack'))
     st.dataframe(yf.get_analysts_(ticker)['EPS Trend'].assign(hack='').set_index('hack'))
     st.dataframe(yf.get_analysts_(ticker)['EPS Revisions'].assign(hack='').set_index('hack'))
     st.dataframe(yf.get_analysts_(ticker)['Growth Estimates'].assign(hack='').set_index('hack'))

    

######################################################################################################################################
######################################################################################################################################
######################################################################################################################################

 
#Creating a sidebar menu
def run(): #function to run the entire dashboard at once
    
    # Add the ticker selection on the sidebar
    # Get the list of stock tickers from S&P500
    ticker_list = ['-'] + yf.tickers_sp500()

    # Add selection box
    global ticker #move the ticker variable to global var names.
    ticker = st.sidebar.selectbox("Select a ticker", ticker_list)
    
    # Add a radio box
    select_tab = st.sidebar.radio("Select tab", ['Summary', 'Chart', 'Statistics','Financials','Analysis','Monte Carlo Simulation'])
     
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
    elif select_tab == 'Statistics':
        tab3()
    elif select_tab == 'Financials':
        tab4()
    elif select_tab == 'Analysis':
        tab5()
    elif select_tab == 'Monte Carlo Simulation':
        tab6()

    
if __name__ == "__main__":
    run()