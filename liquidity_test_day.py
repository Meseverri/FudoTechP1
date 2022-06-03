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
        print(a)
        a=list(a)
        dist_data.append(len(a))
        
        count+=1
    
    dist=pd.DataFrame(dist_data,index=Index)
    return dist


n=datetime.now()
EURUSD_candels=RD.Candels("6EM22-CME.scid_BarData.txt")
POI_Day=pd.read_csv("EURUSD POI Day.csv",index_col=0)
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


T0=datetime(2020,10,4,18)
T1=T0+timedelta(days=1)
T2=T1+timedelta(days=1)
T3=T2+timedelta(days=1)
T4=T3+timedelta(days=1)
T5=T4+timedelta(days=1)

EURUSD=EURUSD_candels.candels
EURUSD_VOL=EURUSD_candels.Volume
EURUSD_VOL_LOCAL=EURUSD_VOL[EURUSD_VOL["Date"]>=T0][EURUSD_VOL["Date"]<=T5]
POI=POI_Day[POI_Day["Date"]>=T0][POI_Day["Date"]<=T5]
POI["T Max"]=POI[["T High","T Low"]].max(axis=1)
POI["T Min"]=POI[["T High","T Low"]].min(axis=1)
print(EURUSD_VOL[EURUSD_VOL["Date"]>=T0][EURUSD_VOL["Date"]<=T5].columns)
print(POI[["T High","T Low","T Max","T Min"]].to_string())

Monday0=EURUSD_VOL[EURUSD_VOL["Date"]>=T0][EURUSD_VOL["Date"]<=POI["T Min"].iloc[0]]
Monday1=EURUSD_VOL[EURUSD_VOL["Date"]>=POI["T Min"].iloc[0]][EURUSD_VOL["Date"]<=POI["T Max"].iloc[0]]
Monday2=EURUSD_VOL[EURUSD_VOL["Date"]>=POI["T Max"].iloc[0]][EURUSD_VOL["Date"]<=T1]

Tuesday0=EURUSD_VOL[EURUSD_VOL["Date"]>=T1][EURUSD_VOL["Date"]<=POI["T Min"].iloc[1]]
Tuesday1=EURUSD_VOL[EURUSD_VOL["Date"]>=POI["T Min"].iloc[1]][EURUSD_VOL["Date"]<=POI["T Max"].iloc[1]]
Tuesday2=EURUSD_VOL[EURUSD_VOL["Date"]>=POI["T Max"].iloc[1]][EURUSD_VOL["Date"]<=T2]

Wednesday0=EURUSD_VOL[EURUSD_VOL["Date"]>=T2][EURUSD_VOL["Date"]<=POI["T Min"].iloc[2]]
Wednesday1=EURUSD_VOL[EURUSD_VOL["Date"]>=POI["T Min"].iloc[2]][EURUSD_VOL["Date"]<=POI["T Max"].iloc[2]]
Wednesday2=EURUSD_VOL[EURUSD_VOL["Date"]>=POI["T Max"].iloc[2]][EURUSD_VOL["Date"]<=T3]

Thursday0=EURUSD_VOL[EURUSD_VOL["Date"]>=T3][EURUSD_VOL["Date"]<=POI["T Min"].iloc[3]]
Thursday1=EURUSD_VOL[EURUSD_VOL["Date"]>=POI["T Min"].iloc[3]][EURUSD_VOL["Date"]<=POI["T Max"].iloc[3]]
Thursday2=EURUSD_VOL[EURUSD_VOL["Date"]>=POI["T Max"].iloc[3]][EURUSD_VOL["Date"]<=T4]

Friday0=EURUSD_VOL[EURUSD_VOL["Date"]>=T4][EURUSD_VOL["Date"]<=POI["T Min"].iloc[4]]
Friday1=EURUSD_VOL[EURUSD_VOL["Date"]>=POI["T Min"].iloc[4]][EURUSD_VOL["Date"]<=POI["T Max"].iloc[4]]
Friday2=EURUSD_VOL[EURUSD_VOL["Date"]>=POI["T Max"].iloc[4]][EURUSD_VOL["Date"]<=T5]






fig, axes = plt.subplots(nrows=5, ncols=3)
print(T0)
print(T1)
print(T2)
print(T3)
print(T4)

Monday0["Mean"].hist(bins=50,ax=axes[0,0])
Monday1["Mean"].hist(bins=50,ax=axes[0,1])
Monday2["Mean"].hist(bins=50,ax=axes[0,2])

Tuesday0["Mean"].hist(bins=50,ax=axes[1,0])
Tuesday1["Mean"].hist(bins=50,ax=axes[1,1])
Tuesday2["Mean"].hist(bins=50,ax=axes[1,2])

Wednesday0["Mean"].hist(bins=50,ax=axes[2,0])
Wednesday1["Mean"].hist(bins=50,ax=axes[2,1])
Wednesday2["Mean"].hist(bins=50,ax=axes[2,2])

Thursday0["Mean"].hist(bins=50,ax=axes[3,0])
Thursday1["Mean"].hist(bins=50,ax=axes[3,1])
Thursday2["Mean"].hist(bins=50,ax=axes[3,2])

Friday0["Mean"].hist(bins=50,ax=axes[4,0])
Friday1["Mean"].hist(bins=50,ax=axes[4,1])
Friday2["Mean"].hist(bins=50,ax=axes[4,2])

EURUSD_VOL_LOCAL.plot(x="Date",y="Mean")

# fig, axes = plt.subplots(nrows=2, ncols=3)

# Monday.plot(x="Mean",y=' NumberOfTrades',ax=axes[0,0])

# Tuesday.plot(x="Mean",y=' NumberOfTrades',ax=axes[0,1])

# Wednesday.plot(x="Mean",y=' NumberOfTrades',ax=axes[0,2])

# Thursday.plot(x="Mean",y=' NumberOfTrades',ax=axes[1,0])

# Friday.plot(x="Mean",y=' NumberOfTrades',ax=axes[1,1])



# fig, axes = plt.subplots(nrows=2, ncols=3)

# Monday.plot.scatter(x="Mean",y= "#trades/volume ratio",ax=axes[0,0])

# Tuesday.plot.scatter(x="Mean",y= "#trades/volume ratio",ax=axes[0,1])

# Wednesday.plot.scatter(x="Mean",y= "#trades/volume ratio",ax=axes[0,2])

# Thursday.plot.scatter(x="Mean",y="#trades/volume ratio",ax=axes[1,0])

# Friday.plot.scatter(x="Mean",y='#trades/volume ratio',ax=axes[1,1])

# fig, axes = plt.subplots(nrows=2, ncols=3)



# Monday.plot(x="Mean",y='Delta',ax=axes[0,0])

# Tuesday.plot(x="Mean",y='Delta',ax=axes[0,1])

# Wednesday.plot(x="Mean",y='Delta',ax=axes[0,2])

# Thursday.plot(x="Mean",y='Delta',ax=axes[1,0])

# Friday.plot(x="Mean",y='Delta',ax=axes[1,1])
plt.show()
