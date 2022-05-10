import Read_data_2 as RD
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import pandas as pd
"""
EST time
Sydney 17:00-00:00 7H 
Tokyo 19:00-04:00 9H
London 03:00-12:00 9H
NY 8:00-17:00 9H

EST time +1
Sydney 18:00-01:00 7H 
Tokyo 20:00-05:00 9H
London 04:00-13:00 9H
NY 09:00-18:00 9H

Solapamientos EST +1
Sydney-Tokyo 20:00-01:00 5H
Tokyo-Londres 04:00-05:00 1H
Londres-NY  09:00-13:00 4H
"""

n=datetime.now()
EURUSD_candels=RD.Candels("6EM22-CME.scid_BarData.txt")
k=datetime.now()-n

EURUSD=RD.Candel_study(EURUSD_candels)
O=datetime.now()-(n+k)


apertura_S=18
apertura_T=20
apertura_L=4
apertura_NY=8

overLap_S_T=20
overLap_T_L=4
overLap_L_NY=9

P1=18
P2=20
P3=1
P4=4
P5=5
P6=9
P7=13


H=9
h=7
O1=5
O2=1
O3=4

Sydney_POI=EURUSD.POIset(datetime(2022,2,6,P1),n=h-O1)#2
Sydney=EURUSD.period_study(datetime(2022,2,6,P1),n=h-O1)

S_T_POI=EURUSD.POIset(datetime(2022,2,6,P2),n=O1)#5
S_T=EURUSD.period_study(datetime(2022,2,6,P2),n=O1)

Tokyo_POI=EURUSD.POIset(datetime(2022,2,7,P3),n=H-O2-O1)#3
Tokyo=EURUSD.period_study(datetime(2022,2,7,P3),n=H-O2-O1)

T_L_POI=EURUSD.POIset(datetime(2022,2,7,P4),n=O2)#1
T_L=EURUSD.period_study(datetime(2022,2,7,P4),n=O2)

London_POI=EURUSD.POIset(datetime(2022,2,7,P5),n=H-O3-O2)#4
London=EURUSD.period_study(datetime(2022,2,7,P5),n=H-O3-O2)

L_NY_POI=EURUSD.POIset(datetime(2022,2,7,P6),n=O3)#4
L_NY=EURUSD.period_study(datetime(2022,2,7,P6),n=O3)

NY_POI=EURUSD.POIset(datetime(2022,2,7,P7),n=H-O3)#5
NY=EURUSD.period_study(datetime(2022,2,7,P7),n=H-O3)

Sydney2_POI=EURUSD.POIset(datetime(2022,2,7,P1),n=h-O1)
Sydney2=EURUSD.period_study(datetime(2022,2,7,P1),n=h-O1)

S_T2_POI=EURUSD.POIset(datetime(2022,2,7,P2),n=O1)
S_T2=EURUSD.period_study(datetime(2022,2,7,P2),n=O1)

Tokyo2_POI=EURUSD.POIset(datetime(2022,2,8,P3),n=H-O2-O1)
Tokyo2=EURUSD.period_study(datetime(2022,2,8,P3),n=H-O2-O1)

T_L2_POI=EURUSD.POIset(datetime(2022,2,8,P4),n=O2)
T_L2=EURUSD.period_study(datetime(2022,2,8,P4),n=O2)

London2_POI=EURUSD.POIset(datetime(2022,2,8,P5),n=H-O3-O2)
London2=EURUSD.period_study(datetime(2022,2,8,P5),n=H-O3-O2)

L_NY2_POI=EURUSD.POIset(datetime(2022,2,8,P6),n=O3)
L_NY2=EURUSD.period_study(datetime(2022,2,8,P6),n=O3)

NY2_POI=EURUSD.POIset(datetime(2022,2,8,P7),n=H-O3)
NY2=EURUSD.period_study(datetime(2022,2,8,P7),n=H-O3)

# S_T was deleted
Set=pd.DataFrame([Sydney_POI, S_T_POI, Tokyo_POI,T_L_POI,London_POI,L_NY_POI,NY_POI,Sydney2_POI,S_T2_POI,Tokyo2_POI,T_L2_POI,London2_POI,L_NY2_POI,NY2_POI])
print(Set)
print(EURUSD)
print("start: ",EURUSD.df.iloc[0,0].date())
print("final: ",EURUSD.df.iloc[-1,0])
Sydney.plot(x="Date",y=[" High"," Low"])
plt.title("Sydney "+str(Sydney["Date"].iloc[0]))

S_T.plot(x="Date",y=[" High"," Low"])
plt.title("Sydney-Tokyo " +str(S_T["Date"].iloc[0]))

Tokyo.plot(x="Date",y=[" High"," Low"] )
plt.title("Tokyo "+str(Tokyo["Date"].iloc[0]))

T_L.plot(x="Date",y=[" High"," Low"])
plt.title("Tokyo-Londres "+str(T_L["Date"].iloc[0]))

London.plot(x="Date",y=[" High"," Low"])
plt.title("Londres "+str(London["Date"].iloc[0]))

L_NY.plot(x="Date",y=[" High"," Low"])
plt.title("Londres-New York "+str(L_NY["Date"].iloc[0]))

NY.plot(x="Date",y=[" High"," Low", " Open"," Last"])
plt.title("New York "+str(NY["Date"].iloc[0]))



# Sydney2.plot(x="Date",y=[" High"," Low", " Open"," Last"])
# plt.title("Sydney2 "+str(Sydney2["Date"].iloc[0]))

# S_T2.plot(x="Date",y=[" High"," Low"])
# plt.title("Sydney-Tokyo " +str(S_T2["Date"].iloc[0]))

# Tokyo2.plot(x="Date",y=[" High"," Low"])
# plt.title("Tokyo2 "+str(Tokyo2["Date"].iloc[0]))

# T_L2.plot(x="Date",y=[" High"," Low"])
# plt.title("Tokyo-Londres "+str(T_L2["Date"].iloc[0]))

# London2.plot(x="Date",y=[" High"," Low"])
# plt.title("Londres2 "+str(London2["Date"].iloc[0]))

# L_NY2.plot(x="Date",y=[" High"," Low"])
# plt.title("Londres-New York "+str(L_NY2["Date"].iloc[0]))

# NY2.plot(x="Date",y=[" High"," Low"])
# plt.title("NY2 "+str(NY2["Date"].iloc[0]))

Set.plot(y="variacion TH-TL")
plt.title("variacion TH-TL")
Set.plot(y=["P high","P low"])
plt.title("price")
Set.plot(y="variacion PH-PL")
plt.title("variacion PH-PL")
print("import Candels time: " ,k)
print("candel study time: ",O)
plt.show()
