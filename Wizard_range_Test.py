import Read_data_2 as RD
import matplotlib.pyplot as plt
from datetime import datetime,timedelta


EURUSD_candels=RD.Candels("6EM22-CME.scid_BarData.txt")
EURUSD_Day=RD.Candel_study(EURUSD_candels,Setions="Day",X=1,Y=28*2)
POI_Day=EURUSD_Day.sample_DF
Price=EURUSD_Day.Prices_in_order
T_L=EURUSD_Day.TrendLines
print("trend lines:",T_L.to_string())
print("This is Price:",Price.to_string())


plt.plot(T_L["Coord"],T_L["Price"])
plt.plot(Price["Index"],Price["P"])
plt.show()