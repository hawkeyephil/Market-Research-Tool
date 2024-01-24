import eurostat
import pandas as pd
from datetime import datetime

output_Source = 'namq_10_gdp' 

#Find the data we want to select
pars = eurostat.get_pars(output_Source)
print(pars) 
par_Values = eurostat.get_par_values(output_Source, 'geo') 
print(par_Values) 

#Define a dataframe to store the query results 
output_Data = pd.DataFrame()
#Define the economies we want to pull GDP data for 
#Chained linked volumes (percentage change from same period previous year)/seasonally and calendar adjusted/Gross domestic product at market prices/economies
filters = {'unit': ['CLV_PCH_SM'], 's_adj': ['SCA'], 'na_item': ['B1GQ'], 'geo': ['CZ', 'HU', 'PL', 'RO']} 
#Use Eurostat API to pull data 
output_Data = eurostat.get_data_df(output_Source, filter_pars=filters) 
#Removes some unnecessary columns 
output_Data = output_Data.drop(['freq', 'unit', 's_adj', 'na_item'], axis = 1)
#Get the most recent observartion and date  
latest_Observations = output_Data.iloc[:, -1] 
latest_Observation_Date = latest_Observations.name 
#Parse the original string into a datetime object
#date_object = datetime.strptime(latest_Observation_Date, '%Y-%m')
#Format the datetime object into a new string with the American format
#latest_Observation_Date = date_object.strftime('%m-%d-%Y')
#Append the observation date to the lates observation 
for index, value in latest_Observations.items(): 
    latest_Observations[index] = str("{:.4g}".format(latest_Observations[index]))+ '% (' + latest_Observation_Date + ')' 

print(latest_Observations) 
