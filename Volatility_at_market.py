from datetime import datetime
import MetaTrader5 as mt5
import statistics
import matplotlib.pyplot as plt
import pandas as pd
import pytz
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def distribution_df(data,parts=100):
    data=data.round(6)
    minimo=data.min()
    maximo=data.max()
    rango=maximo-minimo
    interval_size=rango/parts
    Index=[]
    dist_data=[]
    
    for k in range(parts+1):    
        Index.append(minimo+k*interval_size)

    print("minimo:",minimo)
    print("maximo:",maximo)
    print(f"{Index[0]},{Index[-1]}")
    for i in Index:  
        count=1
        #a=set(data[i<=data]).intersection(set(data[data<(i+count*interval_size)]))
        a=intersection(data[i<=data].tolist(),data[data<(i+count*interval_size)].tolist())
        print(a)
        a=list(a)
        dist_data.append(len(a))
        
        count+=1
    
    dist=pd.DataFrame(dist_data,index=Index)
    return dist


# display data on the MetaTrader 5 package

 
# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# set time zone to UTC
timezone = pytz.timezone("Etc/UTC")
# create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
utc_from = datetime(2020, 1, 10, tzinfo=timezone)
# get 10 EURUSD H4 bars starting from 01.10.2020 in UTC time zone
rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_H4, utc_from, 10)
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
# display each element of obtained data in a new line
print("Display obtained data 'as is'")
for rate in rates:
    print(rate)
 
# create DataFrame out of the obtained data
rates_frame = pd.DataFrame(rates)
# convert time in seconds into the datetime format
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
                           
# display data
print("\nDisplay dataframe with data")
print(rates_frame)  
# display each element of obtained data in a new line

 
# create DataFrame out of the obtained data
rates_frame = pd.DataFrame(rates)
# convert time in seconds into the datetime format
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
#aprox volume estimation mean between High and low times the ticks
rates_frame["H_L_mean"]=(rates_frame["high"]+rates_frame["low"])/2
rates_frame["Aprox volume"]=rates_frame["H_L_mean"]*rates_frame["tick_volume"]

# display data

print("\nDisplay dataframe with data")
print(rates_frame.describe())
#print(distribution_df(rates_frame["tick_volume"],parts=1000).max())
