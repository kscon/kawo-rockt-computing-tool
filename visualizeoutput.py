""" visualizing script"""

import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np

"""
ts = pd.Series(np.random.randn(1000),index=pd.date_range('1/1/2000', periods=1000))
ts = ts.cumsum()
ts.plot()
plt.show()
"""

def visualize(ck1, ck2,ck3):
    numberofteams = ck1 + ck2 + ck3
    df = pd.DataFrame({'Kawo Dish Distribution': [ck1, ck2 , ck3]}, index=['one team', 'two teams', 'three teams'])
    df.plot.pie(y = "Kawo Dish Distribution",figsize=(6, 6), autopct=lambda p: "{:.0f}".format(np.round((p*numberofteams)/100., 0)))
    #plt.show()
    #fig = df.get_figure()
    plt.savefig("./output/kawodistribution.pdf")
