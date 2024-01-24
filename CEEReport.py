import eurostat
import pandas as pd
from datetime import datetime 

#Codes for the Central Europe Report with source and unique behavior stored in a 2D List (Created for future integration with ReportGenerator)
#Format: (Economy, Currency, Currecny Code, Currency Source, Inversion to Euros, GDP Code, GDP Source, Inflation Code, Inflation Source)
central_Europe_Codes = [('Czech Republic', 'koruna', 'CZK', 'eurostat', 'invserion', 'CZ', 'eurostat', 'CZ', 'eurostat'), 
                       ('Hungary', 'forint', 'HUF', 'eurostat', 'inversion', 'HU', 'HU', 'eurostat', 'eurostat'), 
                       ('Poland', 'zloty', 'PLN', 'eurostat', 'inversion', 'PL', 'eurostat', 'PL', 'eurostat'), 
                       ('Romania', 'leu', 'RON', 'eurostat', 'inversion', 'RO', 'eurostat', 'RO', 'eurostat')]

#Defines the data sources
exchange_Rate_Source = 'ert_bil_eur_d' 
output_Source = 'namq_10_gdp' 
inflation_Rate_Source = 'prc_hicp_manr' 

#Defines source filters 
exchange_Rate_Filters = {'currency': ['CZK', 'HUF', 'PLN', 'RON']} 
output_Filters = {'unit': ['CLV_PCH_SM'], 's_adj': ['SCA'], 'na_item': ['B1GQ'], 'geo': ['CZ', 'HU', 'PL', 'RO']}
inflation_Rate_Filters = {'freq': ['M'], 'unit': ['RCH_A'], 'coicop': ['CP00'], 'geo': ['CZ', 'HU', 'PL', 'RO']} 

#Function that uses Eurostat API to pull data and filter for latest observation
def macro_Variable_Collector(source, filters): 
    macro_Variable_Data = pd.DataFrame()
    macro_Variable_Data = eurostat.get_data_df(source, filter_pars = filters) 
    latest_Data = macro_Variable_Data.iloc[:, -1] 
    return(latest_Data) 

#Function that does post processing (like currency inversion) and appends the date to the observation
def process_Append_Date(source, latest_Data): 
    #Collects the observation data and stores it as a variable
    latest_Data_Date = latest_Data.name 
    #Exchange Rates Processing
    if(source == 'ert_bil_eur_d'): 
        #Parse the original string into a datetime object
        date_Object = datetime.strptime(latest_Data_Date, '%Y-%m-%d')
        #Format the datetime object into a new string with the American format
        latest_Data_Date = date_Object.strftime('%m-%d-%Y')
        #Append the observation date to the lates observation 
        for index, value in latest_Data.items(): 
            latest_Data[index] = 1/latest_Data[index] 
            latest_Data[index] = str("{:.3g}".format(latest_Data[index]))+ ' (' + latest_Data_Date + ')' 
    #Output Processing 
    elif(source == 'namq_10_gdp'):
        #Append the observation date to the lates observation 
        for index, value in latest_Data.items(): 
            latest_Data[index] = str("{:.3g}".format(latest_Data[index]))+ '% (' + latest_Data_Date + ')' 
    #Inflation Processing 
    elif(source == 'prc_hicp_manr'):
        date_Object = datetime.strptime(latest_Data_Date, '%Y-%m')
        #Format the datetime object into a new string with the American format
        latest_Data_Date = date_Object.strftime('%m-%d-%Y')
        #Append the observation date to the lates observation 
        for index, value in latest_Data.items(): 
            latest_Data[index] = str("{:.3g}".format(latest_Data[index]))+ '% (' + latest_Data_Date + ')' 
    #Error Handling 
    else: 
        print('Invalid Source') 
    #Returns the processed series 
    return(latest_Data)

#Defines the pandas dataframe that holds all of our data 
central_Europe_Data = pd.DataFrame(columns=['Economy', 'Currency', 'Exchange Rate to Euros', 'Percent Change GDP YoY (Seasonally Adjusted)', 'Percent Change CPI YoY (HICP)']) 

#Function calls
exchange_Rate_Data = macro_Variable_Collector(exchange_Rate_Source, exchange_Rate_Filters) 
exchange_Rate_Data = process_Append_Date(exchange_Rate_Source, exchange_Rate_Data) 

inflation_Rate_Data = macro_Variable_Collector(inflation_Rate_Source, inflation_Rate_Filters) 
inflation_Rate_Data = process_Append_Date(inflation_Rate_Source, inflation_Rate_Data) 

output_Data = macro_Variable_Collector(output_Source, output_Filters) 
output_Data = process_Append_Date(output_Source, output_Data) 

#Combines the results of the above lists to populate the central_Europe_Data dataframe 
counter = 0   
for economy, currency, exchange_Rate_Code, exchange_Rate_Source, exchange_Rate_Inversion, output_Code, output_Source, inflation_Code, inflation_Source in central_Europe_Codes: 
    new_Row = {'Economy': economy, 'Currency': currency, 'Exchange Rate to Euros': exchange_Rate_Data[counter], 'Percent Change GDP YoY (Seasonally Adjusted)': inflation_Rate_Data[counter], 'Percent Change CPI YoY (HICP)': output_Data[counter]} 
    central_Europe_Data = central_Europe_Data.append(new_Row, ignore_index = True) 
    counter = counter + 1 

#Collects todays date 
today = datetime.today().strftime('%m-%d-%Y') 
#Filepath and filenames 
central_Europe_Filename = '~/Downloads/Central-Europe Report (' + today + ").csv" 
#Exports the pandas dataframes stored in the report variables to a .csv file in the downloads folder
central_Europe_Data.to_csv(central_Europe_Filename, index = False) 
#Returns the result to the console for quick access 
print(central_Europe_Data) 


