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
    dist["V*P"]=dist[f"Frequencia {y_ax} relativa"]*dist["Index"]
    dist["V*P^2"]=dist[f"Frequencia {y_ax} relativa"]*dist["Index"]**2

    return dist

def frequency_inside(inf,sup,dist_df):
    
    df=dist_df[dist_df["Index"]>inf][dist_df["Index"]<sup]
    Fr=df.iloc[:,2]
    return Fr.sum() 



n=datetime.now()
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
#getting the week to study
T0=datetime(2020,3,1,18)
T1=T0+timedelta(days=1)
T2=T1+timedelta(days=1)
T3=T2+timedelta(days=1)
T4=T3+timedelta(days=1)
T5=T4+timedelta(days=1)

POI_Day["T Min"]=POI_Day[["T High","T Low"]].min(axis=1)
POI_Day["T Max"]=POI_Day[["T High","T Low"]].max(axis=1)
POI_MONDAY=POI_Day[POI_Day["Date"]>=T0][POI_Day["Date"]<=T1]
POI_TUESDAY=POI_Day[POI_Day["Date"]>=T1][POI_Day["Date"]<=T2]

EURUSD_LOCAL_MONDAY=EURUSD[EURUSD["Date"]>=T0][EURUSD["Date"]<=T1]
EURUSD_LOCAL_TUESDAY=EURUSD[EURUSD["Date"]>=T1][EURUSD["Date"]<=T2]
EURUSD_LOCAL_WEDNESDAY=EURUSD[EURUSD["Date"]>=T2][EURUSD["Date"]<=T3]
EURUSD_LOCAL_THURSDAY=EURUSD[EURUSD["Date"]>=T3][EURUSD["Date"]<=T4]

EURUSD_VOL[" BidVolume $"]=EURUSD_VOL["Mean"]*EURUSD_VOL[" BidVolume"]
EURUSD_VOL[" AskVolume $"]=EURUSD_VOL["Mean"]*EURUSD_VOL[" AskVolume"]
EURUSD_VOL_LOCAL=EURUSD_VOL[EURUSD_VOL["Date"]>=T0][EURUSD_VOL["Date"]<=T1]

EURUSD_VOL_MONDAY=EURUSD_VOL[EURUSD_VOL["Date"]>=T0][EURUSD["Date"]<=T1]
EURUSD_VOL_MONDAY[" Volumen Acumulado"]=EURUSD_VOL_MONDAY[" Volume"].cumsum()
EURUSD_VOL_MONDAY[" Volumen Relativo"]=EURUSD_VOL_MONDAY[" Volume"]/EURUSD_VOL_MONDAY[" Volumen Acumulado"]


EURUSD_VOL_TUESDAY=EURUSD_VOL[EURUSD_VOL["Date"]>=T1][EURUSD["Date"]<=T2]
EURUSD_VOL_WEDNESDAY=EURUSD_VOL[EURUSD_VOL["Date"]>=T2][EURUSD["Date"]<=T3]

Price_dist_MONDAY=distribution_df(EURUSD_VOL_MONDAY,x_ax="Mean",frequency=False,y_ax=" Volume",bins=100)
Price_dist_MONDAY_Bid=distribution_df(EURUSD_VOL_MONDAY,x_ax="Mean",frequency=False,y_ax=" BidVolume",bins=100)
Price_dist_MONDAY_Ask=distribution_df(EURUSD_VOL_MONDAY,x_ax="Mean",frequency=False,y_ax=" AskVolume",bins=100)

Price_dist_TUESDAY=distribution_df(EURUSD_VOL_TUESDAY,x_ax="Mean",frequency=False,y_ax=" Volume",bins=100)
Price_dist_WEDNESDAY=distribution_df(EURUSD_VOL_WEDNESDAY,x_ax="Mean",frequency=False,y_ax=" Volume",bins=100)
# Price_dist_THURSDAY=distribution_df(EURUSD_LOCAL_THURSDAY,x_ax="Mean",frequency=False,y_ax=" Volume",bins=100)
k=datetime.now()
print("time of distributuions:\n",k-n)


MONDAY_HIGH_FREQUENCIES=Price_dist_MONDAY[Price_dist_MONDAY["Frequencia  Volume relativa"]>Price_dist_MONDAY["Frequencia  Volume relativa"].mean()]
MONDAY_HIGH_FREQUENCIES["step"]=MONDAY_HIGH_FREQUENCIES["Index"].shift(-1)-MONDAY_HIGH_FREQUENCIES["Index"]

frequencia_lunes_media=Price_dist_MONDAY["Frequencia  Volume relativa"].mean()
frequencia_martes_media=Price_dist_TUESDAY["Frequencia  Volume relativa"].mean()
frequencia_miercoles_media=Price_dist_WEDNESDAY["Frequencia  Volume relativa"].mean()

frequencia_lunes_Bids_media=Price_dist_MONDAY_Bid["Frequencia  BidVolume relativa"].mean()
frequencia_lunes_Ask_media=Price_dist_MONDAY_Ask["Frequencia  AskVolume relativa"].mean()


print(MONDAY_HIGH_FREQUENCIES.to_string())
print("total high frequencies:\n",MONDAY_HIGH_FREQUENCIES["Frequencia  Volume relativa"].sum())
print("total:\n",Price_dist_MONDAY["Frequencia  Volume relativa"].sum())

volume_profile=EURUSD_VOL_LOCAL[EURUSD_VOL_LOCAL["Mean"]>=1.204079][EURUSD_VOL_LOCAL["Mean"]<1.205840]
print(EURUSD_VOL_MONDAY.head().to_string())

fig, axes = plt.subplots(nrows=2, ncols=2)
fig.suptitle(f"Monday({str(T1)})")
# plt.bar([" AskVolume $"," BidVolume $"],[volume_profile[" AskVolume $"].sum(),volume_profile[" BidVolume $"].sum()])
Price_dist_MONDAY.plot.barh(x="Index",y="Frequencia  Volume relativa",ax=axes[0,0])
axes[0,0].axvline(x=frequencia_lunes_media, color='r', linestyle='-')
axes[0,1].axhline(y=Price_dist_MONDAY["V*P"].sum(), color='r', linestyle='-')

plt.sca(axes[0,0])
plt.yticks(np.arange(EURUSD_LOCAL_MONDAY["Mean"].min(),EURUSD_LOCAL_MONDAY["Mean"].max(),(EURUSD_LOCAL_MONDAY["Mean"].max()-EURUSD_LOCAL_MONDAY["Mean"].min())/2),
            np.arange(EURUSD_LOCAL_MONDAY["Mean"].min(),EURUSD_LOCAL_MONDAY["Mean"].max(),(EURUSD_LOCAL_MONDAY["Mean"].max()-EURUSD_LOCAL_MONDAY["Mean"].min())/2))

EURUSD_LOCAL_MONDAY.plot(y="Mean",ax=axes[0,1])
axes[0,1].axhline(y=Price_dist_MONDAY["V*P"].sum(), color='r', linestyle='-')
Price_dist_MONDAY_Bid.plot.barh(x="Index",y="Frequencia  BidVolume relativa",ax=axes[1,0])
axes[1,0].axvline(x=frequencia_lunes_Bids_media, color='r', linestyle='-')
Price_dist_MONDAY_Ask.plot.barh(x="Index",y="Frequencia  AskVolume relativa",ax=axes[1,1])
axes[1,1].axvline(x=frequencia_lunes_Ask_media, color='r', linestyle='-')

# fig, axes = plt.subplots(nrows=2, ncols=2)
# fig.suptitle(f"Tuesday({str(T2)})")
# Price_dist_TUESDAY.plot.bar(x="Index",y="Frequencia relativa",ax=axes[0,0])
# plt.axhline(y=frequencia_martes_media, color='r', linestyle='-')
# EURUSD_LOCAL_TUESDAY.plot(y="Mean",ax=axes[0,1])

# fig, axes = plt.subplots(nrows=2, ncols=2)
# fig.suptitle(f"Wednesday({str(T3)})")
# Price_dist_WEDNESDAY.plot.bar(x="Index",y="Frequencia relativa",ax=axes[0,0])
# plt.axhline(y=frequencia_miercoles_media, color='r', linestyle='-')
# EURUSD_LOCAL_WEDNESDAY.plot(y="Mean",ax=axes[0,1])

"""Price_dist_MONDAY[Price_dist_MONDAY>Price_dist_MONDAY.mean()].plot.bar()
Price_dist_TUESDAY[Price_dist_TUESDAY>Price_dist_TUESDAY.mean()].plot.bar()
Price_dist_WEDNESDAY[Price_dist_WEDNESDAY>Price_dist_WEDNESDAY.mean()].plot.bar()
Price_dist_THURSDAY[Price_dist_THURSDAY>Price_dist_THURSDAY.mean()].plot.bar()
"""
plt.show()


