import Read_data_2 as RD
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import pandas as pd

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    #for value in list1:

    return lst3

#input una lista otput dataframe de distribuciones
#data: Pandas dataframe
# x_ax: the column witch contains the main random variable
# frequency=True: True if you only need to count the number of times, False if volume is need 
# y_ax=None, 
# bins=100
def distribution_df(data,x_ax,frequency=True,y_ax=None, bins=100):
    data=data.round(6)
    minimo=data[x_ax].min()
    maximo=data[x_ax].max()
    rango=maximo-minimo
    interval_size=rango/bins
    Ranges=[]
    #Index_DF lista con el punto medio del intervalo de frequencia
    #Index_DF=[]
    dist_data=[]
    
    for k in range(bins+1):    
        Ranges.append(round(minimo+k*interval_size,7))
        #Index_DF.append(round(minimo+(2*k+1)*interval_size/2,7))
    count=1
    for i in Ranges:  
        #a=set(data[i<=data]).intersection(set(data[data<(i+count*interval_size)]))
        if count==bins:
            # a=intersection(data[i<=data[x_ax]][x_ax].tolist(),data[data[x_ax]<=(i+interval_size)][x_ax].tolist())
            a=data[i<=data[x_ax]][data[x_ax]<=(i+interval_size)]
        else:
            # a=intersection(data[i<=data[x_ax]][x_ax].tolist(),data[data[x_ax]<(i+interval_size)].tolist())
            a=data[i<=data[x_ax]][data[x_ax]<(i+interval_size)]
        # a=list(a)

        if frequency==True:
            dist_data.append(len(a))
            count+=1
        elif frequency!=True:
            dist_data.append(a[y_ax].sum())
            count+=1
    

    dist=pd.DataFrame({"Index":Ranges,f"Frequencia {y_ax}":dist_data})
    dist[f"Frequencia {y_ax} relativa"]=dist[f"Frequencia {y_ax}"]/np.sum(dist_data)
    dist["Interval Size"]=interval_size
    dist["Vr*P"]=dist[f"Frequencia {y_ax} relativa"]*dist["Index"]
    dist["Vr*P^2"]=dist[f"Frequencia {y_ax} relativa"]*dist["Index"]**2

    return dist

def frequency_inside(inf,sup,dist_df):
    
    df=dist_df[dist_df["Index"]>inf][dist_df["Index"]<sup]
    Fr=df.iloc[:,2]
    return Fr.sum() 

def stats_setion_Series(dist_df):
    Mean=dist_df["Vr*P"].sum()
    Var=dist_df["Vr*P^2"].sum()-Mean**2
    Std=Var**(1/2)
    stats={"Media":Mean,
            "Std":Std}
    return pd.Series(stats)

EURUSD_candels=RD.Candels("6EM22-CME.scid_BarData.txt")
POI_Day=pd.read_csv("EURUSD POI DAY.csv",index_col=0)
POI_Day["P High"]=POI_Day["P High"].astype(float)
POI_Day["P Low"]=POI_Day["P Low"].astype(float)
POI_Day["H sweep"]=POI_Day["H sweep"].astype(bool)
POI_Day["L sweep"]=POI_Day["L sweep"].astype(bool)
POI_Day["Contenido"]=POI_Day["Contenido"].astype(bool)
POI_Day["variacion PH-PL"]=POI_Day["variacion PH-PL"].astype(float)
# POI_Day["Open to POI"]=POI_Day["Open to POI"].astype(float)
# POI_Day["POI to Close"]=POI_Day["POI to Close"].astype(float)
POI_Day["Date"]=pd.to_datetime(POI_Day["Date"])
POI_Day["T High"]=pd.to_datetime(POI_Day["T High"])
POI_Day["T Low"]=pd.to_datetime(POI_Day["T Low"])

EURUSD=EURUSD_candels.candels
EURUSD_VOL=EURUSD_candels.Volume

#separating the day of study from the data
T0=datetime(2020,3,8,18)
T1=T0+timedelta(days=1)
POI_MONDAY=POI_Day[POI_Day["Date"]>=T0][POI_Day["Date"]<=T1]
EURUSD_MONDAY=EURUSD[EURUSD["Date"]>=T0][EURUSD["Date"]<=T1]
EURUSD_VOL_MONDAY=EURUSD_VOL[EURUSD_VOL["Date"]>=T0][EURUSD["Date"]<=T1]
#Acumulacion del volumen por cada precio
EURUSD_VOL_MONDAY[" Volumen Acumulado"]=EURUSD_VOL_MONDAY[" Volume"].cumsum()

#Calculating the volume weighted distribution
Price_dist_MONDAY=distribution_df(EURUSD_VOL_MONDAY,x_ax="Mean",frequency=False,y_ax=" Volume",bins=300)
Price_dist_MONDAY_Bid=distribution_df(EURUSD_VOL_MONDAY,x_ax="Mean",frequency=False,y_ax=" BidVolume",bins=300)
Price_dist_MONDAY_Ask=distribution_df(EURUSD_VOL_MONDAY,x_ax="Mean",frequency=False,y_ax=" AskVolume",bins=300)

Volume_stats_monday=stats_setion_Series(Price_dist_MONDAY)
bid_stats_monday=stats_setion_Series(Price_dist_MONDAY_Bid)
ask_stats_monday=stats_setion_Series(Price_dist_MONDAY_Ask)

#calculemos la frecuencia de datos que estan +- 1std
fr_vol=frequency_inside(Volume_stats_monday["Media"]-Volume_stats_monday["Std"],Volume_stats_monday["Media"]+Volume_stats_monday["Std"],Price_dist_MONDAY)
fr_bid=frequency_inside(bid_stats_monday["Media"]-bid_stats_monday["Std"],bid_stats_monday["Media"]+bid_stats_monday["Std"],Price_dist_MONDAY_Bid)
fr_ask=frequency_inside(ask_stats_monday["Media"]-ask_stats_monday["Std"],ask_stats_monday["Media"]+ask_stats_monday["Std"],Price_dist_MONDAY_Ask)


#calculemos la k tomando  std y mean estaticas
#trabajamos con la tabla de volumen y creamos una nueva columna con la diferencia
P_mean=Volume_stats_monday["Media"]
P_std=Volume_stats_monday["Std"]
EURUSD_VOL_MONDAY["K"]=(EURUSD_VOL_MONDAY["Mean"]-P_mean)/P_std

#calculemos la k dinamica
# trabajamos con la tabla de volumen
"""1) creamos la una columna que multiplique el precio por el volumen
   2) creamos una nueva columna que sume los precios por volumen
   3) creamos la columna de la media como la columna de la suma acumulada de los precios por volumen
   dividido entre el volumen acumulado
   4) creamos la una columna que multiplique el precio**2 por el volumen
   5) creamos una nueva columna que sume los precios**2 por volumen
   6) creamos la columna de la media orden 2 como la columna de la suma acumulada de los precios**2 por volumen
   dividido entre el volumen acumulado
   7) Creamos la columna de la desviacion tipica haciendo la diferencia de la media orden 2 menos 
   la media**2
   8) creamos la columna de la k haciendo la diferencia entre el precio menos la media dividido entre la desviacion.
"""







print(f"Day of setion:\n{T0}\n")
print(f"POI study dataframe:\n{POI_MONDAY.to_string()}\n")
print(f"Price dataframe head:\n{EURUSD_MONDAY.head(10).to_string()}\n")
print(f"Volume dataframe head:\n{EURUSD_VOL_MONDAY.head(10).to_string()}\n")

print(15*"-","Stats",15*"-","\n")
print(f"Price volume weighted distribution\n:{Price_dist_MONDAY.to_string()}\n")
print(f"Price volume weighted mean std:\n{Volume_stats_monday}\n")
print(f"Frequency volume of Value zone:\n{fr_vol*100}%\n")
print(f"Price bid weighted mean std:\n{bid_stats_monday}\n")
print(f"Frequency bid volume of Value zone:\n{fr_bid*100}%\n")
print(f"Price ask weighted mean std:\n{ask_stats_monday}\n")
print(f"Frequency ask volume of Value zone:\n{fr_ask*100}%\n")

EURUSD_VOL_MONDAY.plot(x="Date",y="K")
plt.show()
