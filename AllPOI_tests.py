import Read_data_2 as RD
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import pandas as pd



POI_Day=pd.read_csv("EURUSD POI Day.csv",index_col=0)
POI_Original=pd.read_csv("EURUSD POI Original.csv",index_col=0)
POI_R1=pd.read_csv("EURUSD POI R1.csv",index_col=0)
POI_R2=pd.read_csv("EURUSD POI R2.csv",index_col=0)

POI_Day["P High"]=POI_Day["P High"].astype(float)
POI_Day["P Low"]=POI_Day["P Low"].astype(float)
POI_Day["H sweep"]=POI_Day["H sweep"].astype(bool)
POI_Day["L sweep"]=POI_Day["L sweep"].astype(bool)
POI_Day["Contenido"]=POI_Day["Contenido"].astype(bool)
POI_Day["variacion PH-PL"]=POI_Day["variacion PH-PL"].astype(float)
POI_Day["Date"]=pd.to_datetime(POI_Day["Date"])
POI_Day["T High"]=pd.to_datetime(POI_Day["T High"])
POI_Day["T Low"]=pd.to_datetime(POI_Day["T Low"])
# POI_Day["variacion TH-TL"]=pd.to_timedelta(POI_Day["variacion TH-TL"])
POI_Day["Trend -1"]=POI_Day["Trend"].shift()
POI_Day["Trend -2"]=POI_Day["Trend"].shift(2)



POI_Original["P High"]=POI_Original["P High"].astype(float)
POI_Original["P Low"]=POI_Original["P Low"].astype(float)
POI_Original["H sweep"]=POI_Original["H sweep"].astype(bool)
POI_Original["L sweep"]=POI_Original["L sweep"].astype(bool)
POI_Original["Contenido"]=POI_Original["Contenido"].astype(bool)
POI_Original["variacion PH-PL"]=POI_Original["variacion PH-PL"].astype(float)
POI_Original["Date"]=pd.to_datetime(POI_Original["Date"])
POI_Original["T High"]=pd.to_datetime(POI_Original["T High"])
POI_Original["T Low"]=pd.to_datetime(POI_Original["T Low"])
# POI_Original["variacion TH-TL"]=pd.to_timedelta(POI_Original["variacion TH-TL"])
POI_Original["Trend -1"]=POI_Original["Trend"].shift()
POI_Original["Trend -2"]=POI_Original["Trend"].shift(2)
POI_Original["Trend -3"]=POI_Original["Trend"].shift(3)
POI_Original["Trend -4"]=POI_Original["Trend"].shift(4)
POI_Original["Trend -5"]=POI_Original["Trend"].shift(5)
POI_Original["Trend -6"]=POI_Original["Trend"].shift(6)


POI_R1["P High"]=POI_R1["P High"].astype(float)
POI_R1["P Low"]=POI_R1["P Low"].astype(float)
POI_R1["H sweep"]=POI_R1["H sweep"].astype(bool)
POI_R1["L sweep"]=POI_R1["L sweep"].astype(bool)
POI_R1["Contenido"]=POI_R1["Contenido"].astype(bool)
POI_R1["variacion PH-PL"]=POI_R1["variacion PH-PL"].astype(float)
POI_R1["Date"]=pd.to_datetime(POI_R1["Date"])
POI_R1["T High"]=pd.to_datetime(POI_R1["T High"])
POI_R1["T Low"]=pd.to_datetime(POI_R1["T Low"])
# POI_R1["variacion TH-TL"]=pd.to_timedelta(POI_R1["variacion TH-TL"])
POI_R1["Trend -1"]=POI_R1["Trend"].shift()
POI_R1["Trend -2"]=POI_R1["Trend"].shift(2)
POI_R1["Trend -3"]=POI_R1["Trend"].shift(3)

POI_R2["P High"]=POI_R2["P High"].astype(float)
POI_R2["P Low"]=POI_R2["P Low"].astype(float)
POI_R2["H sweep"]=POI_R2["H sweep"].astype(bool)
POI_R2["L sweep"]=POI_R2["L sweep"].astype(bool)
POI_R2["Contenido"]=POI_R2["Contenido"].astype(bool)
POI_R2["variacion PH-PL"]=POI_R2["variacion PH-PL"].astype(float)
POI_R2["Date"]=pd.to_datetime(POI_R2["Date"])
POI_R2["T High"]=pd.to_datetime(POI_R2["T High"])
POI_R2["T Low"]=pd.to_datetime(POI_R2["T Low"])
# POI_R2["variacion TH-TL"]=pd.to_timedelta(POI_R2["variacion TH-TL"])
POI_R2["Trend -1"]=POI_R2["Trend"].shift()
POI_R2["Trend -2"]=POI_R2["Trend"].shift(2)
POI_R2["Trend -3"]=POI_R2["Trend"].shift(3)
POI_R2["Trend -4"]=POI_R2["Trend"].shift(4)


print("Day:\n True:\n")
print(POI_Day[POI_Day["isHigh"]==True].to_string())
print("False:\n")
print(POI_Day[POI_Day["isHigh"]==False].to_string())
print("Original:\n True:\n")
print(POI_Original[POI_Original["isHigh"]==True].to_string())
print("False:\n")
print(POI_Original[POI_Original["isHigh"]==False].to_string())
print("R1:\n True:\n")
print(POI_R1[POI_R1["isHigh"]==True].to_string())
print("False:\n")
print(POI_R1[POI_R1["isHigh"]==False].to_string())
print("R2:\n True:\n")
print(POI_R2[POI_R2["isHigh"]==True].to_string())
print("False:\n")
print(POI_R2[POI_R2["isHigh"]==False].to_string())

