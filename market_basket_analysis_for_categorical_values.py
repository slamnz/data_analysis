# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 12:57:00 2017

@author: Sunny Lam
"""

outcomes = ["work_interfere", "treatment"]
predictors = [category for category in categories if category not in outcomes]
In [15]:
tuples = {}
for var in outcomes + predictors:
    category_values = {}
    for val in data[var].unique():category_values[val] = (var,val)
    tuples[var] = category_values   
In [16]:
def get_count(data, tuples):
    ordered_categories = [category for (category, value) in tuples]
    counts = data.groupby(ordered_categories).count()[data.columns[0]]
    count = counts
    for tup in tuples: count = count[tup[1]]
    return count

def get_support(data, tuples):
    support = get_count(data,tuples)
    return support/len(data)

def get_confidence(data, predictors, outcomes):
    numerator = get_support(data,predictors+outcomes)
    denominator = get_support(data, predictors)
    return numerator / denominator

def get_lift(data,tuples):
    numerator = get_support(data,tuples)
    denominator = 1 
    for tup in tuples: denominator *= get_support(data,[tup])
    return numerator /denominator
In [17]:
# X => Y

from itertools import combinations

rows = []

for p in predictors:
    for p_value in data[p].unique():
        for o in outcomes:
            for o_value in data[o].unique():
                predictor = tuples[p][p_value]
                outcome = tuples[o][o_value]
                try:
                    row = {"Predictor" : p + "/" + p_value, 
                           "Outcome" : o + "/" + o_value, 
                           "Support": get_support(data, [predictor,outcome]),
                           "Confidence": get_confidence(data,[predictor],[outcome]),
                           "Lift": get_lift(data,[predictor,outcome])}
                    rows += [row]
                except:
                    pass
In [18]:
from pandas import DataFrame
table = DataFrame(rows, columns=["Predictor","Outcome","Support","Confidence","Lift"])