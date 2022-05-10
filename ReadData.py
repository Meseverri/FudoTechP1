import pandas as pd
class candel:
    def __init__(self,date,time,Open,high,low,close,volume,numberOfTrades,bid,ask):
        self.date=date
        self.time=time
        self.Open=Open
        self.high=high
        self.low=low
        self.close=close
        self.volume=volume
        self.numberOfTrades=numberOfTrades
        self.bid=bid
        self.ask=ask

    def __str__(self):
        L=[self.date,self.time,self.Open,self.high,self.low,self.close,self.volume,self.numberOfTrades,self.bid,self.ask]
        txt=""
        count=0
        for i in L:
            if count<len(L)-1:
                txt+=str(i)+","
                count+=1
            else:
                txt+=str(i)

        return(txt)


class candels:
    def __init__(self):
        self.candels=[]
        self.indexColumn=[]

    def readData(self,filename):
        with open(filename,"r") as f:
            count=0
            
            for i in f:
                # i.strip("\n")
                tokens=i.split(',')

                if count==0:
                    tokens[-1]=tokens[-1][:-2]
                    self.indexColumn.append(tokens)
                    count+=1
                else:
                    
                    Candel=candel(tokens[0],tokens[1],float(tokens[2]),float(tokens[3]),float(tokens[4]),float(tokens[5]),int(tokens[6]),int(tokens[7]),int(tokens[8]),int(tokens[9]))
                    self.candels.append(Candel)
                    count+=1
        # self.candels=self.candels[0]
    def to_DataFrame(self):
        candelList=[]
        for i in self.candels:
            c=[i.date,i.time,i.Open,i.high,i.low,i.close,i.volume,i.numberOfTrades,i.bid,i.ask]
            candelList.append(c)

        data=pd.DataFrame(candelList,columns=self.indexColumn)
        return data

    def __str__(self):
        txt="first ten candels:\n"
        txt+="Date,Time, Open, High, Low, Last, Volume, NumberOfTrades, BidVolume, AskVolume\n"
        IndexCount=0
        CandelCount=0
        totalPrints=0       
        while totalPrints<10:  
            totalPrints+=1
            
            for j in self.candels:
                if totalPrints<10:
                    txt+=str(j)+"\n"
                    print(totalPrints)
                    CandelCount+=1
                    totalPrints+=1
                else:
                    txt+=str(j)+"\n"
                    break
                    

        return txt
        


EURUSD=candels()
EURUSD.readData("F.US.EU6H22.scid_BarData.txt")
print(EURUSD.to_DataFrame())