import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def density_df(data,x_ax,frequency=True,y_ax=None, bins=100):
    data=data.round(6)
    minimo=data[x_ax].min()
    maximo=data[x_ax].max()
    rango=maximo-minimo
    interval_size=rango/bins
    Ranges=[]
    #Index_DF lista con el punto medio del intervalo de frequencia
    #Index_DF=[]
    dist_data=[]
    
    for k in range(bins):    
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
    print(Ranges)
    print(dist_data)
    dist=pd.DataFrame({"Index":Ranges,f"Frequencia {y_ax}":dist_data})
    dist[f"Frequencia {y_ax} relativa"]=dist[f"Frequencia {y_ax}"]/np.sum(dist_data)
    dist["Interval Size"]=interval_size
    dist["Vr*P"]=dist[f"Frequencia {y_ax} relativa"]*dist["Index"]
    dist["Vr*P^2"]=dist[f"Frequencia {y_ax} relativa"]*dist["Index"]**2

    return dist

def distribution_Series(dens_df,y_ax=None):
    dens_df.set_index("Index")
    
    pass

volume=pd.read_csv("EURUSD Volume.csv")
# volume_density=density_df(volume,"Mean",False," Volume")
volume_density=density_df(volume,"Mean")
volume.set_index("Mean")
volume_density.set_index("Index")
print(volume_density.cumsum())
