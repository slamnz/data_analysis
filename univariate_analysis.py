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

from seaborn import countplot, set_style, color_palette, despine
from matplotlib.pyplot import show
from IPython.display import display
from pandas import DataFrame

def category_analysis(series):
    
    set_style("whitegrid")
    set_style({'axes.grid': False})
        
    if series.unique().size > 10:
        ax = countplot(data=series, palette=color_palette("colorblind"))
        ax.set_title(ax.get_ylabel())
        ax.set_ylabel("",visible=False)
        
        last_tick = int(round(ax.get_xticks()[-1]/len(series),1) * 10) + 1
        ax.set_xticks([i * (len(series) * 0.1) for i in range(0,last_tick)])
        ax.set_xticklabels(["{:.0f}%".format((tick / len(series)) * 100) for tick in ax.get_xticks()])
        
        despine(left=True)
        show()
        display(DataFrame(series.value_counts()).T)
    
    else:
    
        ax = countplot(series, palette=color_palette("colorblind"))
        
        last_tick = int(round(ax.get_xticks()[-1]/len(series),1) * 10) + 1
        ax.set_yticks([i * (len(series) * 0.1) for i in range(0,last_tick)])
        ax.set_yticklabels(["{:.0f}%".format((tick / len(series)) * 100) for tick in ax.get_yticks()])
        
        maximum_yticklabel_length = max([len(str(x)) for x in series.unique()])
        
        if maximum_yticklabel_length in range (5,7):
            ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
        elif maximum_yticklabel_length > 6:
            ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
            
        ax.set_title(ax.get_xlabel())
        ax.set_xlabel("",visible=False)
            
        despine(left=True)
    
    show()
    
    display(DataFrame(series.value_counts()).T)