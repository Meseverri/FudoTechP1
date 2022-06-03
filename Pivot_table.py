import Read_data_2 as RD
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import pandas as pd

"""cleanin the csv""" 
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

"""Creating the Uper en lower range with x*std distance from the mean and y rolling volatility and rolling mean """
x=1.7
y=30

Price["30 day variance"]=Price["P"].rolling(y*2).std()
Price["30 day mean"]=Price["P"].rolling(y*2).mean()
Price["30 day Low Range"]=Price["30 day mean"]-x*Price["30 day variance"]
Price["30 day High Range"]=Price["30 day mean"]+x*Price["30 day variance"]

Price=Price.drop(["30 day variance","30 day mean"],axis=1)
Price=Price.dropna()
Price["Index"]=range(len(Price))
Price=Price.set_index("Index")

Price["H_Pivots"]=Price["P"]>Price["30 day High Range"]
Price["L_Pivots"]=Price["P"]<Price["30 day Low Range"]

#finding the first pivt column
First_coord=0
F_H=0
F_L=0
Done=False
while not(Done):
    for i in Price["H_Pivots"]:
        if i==False:
            F_H+=1
        else:
            break
    for i in Price["L_Pivots"]:
        if i==False:
            F_L+=1
        else:
            Done=True
            break
if F_H>F_L:
    First_coord=1

#Lista de los candidatos pivotes
H_coord_list=[]
L_coord_list=[]
L_count=0
H_count=0
for L in Price["L_Pivots"]:
    if L==True:
        L_coord_list.append(L_count)
        L_count+=1
    else:
        
        L_count+=1
for H in Price["H_Pivots"]:
    if H==True:
        H_coord_list.append(H_count)
        H_count+=1
    else:
      
        H_count+=1

min_len=min(len(H_coord_list),len(L_coord_list))


L_list=[]
H_list=[]
done=False
L_count=0
H_count=0
Origin=First_coord
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
Pivot_table=Pivot_table.set_index("Date")

print("Pivots\n",Pivot_table)
print("Pivots 1:\n",[Pivot_table.iloc[0,:2].to_list(),Pivot_table.iloc[1,:2].to_list()])
print("Pivots 2:\n",[Pivot_table.iloc[1,:2].to_list(),Pivot_table.iloc[2,:2].to_list()])



# print("Prices:\n", Price)



Price.plot(y=["P","30 day Low Range","30 day High Range"])
plt.title("POI")
plt.show()