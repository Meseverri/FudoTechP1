import pandas as pd
import numpy as np
from datetime import timedelta,datetime
import math
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

        H1=POI_sample_set[" High"].max()
        H0=POI_sample_set[" Low"].min()

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
    

class RN_study:



    def __init__(self,path="", sep=","):
       
        self.df = pd.read_csv(path, sep=sep)
        self.df["Date"]=pd.to_datetime(self.df["Date"])
        self.df.drop([" Time", " High", " Low", " Volume", " Last"],axis=1, inplace=True)
        self.df = self.df.groupby("Date").agg({
                        ' Open': 'first',
                        ' BidVolume': 'sum',
                        ' AskVolume': 'sum',
                        ' NumberOfTrades': 'sum'
        })
        self.df[" week"] = [get_week(x.day) for x in self.df.index]
        self.df[" week_day"] = [x.weekday() for x in self.df.index]

        

        print(self.df.iloc[15:35,:])

  
    


        
    


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