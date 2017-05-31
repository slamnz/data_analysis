# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 10:46:37 2017

@author: Sunny Lam
"""

from seaborn import barplot

def percentplot(data,category)
    ax = barplot(data=data, x=category, y=category, estimator=lambda x: len(x)/len(data) * 100)
    ax.set_ylabel("Percentage")
    ax.set_yticklabels([str(int(a)) + "%" for a in ax.get_yticks()])
    return ax