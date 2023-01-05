import yfinance as yf
from datetime import datetime as dt
import numpy as np
import pandas as pd
from scipy.stats import shapiro as sh


class RiskModel:

    def __init__(self, ticker, end, freq):
        self.prob_dense = 0
        self.data = None
        self.ticker = ticker
        self.end = end
        self.date = "20" + dt.today().strftime('%y-%m-%d')
        self.freq = freq
        self.dist_data = []
        self.std = 0
        self.mean = 0
        self.get_data()
        self.returns()

    def get_data(self) -> None:
        tick = yf.Ticker(str(self.ticker))
        self.data = tick.history(start=self.end, end=self.date, interval=self.freq)
        self.data = pd.DataFrame(self.data)
        self.data = self.data[['Open', 'Dividends']]
        self.data = self.data.dropna()

    def returns(self) -> None:
        '''
        retrieves and saves the ticker data
        '''
        previous = None
        for row in range(len(self.data)):
            if previous is None:
                previous = self.data.iloc[row]['Open']
                continue
            self.dist_data.append(
                ((self.data.iloc[row]['Open'] - previous + self.data.iloc[row]['Dividends']) / previous) * 100)
            previous = self.data.iloc[row]['Open']

    def bottom_five(self):
        '''
        retrieves the returns list and the works out the average returns for the bottom 5%
        :return: 1 float which is the percentage that will be lost
        '''
        rounded = [round(item) for item in self.dist_data]
        if len(self.dist_data) == 0:
            return "Ticker invalid"
        self.mean = sum(self.dist_data) / len(self.dist_data)
        model = np.asarray(rounded)
        self.std = np.std(self.dist_data)
        model = np.sort(model)
        bottom5 = model[:round(model.size * 0.05)]
        return round(np.average(bottom5), 2)

    def norm_dist(self):
        '''
        checks that the returns can be normally distributed and that they can be then be
        :return: 2 floats. 1st represents the 95% confidence, 2nd 99% confidence.
        '''
        value = sh(self.dist_data).pvalue
        if value < 0.05:
            return "Not normally distributed"
        else:
            return round(self.std * -1.65, 2), round(self.std * -2.33, 2)


risk = RiskModel("aapl", "2019-12-06", "1d")
risk.get_data()
risk.returns()
print(risk.bottom_five())
print(risk.norm_dist())