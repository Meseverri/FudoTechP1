import Read_data_2 as RD
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import pandas as pd

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

POI_H=POI.loc[:,["T High","P High"]]
POI_H.rename(columns={"T High":"T","P High":"P"},inplace=True)
POI_L=POI.loc[:,["T Low","P Low"]]
POI_L.rename(columns={"T Low":"T","P Low":"P"},inplace=True)
Price=pd.merge(left=POI_H,right=POI_L,how="outer").sort_values(by="T")


Price["30 day variance"]=Price["P"].rolling(30*2).std()
Price["30 day mean"]=Price["P"].rolling(30*2).mean()

Price["30 day Low Range"]=Price["30 day mean"]-1*Price["30 day variance"]
Price["30 day High Range"]=Price["30 day mean"]+1*Price["30 day variance"]

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
  


# if H_count==len(H_coord_list):
#     H_list.append(H_coord_list[H_count:])

# else:
#     L_list.append(L_coord_list[L_count:])

print("Total H count:",H_count,str(H_count==len(H_coord_list)))
print("Total l count:",L_count,str(L_count==len(L_coord_list)),"\n") 
print("Min len of the coord",min_len)



# print(Price)
 
print("\n"*2,"H pivot candidates coord:\n",H_list)
print("\n"*2,"L pivot candidates coord:\n",L_list)

print("H pivot last candidate coord:\n",H_coord_list[-1])
print("L pivot last candidate coord:\n",L_coord_list[-1],"\n")

# # print("H pivot last candidates coord:\n",H_list[-1])
# # print("L pivot last candidates coord:\n",L_list[-1])
# print("H missing list:\n",H_coord_list[H_count:])
# print("L missing list:\n",L_coord_list[L_count:])

Price.plot(y=["P","30 day Low Range","30 day High Range"])
plt.title("POI")
plt.show()