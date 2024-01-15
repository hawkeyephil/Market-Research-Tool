#Import statements
import pandas_datareader.data as reader
import pandas as panda 
import numpy as numpy 
from IPython.display import display 
from tabulate import tabulate 
from datetime import date

euro_Atlantic_Codes = [('Canada', 'Canadian Dollar', 'DEXCAUS', 'fred', 'na', 'NAEXKP01CAQ657S', 'fred', 'CANCPALTT01CTGYM', 'fred'), 
                       ('Switzerland', 'Swiss Franc', 'DEXSZUS', 'fred', 'na', 'CHEGDPRQPSMEI', 'fred', 'CHECPALTT01CTGYM', 'fred'), 
                       ('United Kingdom', 'Pound Sterling', 'DEXUSUK', 'fred', 'inversion', 'NAEXKP01GBQ657S', 'fred', 'GBRCPALTT01CTGYM', 'fred'), 
                       ('Euro Area', 'Euro', 'DEXUSEU', 'fred', 'inversion', 'NAEXKP01EZQ657S', 'fred', 'CPHPTT01EZM659N', 'fred')]

def macro_Variable_Collector(macro_Variable_Codes): 
    macro_Variables_Dates = panda.DataFrame(columns=['macro_Variable_Recent', 'macro_Variable_Date', 'special_Behavior'])
    for macro_Variable_Code, macro_Variable_Source, special_Behavior in macro_Variable_Codes: 
        macro_Variable = reader.DataReader(macro_Variable_Code, macro_Variable_Source) 
        macro_Variable_Recent = macro_Variable.tail(1)[macro_Variable_Code][0] 
        macro_Variable_Date = macro_Variable.tail(1).index.strftime('%m-%d-%Y')[0]   
        macro_Variable_Date = str(macro_Variable_Date)
        new_Row = {'macro_Variable_Recent': macro_Variable_Recent, 'macro_Variable_Date': macro_Variable_Date, 'special_Behavior': special_Behavior}
        macro_Variables_Dates = macro_Variables_Dates.append(new_Row, ignore_index = True) 
    return macro_Variables_Dates 

def exchange_Rate_Generator(exchange_Rate_Codes):  
    exchange_Rates = macro_Variable_Collector(exchange_Rate_Codes) 
    exchange_Rates_Adjusted = [] 
    for index, row in exchange_Rates.iterrows(): 
        if(row["special_Behavior"] == 'inversion'): 
            row["macro_Variable_Recent"] = 1/row["macro_Variable_Recent"]
        exchange_Rates_Adjusted.append(str("{:.3g}".format(row["macro_Variable_Recent"])) + ' (' + row["macro_Variable_Date"] + ')')
    return (exchange_Rates_Adjusted) 

def output_Generator(output_Codes): 
    outputs = macro_Variable_Collector(output_Codes) 
    outputs_Adjusted = []
    for index, row in outputs.iterrows():        
        outputs_Adjusted.append(str( "{:.3g}".format(row["macro_Variable_Recent"])) + '% (' + row["macro_Variable_Date"] + ')')
    return (outputs_Adjusted) 

def inflation_Rate_Generator(inflation_Rate_Codes): 
    inflation_Rates = macro_Variable_Collector(inflation_Rate_Codes)  
    inflation_Rates_Adjusted = []
    for index, row in inflation_Rates.iterrows(): 
        inflation_Rates_Adjusted.append(str( "{:.4g}".format(row["macro_Variable_Recent"])) + '% (' + row["macro_Variable_Date"] + ')')
    return (inflation_Rates_Adjusted) 

def report_Generator(region_Codes): 
    exchange_Rate_Codes = [] 
    output_Codes = [] 
    inflation_Codes = [] 
    for economy, currency, exchange_Rate_Code, exchange_Rate_Source, exchange_Rate_Inversion, output_Code, output_Source, inflation_Code, inflation_Source in region_Codes: 
        exchange_Rate_Codes.append((exchange_Rate_Code, exchange_Rate_Source, exchange_Rate_Inversion)) 
        output_Codes.append((output_Code, output_Source, 'na')) 
        inflation_Codes.append((inflation_Code, inflation_Source, 'na')) 
    exchange_Rates = exchange_Rate_Generator(exchange_Rate_Codes) 
    outputs = output_Generator(output_Codes)
    inflation_Rates = inflation_Rate_Generator(inflation_Codes) 
    counter = 0 
    euro_Atlantic_Data = panda.DataFrame(columns=['Economy', 'Currency', 'Exchange Rate to USD', 'Percent Change GDP YoY (Seasonally Adjusted)', 'Percent Change CPI YoY (Not Seasonally Adjusted)'])
    for economy, currency, exchange_Rate_Code, exchange_Rate_Source, exchange_Rate_Inversion, output_Code, output_Source, inflation_Code, inflation_Source in region_Codes: 
        new_Row = {'Economy': economy, 'Currency': currency, 'Exchange Rate to USD': exchange_Rates[counter], 'Percent Change GDP YoY (Seasonally Adjusted)': outputs[counter], 'Percent Change CPI YoY (Not Seasonally Adjusted)': inflation_Rates[counter]} 
        euro_Atlantic_Data = euro_Atlantic_Data.append(new_Row, ignore_index = True) 
        counter = counter + 1  
    return euro_Atlantic_Data

report = report_Generator(euro_Atlantic_Codes) 
today = date.today().strftime('%m-%d-%Y')
filename = '~/Downloads/Euro-Atlantic Report (' + today + ").csv"
report.to_csv(filename, index = False)
print(tabulate(report, headers = 'keys', tablefmt = 'plain')) 