import Read_data_2 as RD
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import pandas as pd
POI=pd.read_csv("EURUSD POI.csv",index_col=0)
POI["P high"]=POI["P high"].astype(float)
POI["P low"]=POI["P low"].astype(float)
POI["H sweep"]=POI["H sweep"].astype(bool)
POI["L sweep"]=POI["L sweep"].astype(bool)
POI["Contenido"]=POI["Contenido"].astype(bool)

POI["variacion PH-PL"]=POI["variacion PH-PL"].astype(float)

POI["Date"]=pd.to_datetime(POI["Date"])
POI["T high"]=pd.to_datetime(POI["T high"])
POI["T low"]=pd.to_datetime(POI["T low"])

print(POI[POI["Trend"]=="D_sweep"])
D_sweep=POI[POI["Contenido"]==True][POI["H sweep"]==True]


D_sweep2019=D_sweep[D_sweep["Year"]==2019]
D_sweep2020=D_sweep[D_sweep["Year"]==2020]
D_sweep2021=D_sweep[D_sweep["Year"]==2021]
D_sweep2022=D_sweep[D_sweep["Year"]==2022]

D_sweep2019_S1=D_sweep2019[D_sweep2019["START hour"]==5]
D_sweep2020_S1=D_sweep2020[D_sweep2020["START hour"]==5]
D_sweep2021_S1=D_sweep2021[D_sweep2021["START hour"]==5]
D_sweep2022_S1=D_sweep2022[D_sweep2022["START hour"]==5]

D_sweep2020_S1_Sunday=D_sweep2020[D_sweep2020["Week day"]=="Sunday"]
D_sweep2020_S1_Monday=D_sweep2020[D_sweep2020["Week day"]=="Monday"]
D_sweep2020_S1_Tuesday=D_sweep2020[D_sweep2020["Week day"]=="Tuesday"]
D_sweep2020_S1_Wednesday=D_sweep2020[D_sweep2020["Week day"]=="Wednesday"]
D_sweep2020_S1_Thursday=D_sweep2020[D_sweep2020["Week day"]=="Thursday"]
D_sweep2020_S1_Friday=D_sweep2020[D_sweep2020["Week day"]=="Friday"]

D_sweep2021_S1_Sunday=D_sweep2021[D_sweep2021["Week day"]=="Sunday"]
D_sweep2021_S1_Monday=D_sweep2021[D_sweep2021["Week day"]=="Monday"]
D_sweep2021_S1_Tuesday=D_sweep2021[D_sweep2021["Week day"]=="Tuesday"]
D_sweep2021_S1_Wednesday=D_sweep2021[D_sweep2021["Week day"]=="Wednesday"]
D_sweep2021_S1_Thursday=D_sweep2021[D_sweep2021["Week day"]=="Thursday"]
D_sweep2021_S1_Friday=D_sweep2021[D_sweep2021["Week day"]=="Friday"]

print(len(POI[POI["Year"]==2020]))

print(len(D_sweep2020))
print(len(D_sweep2020_S1))



print(POI)
"""D_sweep2019.plot(x="Date",y=["P high","P low"],style="o")
plt.title("sweeps 2019")

D_sweep2020.plot(x="Date",y=["P high","P low"],style="o")
plt.title("sweeps 2020")

D_sweep2021.plot(x="Date",y=["P high","P low"],style="o")
plt.title("sweeps 2021")

D_sweep2022.plot(x="Date",y=["P high","P low"],style="o")
plt.title("sweeps 2022")

D_sweep2019_S1.plot(x="Date",y=["P high","P low"],style="o")
plt.title("sweeps 2019 S1")

D_sweep2020_S1.plot(x="Date",y=["P high","P low"],style="o")
plt.title("sweeps 2020 S1")

D_sweep2021_S1.plot(x="Date",y=["P high","P low"],style="o")
plt.title("sweeps 2021 S1")

D_sweep2022_S1.plot(x="Date",y=["P high","P low"],style="o")
plt.title("sweeps 2022 S1")
"""
# D_sweep2020_S1_Sunday.plot(x="Date",y="variacion Posterior PH-PL",style="o")
# plt.title("sweeps 2020 S1 Sunday")

# D_sweep2020_S1_Monday.plot(x="Date",y="variacion Posterior PH-PL",style="o")
# plt.title("sweeps 2020 S1 Monday")

# D_sweep2020_S1_Tuesday.plot(x="Date",y="variacion Posterior PH-PL",style="o")
# plt.title("sweeps 2020 S1 Tuesday")

# D_sweep2020_S1_Wednesday.plot(x="Date",y="variacion Posterior PH-PL",style="o")
# plt.title("sweeps 2020 S1 Wednesday")

# D_sweep2020_S1_Thursday.plot(x="Date",y="variacion Posterior PH-PL",style="o")
# plt.title("sweeps 2020 S1 Thursday")

# D_sweep2020_S1_Friday.plot(x="Date",y="variacion Posterior PH-PL",style="o")
# plt.title("sweeps 2020 S1 Friday")

# D_sweep2021_S1_Sunday.plot(x="Date",y="variacion Posterior PH-PL",style="o")
# plt.title("sweeps 2021 S1 Sunday")

# D_sweep2021_S1_Monday.plot(x="Date",y="variacion Posterior PH-PL",style="o")
# plt.title("sweeps 2021 S1 Monday")

# D_sweep2021_S1_Tuesday.plot(x="Date",y="variacion Posterior PH-PL",style="o")
# plt.title("sweeps 2021 S1 Tuesday")

# D_sweep2021_S1_Wednesday.plot(x="Date",y="variacion Posterior PH-PL",style="o")
# plt.title("sweeps 2021 S1 Wednesday")

# D_sweep2021_S1_Thursday.plot(x="Date",y="variacion Posterior PH-PL",style="o")
# plt.title("sweeps 2021 S1 Thursday")

# D_sweep2021_S1_Friday.plot(x="Date",y="variacion Posterior PH-PL",style="o")
# plt.title("sweeps 2021 S1 Friday")

# D_sweep2020.plot(x="variacion PH-PL",y="variacion Posterior PH-PL",style="o")
# plt.title("variacion Posterior PH-PL 2020")

# D_sweep2021.plot(x="variacion PH-PL",y="variacion Posterior PH-PL",style="o")
# plt.title("variacion Posterior PH-PL 2021")


# plt.show()