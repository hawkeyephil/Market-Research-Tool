#Import statements
import pandas_datareader.data as reader
import pandas as panda 
import numpy as numpy 
from IPython.display import display 
from tabulate import tabulate 

#Create a new dataframe to store results
exchange_Rate_Data = panda.DataFrame(columns=['Economy', 'Currency', 'Exchange Rate to USD', 
                'Exchange Rate Date', 'GDP', 'GDP Date'])#, 'Inflation Rate', 'Inflation Rate Date'])

#Currency codes for X Currency to U.S. Dollars spot exchange rate from the FRED database 
#currency_Codes_ToUSD = [('Canadian Dollar', 'DEXCAUS'), ('Swiss Franc', 'DEXSZUS')] 
economey_Codes = [('Canada', 'Canadian Dollar', 'DEXCAUS', 'NGDPRSAXDCCAQ', 'CANCPALTT01CTGYM'), ('Switzerland', 'Swiss Franc', 'DEXSZUS', 'CPMNACSAB1GQCH', 'CHECPALTT01CTGYM')]
#Currency codes for U.S. Dollars to X Currecny spot exchange rate from the FRED database 
#currency_Codes_FromUSD = [('Euro', 'DEXUSEU'), ('Pound Sterling', 'DEXUSUK')] 

#Fetches the exchange rate data for specified currencies and adds the most recent observation to the data frame
for economy, currency, currency_Code, output_Code, inflation_Code in economey_Codes: 
    exchange_Rate = reader.DataReader(currency_Code, 'fred') 
    output = reader.DataReader(output_Code, 'fred') 
    exchange_Rate_Recent = exchange_Rate.tail(1)[currency_Code][0] 
    output_Recent = output.tail(1)[output_Code][0]
    exchange_Rate_Date = exchange_Rate.tail(1).index.strftime('%Y-%m-%d')[0] 
    output_Date = output.tail(1).index.strftime('%Y-%m-%d')[0]
    new_Row = {'Economy': economy, 'Currency': currency, 'Exchange Rate to USD': exchange_Rate_Recent, 'Exchange Rate Date': exchange_Rate_Date, 'GDP': output_Recent, 'GDP Date': output_Date} 
    exchange_Rate_Data = exchange_Rate_Data.append(new_Row, ignore_index=True) 
 
def macro_Variable_Collector(macro_Variable_Codes): 
    macro_Variables_Dates = []
    for macro_Variable_Code, macro_Variable_Source in macro_Variable_Codes: 
        macro_Variable = reader.DataReader(macro_Variable_Code, macro_Variable_Source) 
        macro_Variable_Recent = macro_Variable.tail(1)[macro_Variable_Code][0] 
        macro_Variable_Date = macro_Variable.tail(1).index.strftime('%Y-%m-%d')[0] 
        macro_VariableDate = str(macro_Variable_Recent) + ' ' + str(macro_Variable_Date)
        macro_Variables_Dates.append(macro_VariableDate) 
    print(macro_Variables_Dates)
    return macro_Variables_Dates 

test = [('DEXCAUS', 'fred'), ('DEXSZUS', 'fred')]
macro_Variable_Collector(test)

#Fetches the exchange rate data for specified currencies, inverts to USD, and adds the most recent observation to the data frame
#for name, currency_Code in currency_Codes_FromUSD:
    #exchange_Rate = reader.DataReader(currency_Code, 'fred') 
    #exchange_Rate_Recent = exchange_Rate.tail(1)[currency_Code][0] 
    #exchange_Rate_Recent = 1/exchange_Rate_Recent
    #exchange_Rate_Date = exchange_Rate.tail(1).index.strftime('%Y-%m-%d')[0] 
    #new_Row = {'Currency': name, 'Currency Code': currency_Code, 'Date': exchange_Rate_Date, 'Exchange Rate to USD': exchange_Rate_Recent} 
    #exchange_Rate_Data = exchange_Rate_Data.append(new_Row, ignore_index=True)


#Returns the data frame containing the most recent exchange rate data from the FRED 
#tabulate package allows for multiple formats: plain, pretty, psql, html, etc
print(tabulate(exchange_Rate_Data, headers = 'keys', tablefmt = 'plain'))
