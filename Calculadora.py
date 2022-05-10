
import math

x1=-1
y2=(1+(22570/3600-3140/3600)**2)**(1/2)

print(-math.degrees(math.acos(x1/y2))+90,"deg")
print("arctan:",math.degrees(math.atan(x1/y2)),"deg")

