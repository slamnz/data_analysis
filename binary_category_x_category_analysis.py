# -*- coding: utf-8 -*-
"""
Created on Mon May  1 20:33:19 2017

@author: Sunny Lam
"""

def p_value_table(data, category_of_interest, categorical_features):
    
    from scipy.stats import chi2_contingency
    from pandas import crosstab, DataFrame
    
    p_value_table = DataFrame(index = [category_of_interest], columns = (categorical_features))
    
    for c in categorical_features:
    
        crosstable = crosstab(data[c], data[target])
        chi2, p, dof, expected = chi2_contingency(crosstable)
        p_value_table[c][target] = p
    
    p_value_table = p_value_table.T
    p_value_table["p < 0.05"] = p_value_table.apply(lambda x : x < 0.05)
    
    return p_value_table

# ============================================================================

p_value_table.sort_values("Attrition", ascending=False)

print(p_value_table[p_value_table["p < 0.05"] == False].index.tolist())

significant = p_value_table[p_value_table["p < 0.05"] == True].index.tolist()
print(significant)

# ============================================================================

from seaborn import countplot, despine, axes_style, set_style
from matplotlib.pyplot import show,figure,subplot,xticks,suptitle,title, ylabel, xlabel, margins
from numpy import mean

set_style("whitegrid")

def binary_category_x_category_analysis(data, category_of_interest, categorical_features, target):

    with axes_style({'grid.color': "0.95", "lines.color" : "0.95"}):
    
        for c in categorical_features:
    
            order = data[data[category_of_interest] == target][c].value_counts().sort_values(ascending=False).index
    
            fig = figure(figsize=(12,6))
            suptitle(c, fontsize=16)
            margins(0.8)
            subplot(121)
            title(str(target) + " Only")
            cp = countplot(x=c, data=data[data[category_of_interest] == target], order=order, color="yellow", linewidth=0)
            despine(left=True, top=True)
            
            xlabel_char_length = int(mean([len(str(i)) for i in data[c].unique()]))
            
            if(xlabel_char_length in range(7, 15)): 
                xticks(rotation=45)
            elif(xlabel_char_length > 14):
                xticks(rotation=90)
                
            subplot(122)
            title(str(target) + " vs " + str([i for i not in data[category_of_interest].unique()][0]))
            cp = countplot(x=c, hue=category_of_interest, data=data, order=order, palette=["yellow", "silver"], linewidth=0)
            despine(left=True, top=True)
            if(xlabel_char_length in range(7, 15)): 
                xticks(rotation=45)
            elif(xlabel_char_length > 14):
                xticks(rotation=90)
            xlabel(c)
            show()