#Import statements
import pandas_datareader.data as reader
import pandas as panda 
from IPython.display import display 
from tabulate import tabulate 

#Create a new dataframe to store results
exchange_Rate_Data = panda.DataFrame(columns=['Currencies', 'Currency Code', 'Date', 'Exchange Rate'])

#Currency codes for X Currency to U.S. Dollars spot exchange rate from the FRED database 
currency_Codes_ToUSD = [('JapaneseYen-USD', 'DEXJPUS'), ('CanadianDollar-USD', 'DEXCAUS'), ('SwissFranc-USD', 'DEXSZUS')] 
#Currency codes for U.S. Dollars to X Currecny spot exchange rate from the FRED database 
currency_Codes_FromUSD = [('Euro-USD', 'DEXUSEU'), ('Pounds-USD', 'DEXUSUK'), ('AustralianDollars-USD', 'DEXUSAL')] 

#Fetches the exchange rate data for specified currencies and adds the most recent observation to the data frame
for name, currency_Code in currency_Codes_ToUSD: 
    exchange_Rate = reader.DataReader(currency_Code, 'fred') 
    exchange_Rate_Recent = exchange_Rate.tail(1)[currency_Code][0] 
    exchange_Rate_Date = exchange_Rate.tail(1).index.strftime('%Y-%m-%d')[0] 
    new_Row = {'Currencies': name, 'Currency Code': currency_Code, 'Date': exchange_Rate_Date, 'Exchange Rate': exchange_Rate_Recent} 
    exchange_Rate_Data = exchange_Rate_Data.append(new_Row, ignore_index=True) 

#Fetches the exchange rate data for specified currencies, inverts to USD, and adds the most recent observation to the data frame
for name, currency_Code in currency_Codes_FromUSD:
    exchange_Rate = reader.DataReader(currency_Code, 'fred') 
    exchange_Rate_Recent = exchange_Rate.tail(1)[currency_Code][0] 
    exchange_Rate_Recent = 1/exchange_Rate_Recent
    exchange_Rate_Date = exchange_Rate.tail(1).index.strftime('%Y-%m-%d')[0] 
    new_Row = {'Currencies': name, 'Currency Code': currency_Code, 'Date': exchange_Rate_Date, 'Exchange Rate': exchange_Rate_Recent} 
    exchange_Rate_Data = exchange_Rate_Data.append(new_Row, ignore_index=True) 


#Returns the data frame containing the most recent exchange rate data from the FRED 
#tabulate package allows for multiple formats: plain, pretty, psql, html, etc
print(tabulate(exchange_Rate_Data, headers = 'keys', tablefmt = 'psql'))
