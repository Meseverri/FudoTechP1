import Read_data_2 as RD
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import pandas as pd

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

#input una lista otput dataframe de distribuciones
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
        
        a=list(a)
        dist_data.append(len(a))
        
        count+=1
    
    dist=pd.DataFrame(dist_data,index=Index)
    return dist
n=datetime.now()
EURUSD_candels=RD.Candels("6EM22-CME.scid_BarData.txt")
POI_Day=pd.read_csv("EURUSD POI R2.csv",index_col=0)
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


T0=datetime(2021,2,28,18)
T1=T0+timedelta(days=1)
T2=T1+timedelta(days=1)
T3=T2+timedelta(days=1)
T4=T3+timedelta(days=1)
T5=T4+timedelta(days=1)

Monday_S0=T0
Monday_S1=Monday_S0+timedelta(hours=7)
Monday_S2=Monday_S1+timedelta(hours=4)
Monday_S3=Monday_S2+timedelta(hours=6)
Monday_S4=Monday_S3+timedelta(hours=7)

Tuesday_S0=T1
Tuesday_S1=Tuesday_S0+timedelta(hours=7)
Tuesday_S2=Tuesday_S1+timedelta(hours=4)
Tuesday_S3=Tuesday_S2+timedelta(hours=6)
Tuesday_S4=Tuesday_S3+timedelta(hours=7)

Wednesday_S0=T2
Wednesday_S1=Wednesday_S0+timedelta(hours=7)
Wednesday_S2=Wednesday_S1+timedelta(hours=4)
Wednesday_S3=Wednesday_S2+timedelta(hours=6)
Wednesday_S4=Wednesday_S3+timedelta(hours=7)

Thursday_S0=T3
Thursday_S1=Thursday_S0+timedelta(hours=7)
Thursday_S2=Thursday_S1+timedelta(hours=4)
Thursday_S3=Thursday_S2+timedelta(hours=6)
Thursday_S4=Thursday_S3+timedelta(hours=7)

Friday_S0=T4
Friday_S1=Friday_S0+timedelta(hours=7)
Friday_S2=Friday_S1+timedelta(hours=4)
Friday_S3=Friday_S2+timedelta(hours=6)
Friday_S4=Friday_S3+timedelta(hours=7)

EURUSD=EURUSD_candels.candels
EURUSD_VOL=EURUSD_candels.Volume
#getting the week to study
EURUSD_VOL_LOCAL=EURUSD_VOL[EURUSD_VOL["Date"]>=T0][EURUSD_VOL["Date"]<=T5]
EURUSD_VOL[" BidVolume $"]=EURUSD_VOL["Mean"]*EURUSD_VOL[" BidVolume"]
EURUSD_VOL[" AskVolume $"]=EURUSD_VOL["Mean"]*EURUSD_VOL[" AskVolume"]
POI=POI_Day[POI_Day["Date"]>=T0][POI_Day["Date"]<=T5]

POI["T Min"]=POI[["T High","T Low"]].min(axis=1)
POI["T Max"]=POI[["T High","T Low"]].max(axis=1)

Monday0=EURUSD_VOL[EURUSD_VOL["Date"]>=Monday_S0][EURUSD_VOL["Date"]<=Monday_S1]
Monday1=EURUSD_VOL[EURUSD_VOL["Date"]>=Monday_S1][EURUSD_VOL["Date"]<=Monday_S2]
Monday2=EURUSD_VOL[EURUSD_VOL["Date"]>=Monday_S2][EURUSD_VOL["Date"]<=Monday_S3]
Monday3=EURUSD_VOL[EURUSD_VOL["Date"]>=Monday_S3][EURUSD_VOL["Date"]<=Monday_S4]



Tuesday0=EURUSD_VOL[EURUSD_VOL["Date"]>=Tuesday_S0][EURUSD_VOL["Date"]<=Tuesday_S1]
Tuesday1=EURUSD_VOL[EURUSD_VOL["Date"]>=Tuesday_S1][EURUSD_VOL["Date"]<=Tuesday_S2]
Tuesday2=EURUSD_VOL[EURUSD_VOL["Date"]>=Tuesday_S2][EURUSD_VOL["Date"]<=Tuesday_S3]
Tuesday3=EURUSD_VOL[EURUSD_VOL["Date"]>=Tuesday_S3][EURUSD_VOL["Date"]<=Tuesday_S4]


Wednesday0=EURUSD_VOL[EURUSD_VOL["Date"]>=Wednesday_S0][EURUSD_VOL["Date"]<=Wednesday_S1]
Wednesday1=EURUSD_VOL[EURUSD_VOL["Date"]>=Wednesday_S1][EURUSD_VOL["Date"]<=Wednesday_S2]
Wednesday2=EURUSD_VOL[EURUSD_VOL["Date"]>=Wednesday_S2][EURUSD_VOL["Date"]<=Wednesday_S3]
wednesday3=EURUSD_VOL[EURUSD_VOL["Date"]>=Wednesday_S3][EURUSD_VOL["Date"]<=Wednesday_S4]

Thursday0=EURUSD_VOL[EURUSD_VOL["Date"]>=Thursday_S0][EURUSD_VOL["Date"]<=Thursday_S1]
Thursday1=EURUSD_VOL[EURUSD_VOL["Date"]>=Thursday_S1][EURUSD_VOL["Date"]<=Thursday_S2]
Thursday2=EURUSD_VOL[EURUSD_VOL["Date"]>=Thursday_S2][EURUSD_VOL["Date"]<=Thursday_S3]
Thursday3=EURUSD_VOL[EURUSD_VOL["Date"]>=Thursday_S3][EURUSD_VOL["Date"]<=Thursday_S4]

Friday0=EURUSD_VOL[EURUSD_VOL["Date"]>=Friday_S0][EURUSD_VOL["Date"]<=Friday_S1]
Friday1=EURUSD_VOL[EURUSD_VOL["Date"]>=Friday_S1][EURUSD_VOL["Date"]<=Friday_S2]
Friday2=EURUSD_VOL[EURUSD_VOL["Date"]>=Friday_S2][EURUSD_VOL["Date"]<=Friday_S3]
Friday3=EURUSD_VOL[EURUSD_VOL["Date"]>=Friday_S3][EURUSD_VOL["Date"]<=Friday_S4]


fig, axes = plt.subplots(nrows=2, ncols=4)
fig.suptitle(f"Price volume Monday-Tuesday ({str(T0)})")
Monday0["Mean"].hist(bins=100,ax=axes[0,0])
Monday1["Mean"].hist(bins=100,ax=axes[0,1])
Monday2["Mean"].hist(bins=100,ax=axes[0,2])
Monday3["Mean"].hist(bins=100,ax=axes[0,3])

Tuesday0["Mean"].hist(bins=100,ax=axes[1,0])
Tuesday1["Mean"].hist(bins=100,ax=axes[1,1])
Tuesday2["Mean"].hist(bins=100,ax=axes[1,2])
Tuesday3["Mean"].hist(bins=100,ax=axes[1,3])

fig, axes = plt.subplots(nrows=3, ncols=4)
fig.suptitle(f"Price volume Wednesday-Thursday-Friday ({str(T2)})")
Wednesday0["Mean"].hist(bins=100,ax=axes[0,0])
Wednesday1["Mean"].hist(bins=100,ax=axes[0,1])
Wednesday2["Mean"].hist(bins=100,ax=axes[0,2])
wednesday3["Mean"].hist(bins=100,ax=axes[0,3])

Thursday0["Mean"].hist(bins=100,ax=axes[1,0])
Thursday1["Mean"].hist(bins=100,ax=axes[1,1])
Thursday2["Mean"].hist(bins=100,ax=axes[1,2])
Thursday3["Mean"].hist(bins=100,ax=axes[1,3])

Friday0["Mean"].hist(bins=100,ax=axes[2,0])
Friday1["Mean"].hist(bins=100,ax=axes[2,1])
Friday2["Mean"].hist(bins=100,ax=axes[2,2])
Friday3["Mean"].hist(bins=100,ax=axes[2,3])

fig, axes = plt.subplots(nrows=2, ncols=4)
fig.suptitle(f"BidVolume Monday-Tuesday ({str(T0)})")
Monday0[" BidVolume $"].hist(bins=100,ax=axes[0,0])
Monday1[" BidVolume $"].hist(bins=100,ax=axes[0,1])
Monday2[" BidVolume $"].hist(bins=100,ax=axes[0,2])
Monday3[" BidVolume $"].hist(bins=100,ax=axes[0,3])

Tuesday0[" BidVolume $"].hist(bins=100,ax=axes[1,0])
Tuesday1[" BidVolume $"].hist(bins=100,ax=axes[1,1])
Tuesday2[" BidVolume $"].hist(bins=100,ax=axes[1,2])
Tuesday3[" BidVolume $"].hist(bins=100,ax=axes[1,3])

fig, axes = plt.subplots(nrows=3, ncols=4)
fig.suptitle(f"BidVolume Wednesday-Thursday-Friday ({str(T2)})")
Wednesday0[" BidVolume $"].hist(bins=100,ax=axes[0,0])
Wednesday1[" BidVolume $"].hist(bins=100,ax=axes[0,1])
Wednesday2[" BidVolume $"].hist(bins=100,ax=axes[0,2])
wednesday3[" BidVolume $"].hist(bins=100,ax=axes[0,3])

Thursday0[" BidVolume $"].hist(bins=100,ax=axes[1,0])
Thursday1[" BidVolume $"].hist(bins=100,ax=axes[1,1])
Thursday2[" BidVolume $"].hist(bins=100,ax=axes[1,2])
Thursday3[" BidVolume $"].hist(bins=100,ax=axes[1,3])

Friday0[" BidVolume $"].hist(bins=100,ax=axes[2,0])
Friday1[" BidVolume $"].hist(bins=100,ax=axes[2,1])
Friday2[" BidVolume $"].hist(bins=100,ax=axes[2,2])
Friday3[" BidVolume $"].hist(bins=100,ax=axes[2,3])

fig, axes = plt.subplots(nrows=2, ncols=4)
fig.suptitle(f"AskVolume Monday-Tuesday ({str(T0)})")
Monday0[" AskVolume $"].hist(bins=100,ax=axes[0,0])
Monday1[" AskVolume $"].hist(bins=100,ax=axes[0,1])
Monday2[" AskVolume $"].hist(bins=100,ax=axes[0,2])
Monday3[" AskVolume $"].hist(bins=100,ax=axes[0,3])

Tuesday0[" AskVolume $"].hist(bins=100,ax=axes[1,0])
Tuesday1[" AskVolume $"].hist(bins=100,ax=axes[1,1])
Tuesday2[" AskVolume $"].hist(bins=100,ax=axes[1,2])
Tuesday3[" AskVolume $"].hist(bins=100,ax=axes[1,3])

fig, axes = plt.subplots(nrows=3, ncols=4)
fig.suptitle(f"AskVolume Wednesday-Thursday-Friday ({str(T2)})")
Wednesday0[" AskVolume $"].hist(bins=100,ax=axes[0,0])
Wednesday1[" AskVolume $"].hist(bins=100,ax=axes[0,1])
Wednesday2[" AskVolume $"].hist(bins=100,ax=axes[0,2])
wednesday3[" AskVolume $"].hist(bins=100,ax=axes[0,3])

Thursday0[" AskVolume $"].hist(bins=100,ax=axes[1,0])
Thursday1[" AskVolume $"].hist(bins=100,ax=axes[1,1])
Thursday2[" AskVolume $"].hist(bins=100,ax=axes[1,2])
Thursday3[" AskVolume $"].hist(bins=100,ax=axes[1,3])

Friday0[" AskVolume $"].hist(bins=100,ax=axes[2,0])
Friday1[" AskVolume $"].hist(bins=100,ax=axes[2,1])
Friday2[" AskVolume $"].hist(bins=100,ax=axes[2,2])
Friday3[" AskVolume $"].hist(bins=100,ax=axes[2,3])

fig, axes = plt.subplots(nrows=2, ncols=1)
fig.suptitle(f"Mean Volume({str(T0)})")

EURUSD_VOL_LOCAL.plot(x="Date",y="Mean",ax=axes[0])
EURUSD_VOL_LOCAL[EURUSD_VOL_LOCAL["Delta"]>5].plot(x="Date",y="Delta",style="o",ax=axes[1])
EURUSD_VOL_LOCAL[EURUSD_VOL_LOCAL["Delta"]<-5].plot(x="Date",y="Delta",style="o",ax=axes[1])
plt.show()