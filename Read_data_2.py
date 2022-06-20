import pandas as pd
import numpy as np
from datetime import timedelta,datetime
import math
import warnings
warnings.filterwarnings('ignore')
warnings.warn('DelftStack')
warnings.warn('Do not show this message')

# def weekDay(serie):
def alpha(p,p0,p1):
    P=p-p0
    return P/(p1-p0)

def slope(P0,P1,C0,C1):
    m=(P1-P0)/(C1-C0)
    return m

#Trend toma como inputs 2 booleanos para identificar tendencias 
def trend(Contenido,H_sweep):        
    if Contenido==False:
        if H_sweep==True:
            return "T_Up"
        else:
            return "T_Down"
    else:
        if H_sweep==True:
            return "D_sweep"
        else:
            return "Converge"

def slope(P0,P1,C0,C1):
    m=(P1-P0)/(C1-C0)
    return m

def Price_point(P0,P1,C0,C1,C):
    m=slope(P0,P1,C0,C1)
    P=P0+m*(C-C0)
    return P

def Price_points(P0,P1,C0,C1,first_trend=True):
    Prices=[]
    if first_trend:
        for i in range(C0,C1+1):
            Prices.append(pd.Series([i,Price_point(P0,P1,C0,C1,i)],index=["Coord","Price"]))
    else:
        for i in range(C0+1,C1+1):
            Prices.append(pd.Series([i,Price_point(P0,P1,C0,C1,i)],index=["Coord","Price"]))

    return pd.DataFrame(Prices)
"""Calcula el conjunto de puntos de la recta que junta los pivotes"""


def Trend_lines(Pivots_table):
    count=0
    loc0=0
    loc1=1
    First_Trend=True
    Trends=[]
    while loc1<len(Pivots_table):
        X=[Pivots_table.iloc[loc0,:2].to_list(),Pivots_table.iloc[loc1,:2].to_list()]
        P=[X[0][0],X[1][0]]
        C=[X[0][1],X[1][1]]
        Trends.append(Price_points(P[0],P[1],C[0],C[1],first_trend=First_Trend))
        
        count+=1
        loc0+=1
        loc1+=1
        if count>0:
            First_Trend=False
    
    return pd.concat(Trends,ignore_index=True)

"""Ordenar los tiempos de los precios maximos y minimos de las sesiones tomadas"""
def Price_order(sample_DF):
    POI=sample_DF
    POI_H=POI.loc[:,["T High","P High"]]
    POI_H.rename(columns={"T High":"T","P High":"P"},inplace=True)
    POI_L=POI.loc[:,["T Low","P Low"]]
    POI_L.rename(columns={"T Low":"T","P Low":"P"},inplace=True)
    Price=pd.merge(left=POI_H,right=POI_L,how="outer").sort_values(by="T")

    return Price
"""Creating the Uper and lower range withbx*std distance from the mean and y rolling volatility and rolling mean """


def Outside_Wizards_range(Price,x=1,y=2,setion="Original"):
    #y is the look back of the deveation and the mean
    #x is the standard deveation
    #Sets_per_day indicates number of sets tha corresponds to the setions
    Original=Price
    Setion=setion
    X=x
    Y=y
    Price[f"{Y} lookback std"]=Price["P"].rolling(Y).std()
    Price[f"{Y} lookback mean"]=Price["P"].rolling(Y).mean()
    Price[f"{Y} lookback Low Range"]=Price[f"{Y} lookback mean"]-X*Price[f"{Y} lookback std"]
    Price[f"{Y} lookback High Range"]=Price[f"{Y} lookback mean"]+X*Price[f"{Y} lookback std"]

    #Price=Price.drop([f"{y} lookback std",f"{y} lookback mean"],axis=1)
    # Price=Price.dropna()
    Price["Index"]=range(len(Price))
    """Prize candidates"""
    Price=Price.set_index("Index")
    Price["H_Pivots_candidates"]=Price["P"]>Price[f"{Y} lookback High Range"]
    Price["L_Pivots_candidates"]=Price["P"]<Price[f"{Y} lookback Low Range"]
    print("L Wizards pivots",len(Price["L_Pivots_candidates"][Price["L_Pivots_candidates"]==True]),x,"std")
    print("H Wizards pivots",len(Price["H_Pivots_candidates"][Price["H_Pivots_candidates"]==True]),x,"std")
    if len(Price["L_Pivots_candidates"][Price["L_Pivots_candidates"]==True])==0 and len(Price["H_Pivots_candidates"][Price["H_Pivots_candidates"]==True])==0:
        print(f"The Wizard coldnt find POIs at {Setion} set with {X} Standard dev")
        X-=0.1
        Price=Outside_Wizards_range(Original,x=X,y=Y,setion=Setion)
    
    return Price
"""Devuelve 2 listas con los candidatos de highs y lows 
    siendo la primera los candidatos de High pivots"""
def Wizards_Price_Grouped(Price):
    # print(Price.to_string())
    L_coord_list=Price["L_Pivots_candidates"].index[Price["L_Pivots_candidates"]==True]
    H_coord_list=Price["H_Pivots_candidates"].index[Price["H_Pivots_candidates"]==True]
    
    min_len=min(len(H_coord_list),len(L_coord_list))

    #finding the first pivot column
    First_coord=True
    F_H=H_coord_list[0]
    F_L=L_coord_list[0]

    if F_H>F_L:
        # Primero el Low
        First_coord=False

    L_count=0
    L_candidates=[]
    L_list=[]

    H_count=0
    H_candidates=[]
    H_list=[]
    n=datetime.now()
    while min_len>H_count and min_len>L_count :
        # print(First_coord)
        
        if First_coord==False:
            for l in L_coord_list[L_count:]:
                
                if H_coord_list[H_count]>l:
                    L_candidates.append(l)
                    L_count+=1
                else:
                    L_list.append(L_candidates)
                    First_coord=True
                    L_candidates=[]
                    break

        if First_coord==True:
            for h in H_coord_list[H_count:]:
                # print("Second_loop",H_count)
                if L_coord_list[L_count]>h :
                    H_candidates.append(h)
                    H_count+=1
                else:
                    H_list.append(H_candidates)
                    First_coord=False
                    H_candidates=[]
                    break
        # print("First_loop",L_count)
        # print("Second_loop",H_count)
    # print("Min len",min_len, "H count",H_count, "Low count",L_count)
        
    if min_len==H_count:
        H_list.append(H_candidates)
        L_list.append(L_coord_list[L_count:])
        # print(L_coord_list[L_count:],"-----1-----")
    elif min_len==L_count:
        L_list.append(L_candidates)
        H_list.append(H_coord_list[H_count:])
        # print(L_candidates, "----2----")
    k=datetime.now()
    # print(H_list, L_list)
    print("Wizards loop Time: ",k-n)
    return H_list, L_list
"""Wizards_Pivots_DF devuelve un data frame con tabla de los pivotes highs a lows 
    con estas columnas ["Date","Price","Coord","isHigh"]""" 
def Wizards_Pivots_DF(H_list, L_list, Price):
    """Pivot table oficial"""
    Max_Highs=[]
    Min_Lows=[]

    for P_candidates in H_list:
        Highs=[]

        for c in P_candidates:
            H_P=Price.iloc[c,0:2].to_list()
            H_P.append(c)
            H_P.append(True)

            Highs.append(H_P)

        Highs_df=pd.DataFrame(Highs,columns=["Date","Price","Coord","isHigh"])
        Max_Highs.append(Highs_df.iloc[Highs_df["Price"].idxmax()])

    for P_candidates in L_list:
        Lows=[]

        for c in P_candidates:
            L_P=Price.iloc[c,0:2].to_list()
            L_P.append(c)
            L_P.append(False)
            Lows.append(L_P)

        Lows_df=pd.DataFrame(Lows,columns=["Date","Price","Coord","isHigh"])
        Min_Lows.append(Lows_df.iloc[Lows_df["Price"].idxmin()])
    
    Max_Highs_df=pd.DataFrame(Max_Highs)
    Min_Lows_df=pd.DataFrame(Min_Lows)
    # print("Min lows Wiz:",Min_Lows)
    # print("Max highs Wiz:",Max_Highs)
    Pivot_table=pd.merge(left=Min_Lows_df,right=Max_Highs_df,how="outer").sort_values(by="Date")
    Pivot_table=Pivot_table.set_index("Date")
    return Pivot_table

def getTrueIsHigh(isHigh1, isHigh2):

    if type(isHigh1) != float:
        return isHigh1

    if type(isHigh2) != float:
        return isHigh2
    return "NaN"

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    #for value in list1:

    return lst3

#input una lista otput dataframe de distribuciones
#data: Pandas dataframe
# x_ax: the column witch contains the main random variable
# frequency=True: True if you only need to count the number of times, False if volume is need 
# y_ax=None, 
# bins=100
def distribution_df(data,x_ax,frequency=True,y_ax=None, bins=100):
    data=data.round(6)
    minimo=data[x_ax].min()
    maximo=data[x_ax].max()
    rango=maximo-minimo
    interval_size=rango/bins
    Ranges=[]
    #Index_DF lista con el punto medio del intervalo de frequencia
    #Index_DF=[]
    dist_data=[]
    
    for k in range(bins+1):    
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
    

    dist=pd.DataFrame({"Index":Ranges,f"Frequencia {y_ax}":dist_data})
    dist[f"Frequencia {y_ax} relativa"]=dist[f"Frequencia {y_ax}"]/np.sum(dist_data)
    dist["Interval Size"]=interval_size
    dist["Vr*P"]=dist[f"Frequencia {y_ax} relativa"]*dist["Index"]
    dist["Vr*P^2"]=dist[f"Frequencia {y_ax} relativa"]*dist["Index"]**2

    return dist


class Candels:
    def __init__(self,Path_file,Sep=","):
        
        
        self.candels=pd.read_csv(Path_file,sep=Sep)
        self.candels["DateTime"]=self.candels["Date"]+self.candels[" Time"]
        self.candels["Date"]=pd.to_datetime(self.candels["DateTime"])
        self.candels["Mean"]=(self.candels[" Open"]+self.candels[" Last"]+self.candels[" High"]+self.candels[" Low"])/4
        self.candels["Delta"]=self.candels[" BidVolume"]-self.candels[" AskVolume"]
        self.candels["#trades/volume ratio"]=self.candels[" NumberOfTrades"]/self.candels[" Volume"]
        self.Volume=self.candels.loc[:,["Date","Mean"," Volume"," NumberOfTrades"," BidVolume"," AskVolume","Delta","#trades/volume ratio"]]
        
        # weekMonth = self.calendar()
        # self.candels["Week day"]=weekMonth["Week day"]
        # self.candels["Month"]=weekMonth["Month"]
        
        self.candels=self.candels.drop(["DateTime"," Time"," Volume"," NumberOfTrades"," BidVolume"," AskVolume","Delta","#trades/volume ratio"],axis=1)
       
    def calendar(self):
        WL=[]
        for i in self.candels["Date"].tolist():
            W=i.strftime("%A")
            M=i.strftime("%b")
            WL.append([W,M])
        
        return pd.DataFrame(WL,columns=["Week day","Month"])


    def __str__(self):
        return str(self.candels)
    
class Candel_study:
    def __init__(self,Candels,Setions="Original",X=1,Y=28):
        n=datetime.now()
       
        self.df=Candels.candels
        self.Setion=Setions
        self.sample_DF=self.sample_df(setion=Setions)
        self.Prices_in_order=self.Price_order()
        self.Pivots_table=pd.DataFrame()
        #X,Y volatility and lookback
        self.getIsHighColumn(X,Y)
        self.TrendLines=Trend_lines(self.Pivots_table)
        k=datetime.now()-n
        print(f"POI table setion {self.Setion} took: ",k)
        self.Volume=Candels.Volume
        
        # No se usa mucho por ahora y ademas hay que considerar el caso "="
        self.df["isBull"]=self.df[" Last"]>self.df[" Open"]
        # self.start=self.df.loc[:,"Date"].iat[0,0]

    #period_study devuelve una tabla con n horas desde una hora de inicio
    def period_study(self,Datetime,n=7):
        delta1=timedelta(hours=n)

        POI_sample_set=self.df[((self.df["Date"]>=Datetime) & (self.df["Date"]<Datetime+delta1))]

        # POI_sample_set["Alpha High"]=alpha(POI_sample_set[" High"],H0,H1)
        # POI_sample_set["Alpha Low"]=alpha(POI_sample_set[" Low"],H0,H1)
        
        return POI_sample_set

    def POIset(self,Datetime,n=7):
        POI_df=self.period_study(Datetime,n=n)
        P0=POI_df[" Open"].iloc[0]
        PC=POI_df[" Last"].iloc[-1]
        Ph=POI_df[" High"].max()
        Pl=POI_df[" Low"].min()
        POI_df["Alpha High"]=alpha(POI_df[" High"],Pl,Ph)
        POI_df["Alpha Low"]=alpha(POI_df[" Low"],Pl,Ph)
        Tl=POI_df[POI_df["Alpha Low"]==0].loc[:,["Date"]].iat[0,0]
        Th=POI_df[POI_df["Alpha High"]==1].loc[:,["Date"]].iat[0,0]
        ret=[Datetime,Datetime.strftime("%Y"),Datetime.strftime("%U"),Datetime.strftime("%b"),Datetime.hour,Datetime.strftime("%A"),Th,Tl,P0,Ph,Pl,PC]
      
        if Tl>Th:
            ret.append((Tl-Th).total_seconds())
            ret.append(-(Ph-Pl))
            ret.append(P0-Pl)
            ret.append(Ph-PC)
            ret.append(Tl>Th)
            

            
        else:
            ret.append((Th-Tl).total_seconds())
            ret.append((Ph-Pl))
            ret.append(P0-Ph)
            ret.append(Pl-PC)
            ret.append(Tl>Th)
       
        RET=pd.Series(ret,["Date",
            "Year",
            "Week",
            "Month",
            "START hour",
            "Week day",
            "T High",
            "T Low",
            "P Open",
            "P High",
            "P Low",
            "P Close",
            "variacion TH-TL",
            "variacion PH-PL",
            "Open to POI",
            "POI to Close",
            "High first"])
            
        return RET
       

    def setions_sample_df(self, START,Setions="Original"):
        P1=18
        # P7=13
        if Setions=="Original":
            
            S=2
            O_ST=5
            T=3
            O_TL=1
            L=4
            O_LNY=4
            NY=5
            
            # Caso inicial 18:00H
            if START.hour == P1:

                Sydney_POI= self.POIset(START,n=S)
                START=START+timedelta(hours=S)

                S_T_POI= self.POIset(START,n=O_ST)
                START=START+timedelta(hours=O_ST)
            
                Tokyo_POI= self.POIset(START,n=T)
                START=START+timedelta(hours=T)

                T_L_POI= self.POIset(START,n=O_TL)
                START=START+timedelta(hours=O_TL)

                London_POI= self.POIset(START,n=L)
                START=START+timedelta(hours=L)

                L_NY_POI= self.POIset(START,n=O_LNY)
                START=START+timedelta(hours=O_LNY)

                NY_POI= self.POIset(START,n=NY)
                START=START+timedelta(hours=NY)


                return pd.DataFrame([Sydney_POI, S_T_POI, Tokyo_POI,T_L_POI,London_POI,L_NY_POI,NY_POI])
            else:
                raise Exception(f"Hour datatime not correct, must be {P1}")
        elif Setions=="R1":
            S1=11
            S2=6
            S3=7

            if START.hour == P1:
                # Asia: Sidney + Tokio
                Set1=self.POIset(START,n=S1)
                START=START+timedelta(hours=S1)

                # Londres
                Set2=self.POIset(START,n=S2)
                START=START+timedelta(hours=S2)

                # NY
                Set3=self.POIset(START,n=S3)
                START=START+timedelta(hours=S3)
                
                return pd.DataFrame([Set1, Set2, Set3])
            else:
                raise Exception(f"Hour datatime not correct, must be {P1}")
        
        elif Setions=="R2":
            S1=7
            S2=4
            S3=6
            S4=7

            if START.hour == P1:

                # Sidney para para raul
                Set1=self.POIset(START,n=S1)
                START=START+timedelta(hours=S1)

                # Tokio para para raul
                Set2=self.POIset(START,n=S2)
                START=START+timedelta(hours=S2)

                # Londres para para raul
                Set3=self.POIset(START,n=S3)
                START=START+timedelta(hours=S3)

                # NY para para raul
                Set4=self.POIset(START,n=S4)
                START=START+timedelta(hours=S4)
                
                return pd.DataFrame([Set1, Set2, Set3, Set4])
            else:
                raise Exception(f"Hour datatime not correct, must be {P1}")
        elif Setions=="Day":
            S1=24
            if START.hour == P1:

                # Dia completo respecto a sesiones Sidney-NY  
                Set1=self.POIset(START,n=S1)
                START=START+timedelta(hours=S1)
                
                return pd.DataFrame([Set1])
            else:
                raise Exception(f"Hour datatime not correct, must be {P1}")

        elif Setions=="Week":
            S1=24*5
            if START.hour == P1:

                # Semana completa respecto a sesiones Sidney-NY  
                Set1=self.POIset(START,n=S1)
                START=START+timedelta(hours=S1)
        
                return pd.DataFrame([Set1])
            else:
                raise Exception(f"Hour datatime not correct, must be {P1}")
        elif Setions=="Month":
            S1=24*5*4
            W=4
            if START.hour == P1:

                # Mes completo respecto a sesiones Sidney-NY  
                Set1=self.POIset(START,n=S1)
                START=START+timedelta(weeks=W)
        
                return pd.DataFrame([Set1])
            else:
                raise Exception(f"Hour datatime not correct, must be {P1}")


    
    def sample_df(self,setion="Original"):
        # Asumimos que empieza en la hora correcta EJEMPLO: 2019-09-12 18:00:00
        START=self.df.iloc[0,0]
        
        print("Start date of sample:",START)
        FINAL=self.df.iloc[-1,0]
        print("Final date of sample:",FINAL)

        _dicDeltaTime = {
            "Original":1,
            "R1":1,
            "R2":1,
            "Day":1,
            "Week":7,
            "Month":28
        }
       
        DF_list=[]
        DF_POI=pd.DataFrame()
        
        c=0
        while START <= FINAL :
            
            try:
                
                DF = self.setions_sample_df(START,setion)

                DF_list.append(DF)
                
                c+=1
            except Exception as e: #Ignora los dias que da error
                
                c+=1
                pass

            START=START+timedelta(days=_dicDeltaTime[setion])
       
        
        POI=pd.concat(DF_list,ignore_index=True)
        POI["H sweep"]=POI["P High"]>POI["P High"].shift()
        POI["L sweep"]=POI["P Low"]<POI["P Low"].shift()
        POI["Variacion Posterior PH-PL"]=POI["variacion PH-PL"].shift(-1)
        
        # conditions=[POI["H sweep"]==True,POI["L sweep"]==True]
        POI["Contenido"]=POI["H sweep"]==POI["L sweep"]
        Data=POI[["Contenido","H sweep"]]
        POI["Trend"]=Data.apply(lambda x: trend(x["Contenido"],x["H sweep"]),axis=1)
        
        return POI
    
    
    
    def Price_order(self):
        POI=self.sample_DF
        POI_H=POI.loc[:,["T High","P High"]]
        POI_H.rename(columns={"T High":"T","P High":"P"},inplace=True)
        POI_L=POI.loc[:,["T Low","P Low"]]
        POI_L.rename(columns={"T Low":"T","P Low":"P"},inplace=True)
        Price=pd.merge(left=POI_H,right=POI_L,how="outer").sort_values(by="T")

        return Price

    def getIsHighColumn(self,X=1,Y=28 ):
        """Ordenar los tiempos de los precios maximos y minimos de las sesiones tomadas"""
        Prices=self.Prices_in_order
        POI=self.sample_DF
        """Creating the Uper and lower range with x*std distance from the mean and y rolling volatility and rolling mean """
        Prices=Outside_Wizards_range(Prices,x=X,y=Y,setion=self.Setion)
        H_list, L_list = Wizards_Price_Grouped(Prices)
        Pivot_table = Wizards_Pivots_DF(H_list, L_list, Prices)
        # print(Pivot_table)
        self.Pivots_table=Pivot_table
        Merge1=pd.merge(POI,Pivot_table["isHigh"],how="left",right_on="Date",left_on="T Low")
        POI=pd.merge(Merge1,Pivot_table["isHigh"],how="left",right_on="Date",left_on="T High")
        POI["isHigh"]=POI.apply(lambda x: getTrueIsHigh(x["isHigh_x"], x["isHigh_y"]), axis=1)
        POI = POI.drop(["isHigh_x","isHigh_y"], axis=1)
        self.sample_DF=POI
        print("*"*15," The Magician has succesfully found the pivots ","*"*15)
        


    def save_data(self,path,dataframe):
        pd.to_csv(path)
        print(f"saved at {path}")

 
    def __str__(self):
        return str(self.df)

def get_week(day):
    if day < 8:
        return 1
    if day < 15:
        return 2
    if day < 22:
        return 3
    
    return 4

def stats_setion_Series(dist_df):
    Mean=dist_df["Vr*P"].sum()
    Var=dist_df["Vr*P^2"].sum()-Mean**2
    Std=Var**(1/2)
    stats={"Media":Mean,
            "Std":Std}
    return pd.Series(stats)

def frequency_inside(inf,sup,dist_df):
    df=dist_df[dist_df["Index"]>inf][dist_df["Index"]<sup]
    Fr=df.iloc[:,2]
    return Fr.sum() 

def calculo_k_medio (df_in, bins, Weighted_mean_fixed, Std_fixed):
    #Cantidad de elementos dentro de un bin para crear bins filas
    gb_bins = len(df_in)/bins

    df_in.drop([" NumberOfTrades", " Alpha High", " Alpha Low", " Hash"], axis=1)
    df_in=df_in.groupby(df_in.index//gb_bins).agg({
                        'Date': 'first',
                        ' Open': 'first',
                        ' High': 'max',
                        ' Low': 'min',
                        ' Last': 'last',
                        ' Volume': 'sum',
                        ' BidVolume': 'sum', 
                        ' AskVolume': 'sum',
    })
    df_in[' Hash']=(df_in[" Open"]+df_in[" Last"]+df_in[" High"]+df_in[" Low"])/4


    df_in[" P*V"]=df_in[" Volume"] * df_in[" Hash"]
    df_in[" Acum P*V"]=df_in[" P*V"].cumsum()
    df_in[" Acum Volume"]=df_in[" Volume"].cumsum()
    df_in[" Weighted Mean"]=df_in[" Acum P*V"] / df_in[" Acum Volume"]
    df_in[" P**2*V"]=df_in[" Volume"] * (df_in[" Hash"]**2)
    df_in[" Acum P**2*V"]=df_in[" P**2*V"].cumsum()
    df_in[" Weighted Mean 2"]=(df_in[" Acum P**2*V"])/df_in[" Acum Volume"]
    df_in[" Std"]= (df_in[" Weighted Mean 2"] - df_in[" Weighted Mean"]**2)**(1/2)
    df_in[" k"]=(df_in[" Hash"] - df_in[" Weighted Mean"])/df_in[" Std"]
    df_in[" k Fixed"]=(df_in[" Hash"] - Weighted_mean_fixed)/Std_fixed

    kpos_movil=df_in[df_in[" k"]>0][" k"]
    mean_kpos_movil = kpos_movil.mean()
    max_k_movil = kpos_movil.max()
    over_kpos_movil_bids=df_in[df_in[" k"]>mean_kpos_movil][" BidVolume"].sum()
    over_kpos_movil_asks=df_in[df_in[" k"]>mean_kpos_movil][" AskVolume"].sum()


    

    kneg_movil=df_in[df_in[" k"]<0][" k"]
    mean_kneg_movil = kneg_movil.mean()
    min_k_movil = kneg_movil.min()
    below_kneg_movil_bids=df_in[df_in[" k"]<mean_kneg_movil][" BidVolume"].sum()
    below_kneg_movil_asks=df_in[df_in[" k"]<mean_kneg_movil][" AskVolume"].sum()



    kpos_fixed=df_in[df_in[" k Fixed"]>0][" k Fixed"]
    mean_kpos_fixed = kpos_fixed.mean()
    max_k_fixed = kpos_fixed.max()
    over_kpos_fixed_bids=df_in[df_in[" k Fixed"]>mean_kpos_fixed][" BidVolume"].sum()
    over_kpos_fixed_asks=df_in[df_in[" k Fixed"]>mean_kpos_fixed][" AskVolume"].sum()

    kneg_fixed=df_in[df_in[" k Fixed"]<0][" k Fixed"]
    mean_kneg_fixed = kneg_fixed.mean()
    min_k_fixed = kneg_fixed.min()
    below_kneg_fixed_bids=df_in[df_in[" k Fixed"]<mean_kneg_fixed][" BidVolume"].sum()
    below_kneg_fixed_asks=df_in[df_in[" k Fixed"]<mean_kneg_fixed][" AskVolume"].sum()


    return {
        ' k+ Movil':mean_kpos_movil,
        ' Max k Movil':max_k_movil,
        ' k- Movil':mean_kneg_movil,
        ' Min k Movil':min_k_movil,
        ' k+ Fixed':mean_kpos_fixed,
        ' Max k Fixed':max_k_fixed,
        ' k- Fixed':mean_kneg_fixed,
        ' Min k Fixed':min_k_fixed,
        ' Bids Over k+ Movil':over_kpos_movil_bids,
        ' Asks Over k+ Movil':over_kpos_movil_asks,
        ' Bids Below k- Movil':below_kneg_movil_bids,
        ' Asks Below k- Movil':below_kneg_movil_asks,
        ' Bids Over k+ Fixed':over_kpos_fixed_bids,
        ' Asks Over k+ Fixed':over_kpos_fixed_asks,
        ' Bids Below k- Fixed':below_kneg_fixed_bids,
        ' Asks Below k- Fixed':below_kneg_fixed_asks,
    }



    


class RN_study:

    def __init__(self,path="", sep=","):
       
        self.df = pd.read_csv(path, sep=sep)
        self.df[" DateTime"]=pd.to_datetime(self.df["Date"]+self.df[" Time"])
        self.df["Date"]=pd.to_datetime(self.df["Date"])
        self.traning_df = self.df.copy()
        self.df["Date"] = self.df[" DateTime"]
        self.df.drop([" DateTime"," Time"],axis=1, inplace=True)
        self.traning_df.drop([" DateTime"," Time", " High", " Low", " Volume", " Last"],axis=1, inplace=True)
        self.traning_df = self.traning_df.groupby("Date").agg({
                        ' Open': 'first',
                        ' BidVolume': 'sum',
                        ' AskVolume': 'sum',
                        ' NumberOfTrades': 'sum'
        })
        self.traning_df[" week"] = [get_week(x.day) for x in self.traning_df.index]
        self.traning_df[" week_day"] = [x.weekday() for x in self.traning_df.index]

        for indexDateTime  in self.traning_df.index:
            sesion_datetime = indexDateTime - timedelta(days=1)
            sesion_datetime = sesion_datetime.replace(hour=18,minute=0)

            try:
                self.create_sesions_columns(sesion_datetime, indexDateTime)
            except IndexError:
                pass

        #Class to Predict
        Shifted_tr_df = self.traning_df.shift(periods=-1)
        self.traning_df["Class to Predict-Close Var"] = (self.traning_df[" Open"] - Shifted_tr_df[" Open"])*10000
        


        # print(self.df.iloc[15:35,:])
        print(self.traning_df.iloc[15:35,:].dropna().to_string())

    def alpha(p,p0,p1):
        P=p-p0
        return P/(p1-p0)

    def period_study(self,Datetime,n):
        delta1=timedelta(hours=n)

        return self.df[((self.df["Date"]>=Datetime) & (self.df["Date"]<Datetime+delta1))]
      
    def POIset(self,Datetime,n, Sesion, indexDateTime):
        POI_df=self.period_study(Datetime,n=n).copy()
        POI_df.reset_index(drop=True, inplace=True)
        POI_df[" Hash"]=(POI_df[" Open"]+POI_df[" Last"]+POI_df[" High"]+POI_df[" Low"])/4

        To=Datetime #Tiempo de apertura
        Po=POI_df[" Open"].iloc[0]
        Tc= POI_df.at[POI_df.index[-1], "Date"]
        Pc= POI_df.at[POI_df.index[-1], " Last"]

        Ph=POI_df[" High"].max()
        Pl=POI_df[" Low"].min()
        POI_df[" Alpha High"]=alpha(POI_df[" High"],Pl,Ph)
        POI_df[" Alpha Low"]=alpha(POI_df[" Low"],Pl,Ph)
        Th=POI_df[POI_df[" Alpha High"]==1].iat[0,0]
        Tl=POI_df[POI_df[" Alpha Low"]==0].iat[0,0]

        Bids_acum = POI_df[" BidVolume"].sum()
        Asks_acum = POI_df[" AskVolume"].sum()

        #Sesion actual entorno de valor
        Price_dist=distribution_df(POI_df,x_ax=" Hash",frequency=False,y_ax=" Volume",bins=300)
        Volume_stats=stats_setion_Series(Price_dist)
        Std = Volume_stats["Std"] 
        Weigthed_mean = Volume_stats["Media"]

        #Sesion actual -1 dia entorno de valor
        POI_df_1 = self.period_study(Datetime-timedelta(days=1),n=n).copy()
        POI_df_1[" Hash"]=(POI_df_1[" Open"]+POI_df_1[" Last"]+POI_df_1[" High"]+POI_df_1[" Low"])/4
        Price_dist_1=distribution_df(POI_df_1,x_ax=" Hash",frequency=False,y_ax=" Volume",bins=300)
        Volume_stats_1=stats_setion_Series(Price_dist_1)
        fr_vol_1=frequency_inside(Volume_stats_1["Media"]-Volume_stats_1["Std"],Volume_stats_1["Media"]+Volume_stats_1["Std"],Price_dist)

        #Sesion actual -2 dia entorno de valor
        POI_df_2 = self.period_study(Datetime-timedelta(days=2),n=n).copy()
        POI_df_2[" Hash"]=(POI_df_2[" Open"]+POI_df_2[" Last"]+POI_df_2[" High"]+POI_df_2[" Low"])/4
        Price_dist_2=distribution_df(POI_df_2,x_ax=" Hash",frequency=False,y_ax=" Volume",bins=300)
        Volume_stats_2=stats_setion_Series(Price_dist_2)
        fr_vol_2=frequency_inside(Volume_stats_2["Media"]-Volume_stats_2["Std"],Volume_stats_2["Media"]+Volume_stats_2["Std"],Price_dist)

        #Calculo de las k
        ks =calculo_k_medio(POI_df,300,Weigthed_mean,Std)
     
        #Derivado de Fecha
        self.traning_df.loc[indexDateTime,f" {Sesion} - week"] = get_week(Datetime.day)
        self.traning_df.loc[indexDateTime,f" {Sesion} - week_day"] = Datetime.weekday()
        self.traning_df.loc[indexDateTime,f" {Sesion} - Open Time"] = To.hour
        #No Derivado de Fecha
        self.traning_df.loc[indexDateTime,f" {Sesion} - Open Price"] = Po
        self.traning_df.loc[indexDateTime,f" {Sesion} - Weigthed Mean"] = Weigthed_mean
        self.traning_df.loc[indexDateTime,f" {Sesion} - Upper limmit Value Zone"] = Weigthed_mean + 1*Std
        self.traning_df.loc[indexDateTime,f" {Sesion} - Lower limmit Value Zone"] = Weigthed_mean - 1*Std
        self.traning_df.loc[indexDateTime,f" {Sesion} - % Frecuency inside Sesion Value Zone -1"] = fr_vol_1*100
        self.traning_df.loc[indexDateTime,f" {Sesion} - % Frecuency inside Sesion Value Zone -2"] = fr_vol_2*100
        self.traning_df.loc[indexDateTime,f" {Sesion} - Std Weigthed"] = Std
        self.traning_df.loc[indexDateTime,f" {Sesion} - Bids Acumulated"] = Bids_acum
        self.traning_df.loc[indexDateTime,f" {Sesion} - Asks Acumulated"] = Asks_acum

        self.traning_df.loc[indexDateTime,f" {Sesion} - k+ Movil Mean"] = ks[' k+ Movil']
        self.traning_df.loc[indexDateTime,f" {Sesion} - k- Movil Mean"] = ks[' k- Movil']
        self.traning_df.loc[indexDateTime,f" {Sesion} - k+ Fixed Mean"] = ks[' k+ Fixed']
        self.traning_df.loc[indexDateTime,f" {Sesion} - k- Fixed Mean"] = ks[' k- Fixed']

        self.traning_df.loc[indexDateTime,f" {Sesion} - k Movil Max"] = ks[' Max k Movil']
        self.traning_df.loc[indexDateTime,f" {Sesion} - k Movil Min"] = ks[' Min k Movil']
        self.traning_df.loc[indexDateTime,f" {Sesion} - k Fixed Max"] = ks[' Max k Fixed']
        self.traning_df.loc[indexDateTime,f" {Sesion} - k Fixed Min"] = ks[' Min k Fixed']
        
        self.traning_df.loc[indexDateTime,f" {Sesion} - Bids Over k+ Movil"] = ks[' Bids Over k+ Movil']
        self.traning_df.loc[indexDateTime,f" {Sesion} - Asks Over k+ Movil"] = ks[' Asks Over k+ Movil']
        self.traning_df.loc[indexDateTime,f" {Sesion} - Bids Below k- Movil"] = ks[' Bids Below k- Movil']
        self.traning_df.loc[indexDateTime,f" {Sesion} - Asks Below k- Movil"] = ks[' Asks Below k- Movil']
        self.traning_df.loc[indexDateTime,f" {Sesion} - Bids Over k+ Fixed"] = ks[' Bids Over k+ Fixed']
        self.traning_df.loc[indexDateTime,f" {Sesion} - Asks Over k+ Fixed"] = ks[' Asks Over k+ Fixed']
        self.traning_df.loc[indexDateTime,f" {Sesion} - Bids Below k- Fixed"] = ks[' Bids Below k- Fixed']
        self.traning_df.loc[indexDateTime,f" {Sesion} - Asks Below k- Fixed"] = ks[' Asks Below k- Fixed']
        
        if Tl<Th: # Primer POI = Low
            #Derivado de Fecha
            self.traning_df.loc[indexDateTime,f" {Sesion} - Var Segs Open-POI1"] = (Tl-To).total_seconds()
            self.traning_df.loc[indexDateTime,f" {Sesion} - Var Segs POI1-POI2"] = (Th-Tl).total_seconds()
            self.traning_df.loc[indexDateTime,f" {Sesion} - Var Segs POI2-Close"] = (Tc-Th).total_seconds()
            #No Derivado de Fecha
            self.traning_df.loc[indexDateTime,f" {Sesion} - Var Pips Open-POI1"] = ((Pl-Po)*10000)  # -
            self.traning_df.loc[indexDateTime,f" {Sesion} - Var Pips POI1-POI2"] = ((Ph-Pl)*10000)  # +
            self.traning_df.loc[indexDateTime,f" {Sesion} - Var Pips POI2-Close"] = ((Pc-Ph)*10000) # -

        else: # Primer POI = High
            #Derivado de Fecha
            self.traning_df.loc[indexDateTime,f" {Sesion} - Var Segs Open-POI1"] = (Th-To).total_seconds()
            self.traning_df.loc[indexDateTime,f" {Sesion} - Var Segs POI1-POI2"] = (Tl-Th).total_seconds()
            self.traning_df.loc[indexDateTime,f" {Sesion} - Var Segs POI2-Close"] = (Tc-Tl).total_seconds()
            #No Derivado de Fecha
            self.traning_df.loc[indexDateTime,f" {Sesion} - Var Pips Open-POI1"] = ((Ph-Po)*10000)  # +
            self.traning_df.loc[indexDateTime,f" {Sesion} - Var Pips POI1-POI2"] = ((Pl-Ph)*10000)  # -
            self.traning_df.loc[indexDateTime,f" {Sesion} - Var Pips POI2-Close"] = ((Pc-Pl)*10000) # +




  
    def create_sesions_columns (self, START, indexDateTime):
        P1=18
       
        S1=7
        S2=4
        S3=6
        S4=7

        if START.hour == P1:

            # Sidney para para raul
            self.POIset(START,S1,"Sidney", indexDateTime)
            START=START+timedelta(hours=S1)

            # Tokio para para raul
            self.POIset(START,S2,"Tokio", indexDateTime)
            START=START+timedelta(hours=S2)

            # Londres para raul
            self.POIset(START,S3,"Londres", indexDateTime)
            START=START+timedelta(hours=S3)

            # NY para para raul
            self.POIset(START,S4,"Ny", indexDateTime)
            START=START+timedelta(hours=S4)
            
        else:
            raise Exception(f"Hour datatime not correct, must be {P1}")


    


        
    


    def save_data(self,path,dataframe):
        pd.to_csv(path)
        print(f"saved at {path}")

 
    def __str__(self):
        return str(self.df)




class Ticks:
    def __init__(self,Path_file,Sep="\t"):
        self.ticks=pd.read_csv(Path_file,sep=Sep)
        self.ticks["DateTime"]=self.ticks["<DATE>"]+" "+self.ticks["<TIME>"]
        self.ticks["<DATE>"]=pd.to_datetime(self.ticks["DateTime"])
        self.ticks=self.ticks.drop(["DateTime","<TIME>","<LAST>","<VOLUME>"],axis=1)
    
    def __str__(self):
        return str(self.ticks)