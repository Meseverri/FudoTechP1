import Read_data_2 as RD
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import pandas as pd
POI=pd.read_csv("EURUSD POI.csv",index_col=0)
POI["P high"]=POI["P high"].astype(float)
POI["P low"]=POI["P low"].astype(float)
POI["variacion PH-PL"]=POI["variacion PH-PL"].astype(float)

POI["Date"]=pd.to_datetime(POI["Date"])
POI["T high"]=pd.to_datetime(POI["T high"])
POI["T low"]=pd.to_datetime(POI["T low"])
RSet=POI

enero=POI[POI["Month"]=="Jan"]
febrero=POI[POI["Month"]=="Feb"]
marzo=POI[POI["Month"]=="Mar"]
abril=POI[POI["Month"]=="Apr"]
mayo=POI[POI["Month"]=="May"]
junio=POI[POI["Month"]=="Jun"]
julio=POI[POI["Month"]=="Jul"]
agosto=POI[POI["Month"]=="Aug"]
septiembre=POI[POI["Month"]=="Sep"]
octubre=POI[POI["Month"]=="Oct"]
noviembre=POI[POI["Month"]=="Nov"]
diciembre=POI[POI["Month"]=="Dec"]

enero2020=enero[enero["Year"]==2020]
enero2021=enero[enero["Year"]==2021]

febrero2020=febrero[febrero["Year"]==2020]
febrero2021=febrero[febrero["Year"]==2021]

marzo2020=marzo[marzo["Year"]==2020]
marzo2021=marzo[marzo["Year"]==2021]

abril2020=abril[abril["Year"]==2020]
abril2021=abril[abril["Year"]==2021]

mayo2020=mayo[mayo["Year"]==2020]
mayo2021=mayo[mayo["Year"]==2021]

junio2020=junio[junio["Year"]==2020]
junio2021=junio[junio["Year"]==2021]

julio2020=julio[julio["Year"]==2020]
julio2021=julio[julio["Year"]==2021]

agosto2020=agosto[agosto["Year"]==2020]
agosto2021=agosto[agosto["Year"]==2021]

septiembre2020=septiembre[septiembre["Year"]==2020]
septiembre2021=septiembre[septiembre["Year"]==2021]

octubre2020=octubre[octubre["Year"]==2020]
octubre2021=octubre[octubre["Year"]==2021]

noviembre2020=noviembre[noviembre["Year"]==2020]
noviembre2021=noviembre[noviembre["Year"]==2021]

diciembre2020=diciembre[diciembre["Year"]==2020]
diciembre2021=diciembre[diciembre["Year"]==2021]

print(RSet)

RSet2019=RSet[RSet["Year"]==2019]
RSet2020=RSet[RSet["Year"]==2020]
RSet2021=RSet[RSet["Year"]==2021]
RSet2022=RSet[RSet["Year"]==2022]

RSEnero_W0=RSet2020[RSet2020["Week"]==0]
RSEnero_W1=RSet2020[RSet2020["Week"]==1]
RSEnero_W2=RSet2020[RSet2020["Week"]==2]
RSEnero_W3=RSet2020[RSet2020["Week"]==3]
RSEnero_W4=RSet2020[RSet2020["Week"]==4]



enero2020.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("enero 2021")

febrero2020.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("febrero 2021")

marzo2020.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("marzo 2021")

abril2020.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("abril 2021")

mayo2020.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("mayo 2021")

junio2020.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("junio 2021")

julio2020.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("julio 2021")

agosto2020.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("agosto 2021")

septiembre2020.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("septiembre 2021")

octubre2020.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("octubre 2021")

noviembre2020.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("noviembre 2021")

diciembre2020.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("diciembre 2021")

"""2022"""
enero2021.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("enero 2022")

febrero2021.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("febrero 2022")

marzo2021.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("marzo 2022")

abril2021.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("abril 2022")

mayo2021.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("mayo 2022")

junio2021.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("junio 2022")

julio2021.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("julio 2022")

agosto2021.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("agosto 2022")

septiembre2021.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("septiembre 2022")

octubre2021.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("octubre 2022")

noviembre2021.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("noviembre 2022")

diciembre2021.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
plt.title("diciembre 2022")

# RSEnero_W0.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
# plt.title("Enero 2020 W0 ")
# RSEnero_W1.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
# plt.title("Enero 2020 W1 ")
# RSEnero_W2.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
# plt.title("Enero 2020 W2 ")
# RSEnero_W3.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
# plt.title("Enero 2020 W3 ")
# RSEnero_W4.plot(x="variacion PH-PL",y=["P high","P low"],style="o")
# plt.title("Enero 2020 W4 ")


# RSEnero_W0.plot(x="Date" ,y=["P high","P low"],style="o")
# plt.title("Enero 2020 W0 precio")
# RSEnero_W0.plot(x="T high",y="variacion PH-PL",style="o")
# plt.title("Enero 2020 W0")

# RSEnero_W1.plot(x="Date" ,y=["P high","P low"],style="o")
# plt.title("Enero 2020 W1 precio")
# RSEnero_W1.plot(x="T high",y="variacion PH-PL",style="o")
# plt.title("Enero 2020 W1")


# RSEnero_W2.plot(x="Date" ,y=["P high","P low"],style="o")
# plt.title("Enero 2020 W2 precio")
# RSEnero_W2.plot(x="T high",y="variacion PH-PL",style="o")
# plt.title("Enero 2020 W2")

# RSEnero_W3.plot(x="Date" ,y=["P high","P low"],style="o")
# plt.title("Enero 2020 W3 precio")
# RSEnero_W3.plot(x="T high",y="variacion PH-PL",style="o")
# plt.title("Enero 2020 W3")

# RSEnero_W4.plot(x="Date" ,y=["P high","P low"],style="o")
# plt.title("Enero 2020 W4 precio")
# RSEnero_W4.plot(x="T high",y="variacion PH-PL",style="o")
# plt.title("Enero 2020 W4")

"""

# enero2020[enero2020["Week"]==1].plot(x="T high",y=["P high","P low"])
# plt.title("Enero 2020 W1 precio")
# enero2020[enero2020["Week"]==1].plot(x="T high",y="variacion PH-PL")
# plt.title("Enero 2020 W1")

# enero2021[enero2021["Week"]==1].plot(y=["P high","P low"])
# plt.title("Enero 2021 W1 precio")
# enero2021[enero2021["Week"]==1].plot(x="T high",y="variacion PH-PL")
# plt.title("Enero 2021 W1")

# enero2022[enero2022["Week"]==1].plot(y=["P high","P low"])
# plt.title("Enero 2022 W1 precio")
# enero2022[enero2022["Week"]==1].plot(x="T high",y="variacion PH-PL")
# plt.title("Enero 2022 W1")

# enero2020[enero2020["Week"]==2].plot(y=["P high","P low"])
# plt.title("Enero 2020 W2 precio")
# enero2020[enero2020["Week"]==2].plot(x="T high",y="variacion PH-PL")
# plt.title("Enero 2020 W2")

# enero2021[enero2021["Week"]==2].plot(y=["P high","P low"])
# plt.title("Enero 2021 W2 precio")
# enero2021[enero2021["Week"]==2].plot(x="T high",y="variacion PH-PL")
# plt.title("Enero 2021 W2")

# enero2022[enero2022["Week"]==2].plot(y=["P high","P low"])
# plt.title("Enero 2022 W2 precio")
# enero2022[enero2022["Week"]==2].plot(x="T high",y="variacion PH-PL")
# plt.title("Enero 2022 W2")

# enero2020[enero2020["Week"]==3].plot(y=["P high","P low"])
# plt.title("Enero 2020 W3 precio")
# enero2020[enero2020["Week"]==3].plot(x="T high",y="variacion PH-PL")
# plt.title("Enero 2020 W3")

# enero2021[enero2021["Week"]==3].plot(y=["P high","P low"])
# plt.title("Enero 2021 W3 precio")
# enero2021[enero2021["Week"]==3].plot(x="T high",y="variacion PH-PL")
# plt.title("Enero 2021 W3")

# enero2022[enero2022["Week"]==3].plot(y=["P high","P low"])
# plt.title("Enero 2022 W3 precio")
# enero2022[enero2022["Week"]==3].plot(x="T high",y="variacion PH-PL")
# plt.title("Enero 2022 W3")

# enero2020[enero2020["Week"]==4].plot(y=["P high","P low"])
# plt.title("Enero 2021 W4 precio")
# enero2020[enero2020["Week"]==4].plot(x="T high",y="variacion PH-PL")
# plt.title("Enero 2020 W4")

# enero2021[enero2021["Week"]==4].plot(y=["P high","P low"])
# plt.title("Enero 2021 W4 precio")
# enero2021[enero2021["Week"]==4].plot(x="T high",y="variacion PH-PL")
# plt.title("Enero 2021 W4")

# enero2022[enero2022["Week"]==4].plot(y=["P high","P low"])
# plt.title("Enero 2022 W4 precio")
# enero2022[enero2022["Week"]==4].plot(x="T high",y="variacion PH-PL")
# plt.title("Enero 2022 W4")

"""
plt.show()


