import Read_data_2 as RD
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import pandas as pd

def trend(Contenido,H_sweep):        
    if Contenido==False:
        if H_sweep==True:
            return "T_Up"
        else:
            return "T_Down"
    else:
        if H_sweep==True:
            return "D_sweep"
        else:
            return "Converge"

POI=pd.read_csv("EURUSD POI.csv",index_col=0)
POI["P High"]=POI["P High"].astype(float)
POI["P Low"]=POI["P Low"].astype(float)
POI["H sweep"]=POI["H sweep"].astype(bool)
POI["L sweep"]=POI["L sweep"].astype(bool)
POI["Contenido"]=POI["Contenido"].astype(bool)

POI["variacion PH-PL"]=POI["variacion PH-PL"].astype(float)

POI["Date"]=pd.to_datetime(POI["Date"])
POI["T High"]=pd.to_datetime(POI["T High"])
POI["T Low"]=pd.to_datetime(POI["T Low"])
# POI=POI[POI["Week day"]=="Sunday"]

print(POI)


D_sweep=POI[POI["Trend"]=="D_sweep"]
T_Up=POI[POI["Trend"]=="T_Up"]
T_Down=POI[POI["Trend"]=="T_Down"]
Converge=POI[POI["Trend"]=="Converge"]



# T_Up[T_Up["Year"]==2020].plot(x="Date",y=["P High","P Low"],style="o")
# plt.title("Up trends")
# T_Down[T_Down["Year"]==2020].plot(x="Date",y=["P High","P Low"],style="o")
# plt.title("Down Trend")
# D_sweep[D_sweep["Year"]==2020].plot(x="Date",y=["P High","P Low"],style="o")
# plt.title("D_sweep")
# Converge[Converge["Year"]==2020].plot(x="Date",y=["P High","P Low"],style="o")
# plt.title("Converge")
# plt.show()
"""
T_Up.plot(x="Date",y=["P High","P Low"],style="o")
plt.title("Up trends")
T_Down.plot(x="Date",y=["P High","P Low"],style="o")
plt.title("Down Trend")
D_sweep.plot(x="Date",y=["P High","P Low"],style="o")
plt.title("D_sweep")
Converge.plot(x="Date",y=["P High","P Low"],style="o")
plt.title("Converge")
plt.show()
"""
POI_H=POI.loc[:,["T High","P High"]]
POI_H.rename(columns={"T High":"T","P High":"P"},inplace=True)
POI_L=POI.loc[:,["T Low","P Low"]]
POI_L.rename(columns={"T Low":"T","P Low":"P"},inplace=True)
print("High POI: \n",POI_H)
print("Lows POI: \n",POI_L)

POI["30 day rolling Min"]=POI["P Low"].rolling(4).min()
POI["30 day rolling Max"]=POI["P High"].rolling(4).max()

# Price=pd.concat([POI_H,POI_L])
Price=pd.merge(left=POI_H,right=POI_L,how="outer").sort_values(by="T")



Price["15 day variance"]=Price.rolling(30).std()
Price["15 day mean"]=Price["P"].rolling(30).mean()
Price["30 day variance"]=Price["P"].rolling(30*2).std()
Price["30 day mean"]=Price["P"].rolling(30*2).mean()

Price["15 day Low Range"]=Price["15 day mean"]-Price["15 day variance"]
Price["15 day High Range"]=Price["15 day mean"]+Price["15 day variance"]

Price["30 day Low Range"]=Price["30 day mean"]-1*Price["30 day variance"]
Price["30 day High Range"]=Price["30 day mean"]+1*Price["30 day variance"]

Price["30 day rolling Min"]=Price["P"].rolling(4).min()
Price["30 day rolling Max"]=Price["P"].rolling(4).max()
Price=Price.dropna()
Price["Index"]=range(len(Price))

Price=Price.set_index("Index")
print("Price data:\n",Price)


# Price["15 day High Range"]=Price["15 day High Range"].rolling(5).max()
# Price["15 day Low Range"]=Price["15 day Low Range"].rolling(5).min()


Price.plot(y=["P","30 day Low Range","30 day High Range"])
plt.title("POI")
Price.plot(x="T",y="30 day variance")
plt.title("15 day variance")
Price.hist(column="30 day variance")
plt.show()