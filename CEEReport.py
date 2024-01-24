import eurostat
import pandas as pd
from datetime import datetime 

#Codes for the Central Europe Report with source and unique behavior stored in a 2D List  
#Format: (Economy, Currency, Currecny Code, Currency Source, Inversion to Euros, GDP Code, GDP Source, Inflation Code, Inflation Source)
central_Europe_Codes = [('Czech Republic', 'koruna', 'CZK', 'eurostat', 'invserion', 'na', 'na', 'CZ', 'eurostat'), 
                       ('Hungary', 'forint', 'HUF', 'eurostat', 'inversion', 'na', 'na', 'HU', 'eurostat'), 
                       ('Poland', 'zloty', 'PLN', 'eurostat', 'inversion', 'na', 'na', 'PL', 'eurostat'), 
                       ('Romania', 'leu', 'RON', 'eurostat', 'inversion', 'na', 'na', 'RO', 'eurostat')]

#Defines the data sources
exchange_Rate_Source = 'ert_bil_eur_d' 
output_Source = 'namq_10_gdp' 
inflation_Rate_Source = 'prc_hicp_manr' 

#Find the data we want to select
pars = eurostat.get_pars(exchange_Rate_Source)
#print(pars) 
par_Values = eurostat.get_par_values(exchange_Rate_Source, 'currency') 
#print(par_Values) 

#Define a dataframe to store the query results 
exchange_Rates_Data = pd.DataFrame()
#Define the currencies we want to pull exchange rate data for 
filters = {'currency': ['CZK', 'HUF', 'PLN', 'RON']} 
#Use Eurostat API to pull data 
exchange_Rates_Data = eurostat.get_data_df(exchange_Rate_Source, filter_pars=filters) 
#Removes some unnecessary columns 
exchange_Rates_Data = exchange_Rates_Data.drop(['freq', 'statinfo', 'unit'], axis = 1)
#Get the most recent observartion and date  
latest_Observations = exchange_Rates_Data.iloc[:, -1] 
latest_Observation_Date = latest_Observations.name 
#Parse the original string into a datetime object
date_object = datetime.strptime(latest_Observation_Date, '%Y-%m-%d')
#Format the datetime object into a new string with the American format
latest_Observation_Date = date_object.strftime('%m-%d-%Y')
#Append the observation date to the lates observation 
for index, value in latest_Observations.items(): 
    latest_Observations[index] = 1/latest_Observations[index] 
    latest_Observations[index] = str("{:.4g}".format(latest_Observations[index]))+ ' (' + latest_Observation_Date + ')' 



#Define a dataframe to store the query results 
inflation_Rates_Data = pd.DataFrame()
#Define the economies we want to pull exchange rate data for 
filters = {'geo': ['CZ', 'HU', 'PL', 'RO']} 
#Use Eurostat API to pull data 
inflation_Rates_Data = eurostat.get_data_df(inflation_Rate_Source, filter_pars=filters) 
print(inflation_Rates_Data)
#Removes some unnecessary columns 
inflation_Rates_Data = inflation_Rates_Data.drop(['freq', 'unit', 'coicop'], axis = 1)
#Get the most recent observartion and date  
latest_Observations2 = inflation_Rates_Data.iloc[:, -1] 
latest_Observation_Date2 = latest_Observations2.name 
#Parse the original string into a datetime object
date_object2 = datetime.strptime(latest_Observation_Date2, '%Y-%m')
#Format the datetime object into a new string with the American format
latest_Observation_Date2 = date_object2.strftime('%m-%d-%Y')
#Append the observation date to the lates observation 
for index, value in latest_Observations2.items(): 
    latest_Observations2[index] = str("{:.3g}".format(latest_Observations2[index]))+ '% (' + latest_Observation_Date2 + ')' 



#Defines the pandas dataframe that holds all of our data 
central_Europe_Data = pd.DataFrame(columns=['Economy', 'Currency', 'Exchange Rate to Euros', 'Percent Change GDP YoY (Seasonally Adjusted)', 'Percent Change CPI YoY (HICP)']) 

counter = 0 
#Combines the results of the above lists to make a dataframe 
for economy, currency, exchange_Rate_Code, exchange_Rate_Source, exchange_Rate_Inversion, output_Code, output_Source, inflation_Code, inflation_Source in central_Europe_Codes: 
    new_Row = {'Economy': economy, 'Currency': currency, 'Exchange Rate to Euros': latest_Observations[counter], 'Percent Change GDP YoY (Seasonally Adjusted)': 'Coming Soon!', 'Percent Change CPI YoY (Not Seasonally Adjusted)': latest_Observations2[counter]} 
    central_Europe_Data = central_Europe_Data.append(new_Row, ignore_index = True) 
    counter = counter + 1 

#Collects todays date 
today = datetime.today().strftime('%m-%d-%Y') 
#Filepath and filenames 
central_Europe_Filename = '~/Downloads/Central-Europe Report (' + today + ").csv" 
#Exports the pandas dataframes stored in the report variables to a .csv file in the downloads folder
central_Europe_Data.to_csv(central_Europe_Filename, index = False)
print(central_Europe_Data) 


