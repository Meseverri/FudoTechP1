import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import pandas as pd
# Ci son coordenadas del indice (numero entero) y no temporales 
def slope(P0,P1,C0,C1):
    m=(P1-P0)/(C1-C0)
    return m

def Price_point(P0,P1,C0,C1,C):
    m=slope(P0,P1,C0,C1)
    P=P0+m*(C-C0)
    return P

def Price_points(P0,P1,C0,C1,first_trend=True):
    Prices=[]
    if first_trend:
        for i in range(C0,C1+1):
            Prices.append(pd.Series([i,Price_point(P0,P1,C0,C1,i)],index=["Coord","Price"]))
    else:
        for i in range(C0+1,C1+1):
            Prices.append(pd.Series([i,Price_point(P0,P1,C0,C1,i)],index=["Coord","Price"]))

    return pd.DataFrame(Prices)


def Trend_lines(Pivots_table):
    count=0
    loc0=0
    loc1=1
    First_Trend=True
    Trends=[]
    while loc1<len(Pivots_table):
        X=[Pivots_table.iloc[loc0,:2].to_list(),Pivots_table.iloc[loc1,:2].to_list()]
        P=[X[0][0],X[1][0]]
        C=[X[0][1],X[1][1]]
        Trends.append(Price_points(P[0],P[1],C[0],C[1],first_trend=First_Trend))
        
        count+=1
        loc0+=1
        loc1+=1
        if count>0:
            First_Trend=False
    
    return pd.concat(Trends,ignore_index=True)








"""Formating the csv""" 
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

"""Ordenar los tiempos de los precios maximos y minimos de las sesiones tomadas"""
POI_H=POI.loc[:,["T High","P High"]]
POI_H.rename(columns={"T High":"T","P High":"P"},inplace=True)
POI_L=POI.loc[:,["T Low","P Low"]]
POI_L.rename(columns={"T Low":"T","P Low":"P"},inplace=True)
Price=pd.merge(left=POI_H,right=POI_L,how="outer").sort_values(by="T")

"""Creating the Uper and lower range with x*std distance from the mean and y rolling volatility and rolling mean """
x=1.55
y=14
SET_PER_DAY=2
Price["28 day std"]=Price["P"].rolling(y*SET_PER_DAY*2).std()
Price["28 day mean"]=Price["P"].rolling(y*SET_PER_DAY*2).mean()
Price["28 day Low Range"]=Price["28 day mean"]-x*Price["28 day std"]
Price["28 day High Range"]=Price["28 day mean"]+x*Price["28 day std"]

Price=Price.drop(["28 day std","28 day mean"],axis=1)
Price=Price.dropna()
Price["Index"]=range(len(Price))
Price=Price.set_index("Index")

Price["H_Pivots_candidates"]=Price["P"]>Price["28 day High Range"]
Price["L_Pivots_candidates"]=Price["P"]<Price["28 day Low Range"]

#finding the first pivot column
First_coord=0
# F_H=Price["H_Pivots"].index(True)
# F_L=Price["L_Pivots"].index(True)

F_H=0
F_L=0
Done=False
while not(Done):
    for i in Price["H_Pivots_candidates"]:
        if i==False:
            F_H+=1
        else:
            break
    for i in Price["L_Pivots_candidates"]:
        if i==False:
            F_L+=1
        else:
            Done=True
            break

if F_H>F_L:
    # Primero el Low
    First_coord=1

#Lista de los candidatos pivotes
H_coord_list=[]
L_coord_list=[]
L_count=0
H_count=0

for H in Price["H_Pivots_candidates"]:
    if H==True:
        H_coord_list.append(H_count)
        H_count+=1
    else:
        H_count+=1

for L in Price["L_Pivots_candidates"]:
    if L==True:
        L_coord_list.append(L_count)
        L_count+=1
    else:
        L_count+=1



min_len=min(len(H_coord_list),len(L_coord_list))


L_list=[]
H_list=[]
L_count=0
H_count=0
H_candidates=[]
L_candidates=[]
while min_len>H_count or min_len>L_count :
    
    if First_coord==1:
        for l in L_coord_list[L_count:]:
            if H_coord_list[H_count]>l:
                L_candidates.append(l)
                L_count+=1
            else:
                L_list.append(L_candidates)
                First_coord=0
                
                L_candidates=[]
                break
    if First_coord==0:
        for h in H_coord_list[H_count:]:
            if L_coord_list[L_count]>h :
                H_candidates.append(h)
                H_count+=1
            else:
                H_list.append(H_candidates)
                First_coord=1
                H_candidates=[]
                break
          
if min_len==H_count:
    H_list.append(H_candidates)
    L_list.append(L_coord_list[L_count:])
elif min_len==L_count:
    L_list.append(L_candidates)
    H_list.append(H_coord_list[H_count:])

"""Pivot table oficial"""


Max_Highs=[]
Min_Lows=[]

for P_candidates in H_list:
    Highs=[]
    for c in P_candidates:
        H_P=Price.iloc[c,0:2].to_list()
        H_P.append(c)
        H_P.append(True)
        Highs.append(H_P)
    Highs_df=pd.DataFrame(Highs,columns=["Date","Price","Coord","isHigh"])
    Max_Highs.append(Highs_df.iloc[Highs_df["Price"].idxmax()])


for P_candidates in L_list:
    Lows=[]
    for c in P_candidates:
        L_P=Price.iloc[c,0:2].to_list()
        L_P.append(c)
        L_P.append(False)
        Lows.append(L_P)

    Lows_df=pd.DataFrame(Lows,columns=["Date","Price","Coord","isHigh"])
    Min_Lows.append(Lows_df.iloc[Lows_df["Price"].idxmin()])
  
Max_Highs_df=pd.DataFrame(Max_Highs)
Min_Lows_df=pd.DataFrame(Min_Lows)
Pivot_table=pd.merge(left=Min_Lows_df,right=Max_Highs_df,how="outer").sort_values(by="Date")
Pivot_table["leg duration"]=Pivot_table["Date"]-Pivot_table["Date"].shift()
Pivot_table=Pivot_table.set_index("Date")



Trends=Trend_lines(Pivot_table)


Trends.plot(x="Coord",y="Price")

print("Precios ordenados:\n",Price)
print("Precios pivotes:\n",Pivot_table)
print("High Pivots:\n",Max_Highs_df)
print("Low Pivots:\n",Min_Lows_df)
print("Precios Siguiendo la pendiente de los Pivotes:\n",Trends)


PruebaL=pd.merge(POI,Pivot_table["isHigh"],how="left",right_on="Date",left_on="T Low")
PruebaH=pd.merge(POI,Pivot_table["isHigh"],how="left",right_on="Date",left_on="T High")
print(POI.columns)
# print(pruebaH)


plt.plot(Trends["Coord"],Trends["Price"])
plt.plot(Price.index,Price["P"])
plt.show()