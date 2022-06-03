
import math
from datetime import datetime,timedelta
# x1=-1
# y2=(1+(22570/3600-3140/3600)**2)**(1/2)

# print(-math.degrees(math.acos(x1/y2))+90,"deg")
# print("arctan:",math.degrees(math.atan(x1/y2)),"deg")

datetime1=datetime(2020,1,1)
datetime2=datetime(2020,1,2)
delta1=datetime2-datetime1
print(delta1)
print(delta1.total_seconds())
print(24*60*60)