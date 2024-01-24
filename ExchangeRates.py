import eurostat
import pandas as pd
from datetime import datetime

exchange_Rate_Source = 'ert_bil_eur_d' 

#Find the data we want to select
pars = eurostat.get_pars(exchange_Rate_Source)
print(pars) 
par_Values = eurostat.get_par_values(exchange_Rate_Source, 'currency') 
print(par_Values)

#Define a dataframe to store the exchange rate data results 
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
    latest_Observations[index] = str("{:.3g}".format(latest_Observations[index]))+ ' (' + latest_Observation_Date + ')' 

print(latest_Observations) 