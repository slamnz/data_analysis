# -*- coding: utf-8 -*-
"""
Created on Wed May 31 11:32:47 2017

@author: Sunny Lam
"""

# === Numeric Analysis === #

from seaborn import distplot, boxplot, countplot, set_style,despine, axes_style
from matplotlib.pyplot import subplot, show
from IPython.display import display
from pandas import DataFrame

def numeric_analysis(series):
    
    no_nulls = series.dropna()
    
    with axes_style({"axes.grid": False}):
        
        cell_1 = subplot(211)
        dp = distplot(no_nulls, kde=False)
        dp.set_xlabel("",visible=False)
        dp.set_yticklabels(dp.get_yticklabels(),visible=False)
        despine(left = True)

        cell_2 = subplot(212, sharex=cell_1)
        boxplot(no_nulls)
        despine(left=True)
    
    show()
    
    display(DataFrame(series.describe().round(2)).T)
    
# === Category Analysis === #

def category_analysis(series):
    
    set_style("whitegrid")
    
    with axes_style({'axes.grid': False}):
        cp = countplot(series)
        cp.set_title(cp.get_xlabel())
        cp.set_xlabel("",visible=False)
        despine()
    
    show()
    display(DataFrame(series.value_counts().apply(lambda x: x / len(series) * 100).round(2)).T)