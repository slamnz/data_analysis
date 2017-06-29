# -*- coding: utf-8 -*-
"""
Created on Wed May 31 11:32:47 2017

@author: Sunny Lam
"""

from seaborn import distplot, boxplot, countplot, set_style,despine, axes_style, set_palette, color_palette
from matplotlib.pyplot import subplot, show
from IPython.display import display
from pandas import DataFrame
from scipy.stats import normaltest, skew, skewtest

# === Numeric Analysis === #

def numeric_analysis(series):
    
    no_nulls = series.dropna()
    
    with axes_style({"axes.grid": False}):
        
        cell_1 = subplot(211)
        dp = distplot(no_nulls, kde=True)
        dp.set_xlabel("",visible=False)
        dp.set_yticklabels(dp.get_yticklabels(),visible=False)
        despine(left = True)

        cell_2 = subplot(212, sharex=cell_1)
        boxplot(no_nulls)
        despine(left=True)
    
    show()
    
    display(DataFrame(series.describe().round(2)).T)
    
    display(DataFrame(list(normaltest(series)), columns=["Normal Test"], index=["statistic","p-value"]).T.round(2))
    
    display(DataFrame(list(skewtest(series)), columns=["Skew Test"], index=["statistic","p-value"]).T.round(2))
    
    display(DataFrame([skew(series)], columns=["Skew"], index=[""]).T)

# === Category Analysis === #
    
def category_analysis(series):
    
    set_style("whitegrid")
    set_palette = color_palette("colorblind")
    
    with axes_style({'axes.grid': False}):
        cp = countplot(series)
        cp.set_title(cp.get_xlabel())
        cp.set_xlabel("",visible=False)
        despine()
    
    show()
    display(DataFrame(series.value_counts().apply(lambda x: "{:.2f}%".format(x / len(series) * 100))).T)