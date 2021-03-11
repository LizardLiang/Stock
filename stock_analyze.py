import numpy as np


class Stock_Analyze:
    def __init__(self):
        self.Heightest = 0
        self.Lowest = 0
        self.breakpoint = []

    def get_Section(self, datas):
        self.Heightest = max(datas)
        self.Lowest = min(datas)

    def get_Hightest(self):
        return self.Hightest

    def get_Lowest(self):
        return self.Lowest

    def set_breakpoint(self, datas):
        self.Heightest = datas[0]
        self.Lowest = datas[1]

        trend = False  # when treand is upward set to true otherwise false
        if datas[0] < datas[1]:
            trend = True
        else:
            trend = False

        pre_data = datas[0]
        for data in datas:
            if trend and data < pre_data:
                trend = False
                self.breakpoint.append(pre_data)
            elif not trend and data > pre_data:
                trend = True
                self.breakpoint.append(pre_data)
            pre_data = data

        return self.breakpoint
