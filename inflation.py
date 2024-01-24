import eurostat
import pandas as pd
from datetime import datetime

inflation_Rate_Source = 'prc_hicp_manr' 

#Find the data we want to select
pars = eurostat.get_pars(inflation_Rate_Source)
print(pars) 
par_Values = eurostat.get_par_values(inflation_Rate_Source, 'geo') 
print(par_Values) 


#Define a dataframe to store the query results 
inflation_Rates_Data = pd.DataFrame()
#Define the economies we want to pull inflation rate data for 
filters = {'geo': ['CZ', 'HU', 'PL', 'RO']} 
#Use Eurostat API to pull data 
inflation_Rates_Data = eurostat.get_data_df(inflation_Rate_Source, filter_pars=filters) 
print(inflation_Rates_Data)
#Removes some unnecessary columns 
inflation_Rates_Data = inflation_Rates_Data.drop(['freq', 'unit', 'coicop'], axis = 1)
#Get the most recent observartion and date  
latest_Observations = inflation_Rates_Data.iloc[:, -1] 
latest_Observation_Date = latest_Observations.name 
#Parse the original string into a datetime object
date_object = datetime.strptime(latest_Observation_Date, '%Y-%m')
#Format the datetime object into a new string with the American format
latest_Observation_Date = date_object.strftime('%m-%d-%Y')
#Append the observation date to the lates observation 
for index, value in latest_Observations.items(): 
    latest_Observations[index] = str("{:.4g}".format(latest_Observations[index]))+ ' (' + latest_Observation_Date + ')' 

print(latest_Observations) 