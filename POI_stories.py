import Read_data_2 as RD
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import pandas as pd

n=datetime.now()
EURUSD_candels=RD.Candels("6EM22-CME.scid_BarData.txt",dropVolume=True)

EURUSD_Day=RD.Candel_study(EURUSD_candels,Setions="Day",X=1,Y=28*2)#1 set,28 dias 2pois
EURUSD_Original=RD.Candel_study(EURUSD_candels,X=1,Y=392)#7 sesiones al dia 28 dias 2 pois
EURUSD_R1=RD.Candel_study(EURUSD_candels,Setions="R1",X=1,Y=168)#3sets p.day, 28 dias 2 pois
EURUSD_R2=RD.Candel_study(EURUSD_candels,Setions="R2",X=1,Y=224)#4sets p.day, 28dias 2 pois

POI_Original=EURUSD_Original.sample_DF
POI_Day=EURUSD_Day.sample_DF
POI_R1=EURUSD_R1.sample_DF
POI_R2=EURUSD_R2.sample_DF

k=datetime.now()

POI_Original.to_csv("EURUSD POI Original.csv")
POI_Day.to_csv("EURUSD POI Day.csv")
POI_R1.to_csv("EURUSD POI R1.csv")
POI_R2.to_csv("EURUSD POI R2.csv")

print(n-k)


