from backtesting import Backtest , Strategy
from backtesting.test import GOOG

Backtest(GOOG,SmaCross).run()
#Tutorial https://youtu.be/e4ytbIm2Xg0 example

class RsiOscilator(Strategy):
    def init(self):
        pass
    #read the next candel
    def next(self):
        pass
