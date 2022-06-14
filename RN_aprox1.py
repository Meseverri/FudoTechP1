from Read_data_2 import RN_study
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import pandas as pd

"""
Informacion referida a temporalidad "actual" se refiere a la vela recien cerrada (pensando en tiempo real)
Informacion referida a temporalidad "en curso" se refiere a la vela que no ha cerrado (pensando en tiempo real)

Atributos a usar para la RN
-Precio de apertura   +
-Bid de la vela actual +
-Ask de la vela actual +
-Numero de trades +
Derivados de Fechas para la instancia actual:
    -Week [Primera semana ,Segunda semana ,Tercera semana,cuarta semana] +
    -Dia de la semana (nominal lunes (0), martes (1), etc) +

Atributos de n sesiones hacia atras con las que la instancia actual esta reaccionando:
    Derivados de Fechas para cada sesion:
        -Week [Primera semana ,Segunda semana ,Tercera semana,cuarta semana] +
        -Dia de la semana (nominal lunes (0), martes (1), etc) +
        -Hora de apertura formato 24h +
                -Primer POI en overlap  (utilizar cuando tratemos con sesiones)
                -Segundo POI en overlap (utilizar cuando tratemos con sesiones)
        -Variacion en segundos desde apertura hasta primer POI +
        -Variacion en segundos del primer POI al segundo POI +
        -Variacion en segundos del segundo POI al close +
        
    -Precio de apertura +
    -Variacion en pips desde precio de apertura y primer POI +
    -Variacion en pips desde precio del primer POI al segundo POI +
    -Variacion en pips desde precio del segundo POI al close +

    -Media ponderada hasta el precio final de la sesion +
    -Desviacion tipica ponderada hasta el final de la sesion +
    -Cota superior del entorno de valor +
    -Cota inferior del entorno de valor +
    -frecuencia del entorno de valor -1 en la actual +
    -frecuencia del entorno de valor -2 en la actual + 
    -frecuencia del entorno de valor -3 en la actual -

    -K+ distancia del precio en curso por arriba de la media muestral (Se van calculando la media ponderada y la desviacion tipica acumuladas para cada instancia de la sesion) 
    -k- distancia del precio en curso por debajo de la media muestral (Se van calculando la media ponderada y la desviacion tipica acumuladas para cada instancia de la sesion)
    -K+ veces la desviacion tipica por arriba de la media muestral( la media y la desviacion estandar son constantes)
    -K- veces la desviacion tipica por abajo de la media muestral( la media y la desviacion estandar son constantes)

    
    -Bids acumulados de la sesion (total de bids) +
    -Asks acumulados de la sesion (total de asks) +
    -Bids acumulados por arriba de k+ veces la desviasion tipica de la sesion (total de bids)
    -Asks acumulados por arriba de k+ veces la desviasion tipica de la sesion (total de asks)
    -Bids acumulados por abajo de k- veces la desviasion tipica de la sesion (total de bids)
    -Asks acumulados por abajo de k- veces la desviasion tipica de la sesion (total de asks)


Atributo a predecir:
    -Variacion de precio en pips desde la vela actual hasta el close de la vela en curso (no usamos el precio porque tiene valores muy pequenos) +
    -Variacion de precio en pips desde la vela actual hasta el high de la vela en curso (no usamos el precio porque tiene valores muy pequenos) -
    -Variacion de precio en pips desde la vela actual hasta el low de la vela en curso (no usamos el precio porque tiene valores muy pequenos) -
    -Predecir la media ponderada del precio de la vela en curso (tendriamos el problema de predecir un precio muy pequeno) -
    
    
"""


df = RN_study("6EM22-CME.scid_BarData.txt")
