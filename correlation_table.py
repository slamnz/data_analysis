# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 21:31:10 2017

@author: Sunny Lam
"""

data = ""
numerical_features = ""

from scipy.stats import pearsonr,spearmanr,kendalltau
from itertools import combinations

rows_list = []

for x1,x2 in combinations(numerical_features,2):
    
    row = {}
    row["Variable A"] = x1 
    row["Variable B"] = x2
    
    pearson = pearsonr(data[x1],data[x2])
    row["Pearson"] = pearson[0]
    row["Pearson's p-value"] = pearson[1]
    
    spearman = spearmanr(data[x1],data[x2])
    row["Spearman"] = spearman[0]
    row["Spearman's p-value"] = spearman[1]
    
    kendall = kendalltau(data[x1],data[x2])
    row["Kendall"] = kendall[0]
    row["Kendall's p-value"] = kendall[1]
    
    rows_list.append(row)

ordered_columns = ["Variable A", "Variable B", "Pearson", "Pearson's p-value", "Spearman", "Spearman's p-value", "Kendall", "Kendall's p-value"]

from pandas import DataFrame

correlation_table = DataFrame(columns="ordered_columns", data=rows_list)

from IPython.display import display

display(correlation_table.sort("Pearson", ascending=False).round(2))

target_filter = (correlation_table["Variable B"] == target) | (correlation_table["Variable A"] == target)

display(correlation_table.sort("Pearson", ascending=False).round(2))
