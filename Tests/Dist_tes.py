import pandas as pd
import random


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

s=[]
for i in range(100):
    s.append(random.randrange(1,10))
df=pd.Series(s)
print(s)
print("dist:\n",distribution_df(df,parts=10).to_string())
print("total:",distribution_df(df,parts=8).to_string())

