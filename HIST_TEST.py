import Read_data_2 as RD
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import pandas as pd

EURUSD_candels=RD.Candels("6EM22-CME.scid_BarData.txt")
EURUSD=EURUSD_candels.candels
EURUSD_VOL=EURUSD_candels.Volume

EURUSD_VOL[" BidVolume $"]=EURUSD_VOL["Mean"]*EURUSD_VOL[" BidVolume"]
EURUSD_VOL[" AskVolume $"]=EURUSD_VOL["Mean"]*EURUSD_VOL[" AskVolume"]

T0=datetime(2021,2,28,18)
T1=T0+timedelta(days=1)
T2=T1+timedelta(days=1)
T3=T2+timedelta(days=1)
T4=T3+timedelta(days=1)
T5=T4+timedelta(days=1)

EURUSD_LOCAL=EURUSD[EURUSD["Date"]>=T0][EURUSD["Date"]<=T1]
EURUSD_VOL_LOCAL=EURUSD_VOL[EURUSD_VOL["Date"]>=T0][EURUSD_VOL["Date"]<=T1]
EURUSD_LOCAL["Mean"].hist(bins=100)
plt.show()