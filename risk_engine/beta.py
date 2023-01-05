from risk_engine.risk import RiskModel as re

class Beta:

    def __init__(self, ticker):
        self.ticker = ticker
        self.risk = re(self.ticker,"2019-12-06", "1d" )


    def coveriance(self):

    def variance(self):
