# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 21:31:10 2017

@author: Sunny Lam
"""

data = ""
target = ""

kendall = data.corr("kendall")
pearson = data.corr("pearson")
spearman = data.corr("spearman")

from pandas import DataFrame

correlation_table = DataFrame()
correlation_table["kendall"] = kendall[target]
correlation_table["pearson"] = pearson[target]
correlation_table["spearman"] = spearman[target]

from IPython.display import display

display(correlation_table.sort_values("pearson", ascending=False).round(2))