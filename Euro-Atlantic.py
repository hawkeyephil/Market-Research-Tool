#Import statements
import pandas_datareader.data as reader
import pandas as panda 
import numpy as numpy 
from IPython.display import display 
from tabulate import tabulate 

euro_Atlantic_Codes = [('Canada', 'Canadian Dollar', 'DEXCAUS', 'fred', 'NGDPRSAXDCCAQ', 'fred', 'CANCPALTT01CTGYM', 'fred'), ('Switzerland', 'Swiss Franc', 'DEXSZUS', 'fred', 'CPMNACSAB1GQCH', 'fred', 'CHECPALTT01CTGYM', 'fred')]

def macro_Variable_Collector(macro_Variable_Codes): 
    macro_Variables_Dates = []
    for macro_Variable_Code, macro_Variable_Source in macro_Variable_Codes: 
        macro_Variable = reader.DataReader(macro_Variable_Code, macro_Variable_Source) 
        macro_Variable_Recent = macro_Variable.tail(1)[macro_Variable_Code][0] 
        macro_Variable_Recent = "{:.4g}".format(macro_Variable_Recent)
        macro_Variable_Date = macro_Variable.tail(1).index.strftime('%Y-%m-%d')[0] 
        macro_VariableDate = str(macro_Variable_Recent) + ' (' + str(macro_Variable_Date) + ')'
        macro_Variables_Dates.append(macro_VariableDate) 
    return macro_Variables_Dates 

def report_Generator(region_Codes): 
    exchange_Rate_Codes = [] 
    output_Codes = [] 
    inflation_Codes = [] 
    for economy, currency, exchange_Rate_Code, exchange_Rate_Source, output_Code, output_Source, inflation_Code, inflation_Source in region_Codes: 
        exchange_Rate_Codes.append((exchange_Rate_Code, exchange_Rate_Source)) 
        output_Codes.append((output_Code, output_Source)) 
        inflation_Codes.append((inflation_Code, inflation_Source)) 
    exchange_Rates = macro_Variable_Collector(exchange_Rate_Codes) 
    outputs = macro_Variable_Collector(output_Codes)
    inflation_Rates = macro_Variable_Collector(inflation_Codes) 
    counter = 0 
    euro_Atlantic_Data = panda.DataFrame(columns=['Economy', 'Currency', 'Exchange Rate to USD', 'GDP', 'Inflation Rate'])
    for economy, currency, exchange_Rate_Code, exchange_Rate_Source, output_Code, output_Source, inflation_Code, inflation_Source in region_Codes: 
        new_Row = {'Economy': economy, 'Currency': currency, 'Exchange Rate to USD': exchange_Rates[counter], 'GDP': outputs[counter], 'Inflation Rate': inflation_Rates[counter]} 
        euro_Atlantic_Data = euro_Atlantic_Data.append(new_Row, ignore_index = True) 
        counter = counter + 1  
    return euro_Atlantic_Data

report = report_Generator(euro_Atlantic_Codes) 
print(tabulate(report, headers = 'keys', tablefmt = 'plain'))