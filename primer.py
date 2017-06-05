# -*- coding: utf-8 -*-
"""
Created on Mon May 15 23:03:09 2017

@author: Sunny Lam
"""

def get_feature_lists_by_dtype(data):
    output = {}
    for f in data.columns:
        dtype = str(data[f].dtype)
        if dtype not in output.keys(): output[dtype] = [f]
        else: output[dtype] += [f]
    return output

def show_uniques(data,features):
    for f in features:
        if len(data[f].unique()) < 30:
            print("%s: count(%s) %s" % (f,len(data[f].unique()),data[f].unique()))
        else:
            print("%s: count(%s/%s) %s" % (f,len(data[f].unique()),len(data),data[f].unique()[0:10]))

def show_all_uniques(data):
    features = data.columns.tolist()
    dtypes = get_feature_lists_by_dtype(data,features)
    for key in dtypes.keys():
        print(key + "\n")
        show_uniques(data,dtypes[key])
        print()
