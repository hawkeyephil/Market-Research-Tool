#Author: Phil Caldarella 
#Descriptions: Generates .csv file with most recent exchange rate, change GDP, and change CPI from various 
#Euro-Atlantic economies for quick overview of the region 

#Import statements 
#These are additional packages that need to be installed 
import pandas_datareader.data as reader
import pandas as panda 
import numpy as numpy 
#These are in base Python (already installed with Python) 
from IPython.display import display 
from tabulate import tabulate 
from datetime import date

#Codes for the Euro-Atlantic Reports with source and unique behavior stored in a 2D List  
#Format: (Economy, Currency, Currecny Code, Currency Source, Inversion to USD, GDP Code, GDP Source, Inflation Code, Inflation Source)
euro_Atlantic_Codes = [('Canada', 'Canadian Dollar', 'DEXCAUS', 'fred', 'na', 'NAEXKP01CAQ657S', 'fred', 'CANCPALTT01CTGYM', 'fred'), 
                       ('Switzerland', 'Swiss Franc', 'DEXSZUS', 'fred', 'na', 'CHEGDPRQPSMEI', 'fred', 'CHECPALTT01CTGYM', 'fred'), 
                       ('United Kingdom', 'Pound Sterling', 'DEXUSUK', 'fred', 'inversion', 'NAEXKP01GBQ657S', 'fred', 'GBRCPALTT01CTGYM', 'fred'), 
                       ('Euro Area', 'Euro', 'DEXUSEU', 'fred', 'inversion', 'NAEXKP01EZQ657S', 'fred', 'CPHPTT01EZM659N', 'fred')]

#Function that qurries source for data and date given a 2D list (code, source, special behavior) 
def macro_Variable_Collector(macro_Variable_Codes): 
    #Dataframe that contains the most recent observation, date observation was taken, and any special behavior 
    macro_Variables_Dates = panda.DataFrame(columns=['macro_Variable_Recent', 'macro_Variable_Date', 'special_Behavior']) 
    #Loops which collects data on each variable passed in the macro_Variable_Codes array 
    for macro_Variable_Code, macro_Variable_Source, special_Behavior in macro_Variable_Codes: 
        #Query data soruce for select code 
        macro_Variable = reader.DataReader(macro_Variable_Code, macro_Variable_Source) 
        #Most recent observation only 
        macro_Variable_Recent = macro_Variable.tail(1)[macro_Variable_Code][0] 
        #Most recent observation date 
        macro_Variable_Date = macro_Variable.tail(1).index.strftime('%m-%d-%Y')[0] 
        #Turns date into a string for later ease of combination  
        macro_Variable_Date = str(macro_Variable_Date) 
        #Creates a new row entry with the observation, date, and special behavior 
        new_Row = {'macro_Variable_Recent': macro_Variable_Recent, 'macro_Variable_Date': macro_Variable_Date, 'special_Behavior': special_Behavior} 
        #Adds the row to the macro_Variables_Dates data frame 
        macro_Variables_Dates = macro_Variables_Dates.append(new_Row, ignore_index = True) 
    return macro_Variables_Dates 

def exchange_Rate_Generator(exchange_Rate_Codes): 
    #Calls the macro_Variable_Collector function (above function) to collect exchange rate data 
    exchange_Rates = macro_Variable_Collector(exchange_Rate_Codes) 
    #New list which holds exchange rate data after adjustments are made 
    exchange_Rates_Adjusted = [] 
    #Iterates through each exchange rate  
    for index, row in exchange_Rates.iterrows(): 
        #Inverts the exchange rate to USD if needed 
        if(row["special_Behavior"] == 'inversion'): 
            row["macro_Variable_Recent"] = 1/row["macro_Variable_Recent"] 
        #Reduces sig figs of exchange rate and appends the observation date 
        exchange_Rates_Adjusted.append(str("{:.3g}".format(row["macro_Variable_Recent"])) + ' (' + row["macro_Variable_Date"] + ')')
    #Returns list of exchange rates after cleaning 
    return (exchange_Rates_Adjusted) 

def output_Generator(output_Codes): 
    #Calls the macro_Variable_Collector function to collect GDP data 
    outputs = macro_Variable_Collector(output_Codes) 
    #New list which holds GDP data after adjustments are made 
    outputs_Adjusted = [] 
    #Iterates through each exchange rate  
    for index, row in outputs.iterrows(): 
        #Reduces sig figs of GDP and appends a percent sign and the observation date       
        outputs_Adjusted.append(str( "{:.3g}".format(row["macro_Variable_Recent"])) + '% (' + row["macro_Variable_Date"] + ')')
    #Returns list of GDPs after cleaning 
    return (outputs_Adjusted) 

def inflation_Rate_Generator(inflation_Rate_Codes): 
    #Calls the macro_Variable_Collector function to collect inflation rate data 
    inflation_Rates = macro_Variable_Collector(inflation_Rate_Codes) 
    #New list which holds inflation rate data after adjustments are made 
    inflation_Rates_Adjusted = [] 
    #Iterates through each inflation rate  
    for index, row in inflation_Rates.iterrows(): 
        #Reduces sig figs of inflation and appends a percent sign and the observation date         
        inflation_Rates_Adjusted.append(str( "{:.4g}".format(row["macro_Variable_Recent"])) + '% (' + row["macro_Variable_Date"] + ')')
    #Returns list of inflation rates after cleaning 
    return (inflation_Rates_Adjusted) 

#Generates report given region codes 
def report_Generator(region_Codes): 
    #Lists which contain each macro variable codes, sources, and special behavior (if any) 
    exchange_Rate_Codes = [] 
    output_Codes = [] 
    inflation_Codes = [] 
    #Loops through each row in the region_Codes dataframe and appends the macro variable to the correct list 
    for economy, currency, exchange_Rate_Code, exchange_Rate_Source, exchange_Rate_Inversion, output_Code, output_Source, inflation_Code, inflation_Source in region_Codes: 
        exchange_Rate_Codes.append((exchange_Rate_Code, exchange_Rate_Source, exchange_Rate_Inversion)) 
        output_Codes.append((output_Code, output_Source, 'na')) 
        inflation_Codes.append((inflation_Code, inflation_Source, 'na')) 
    #Stores the results of the function calls that gather and clean each macro variable data passing the lists of codes as parameters 
    exchange_Rates = exchange_Rate_Generator(exchange_Rate_Codes) 
    outputs = output_Generator(output_Codes)
    inflation_Rates = inflation_Rate_Generator(inflation_Codes) 
    counter = 0 
    #Final dataframe to contain all observations
    euro_Atlantic_Data = panda.DataFrame(columns=['Economy', 'Currency', 'Exchange Rate to USD', 'Percent Change GDP YoY (Seasonally Adjusted)', 'Percent Change CPI YoY (Not Seasonally Adjusted)']) 
    #Combines the results of the above lists to make a dataframe 
    for economy, currency, exchange_Rate_Code, exchange_Rate_Source, exchange_Rate_Inversion, output_Code, output_Source, inflation_Code, inflation_Source in region_Codes: 
        new_Row = {'Economy': economy, 'Currency': currency, 'Exchange Rate to USD': exchange_Rates[counter], 'Percent Change GDP YoY (Seasonally Adjusted)': outputs[counter], 'Percent Change CPI YoY (Not Seasonally Adjusted)': inflation_Rates[counter]} 
        euro_Atlantic_Data = euro_Atlantic_Data.append(new_Row, ignore_index = True) 
        counter = counter + 1  
    #Returns the pandas dataframe with all findings 
    return euro_Atlantic_Data

#Stores results of the report function call with the euro_Atlantic_Codes parameter 
report = report_Generator(euro_Atlantic_Codes) 
#Collects todays date 
today = date.today().strftime('%m-%d-%Y') 
#Filepath and filename 
filename = '~/Downloads/Euro-Atlantic Report (' + today + ").csv" 
#Exports the pandas dataframe stored in the report variable to a .csv file in the downloads folder
report.to_csv(filename, index = False) 
#Returns the report findings to the console for quick access 
print(tabulate(report, headers = 'keys', tablefmt = 'plain')) 