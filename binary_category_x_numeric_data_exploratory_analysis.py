# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 16:17:07 2017

@author: Sunny Lam
"""

def display_ttest(data, category, numeric):
    output = {}
    s1 = data[data[category] == data[category].unique()[0]][numeric]
    s2 = data[data[category] == data[category].unique()[1]][numeric]
    from scipy.stats import ttest_ind
    t, p = ttest_ind(s1,s2)
    from IPython.display import display
    from pandas import DataFrame
    display(DataFrame(data=[{"t-test statistic" : t, "p-value" : p}], columns=["t-test statistic", "p-value"], index=[category]))

def display_ztest(data, category, numeric):
    output = {}
    s1 = data[data[category] == data[category].unique()[0]][numeric]
    s2 = data[data[category] == data[category].unique()[1]][numeric]
    from statsmodels.stats.weightstats import ztest
    z, p = ztest(s1,s2)
    from IPython.display import display
    from pandas import DataFrame
    display(DataFrame(data=[{"z-test statistic" : z, "p-value" : p}], columns=["z-test statistic", "p-value"], index=[category]))
    
def display_cxn_analysis(data, category, numeric):
    
    from seaborn import boxplot, kdeplot, set_style
    from matplotlib.pyplot import show, figure, subplots, ylabel, xlabel, subplot, suptitle
    
    pal = {data[category].unique()[0] : "grey", data[category].unique()[1] : "yellow"}

    set_style("whitegrid")
    figure(figsize=(12,5))
    suptitle(numeric + " by " + category)

    # ==============================================
    
    p1 = subplot(2,2,2)
    boxplot(y=category, x=numeric, data=data, orient="h", palette = pal)
    p1.get_xaxis().set_visible(False)

    # ==============================================
    
    p2 = subplot(2,2,4, sharex=p1)
    
    s1 = data[data[category] == data[category].unique()[0]][numeric]
    s1 = s1.rename(data[category].unique()[0])
    kdeplot(s1, shade=True, color = pal[data[category].unique()[0]])
    
    s2 = data[data[category] == data[category].unique()[1]][numeric]
    s2 = s2.rename(data[category].unique()[1])  
    kdeplot(s2, shade=True, color = pal[data[category].unique()[1]])
    
    ylabel("Density Function")
    xlabel(numeric)
    
    # ==============================================
    
    p3 = subplot(1,2,1)
    from seaborn import pointplot
    from matplotlib.pyplot import rc_context

    with rc_context({'lines.linewidth': 0.8}):
        pointplot(x=category, y=numeric, data=data, capsize=.1, color="black", marker="s")
    
    # ==============================================
    
    show()
    
    #display p value
    
    if(data[category].value_counts()[0] > 30 and data[category].value_counts()[1] > 30):
        display_ztest(data,category,numeric)
    else:
        display_ttest(data,category,numeric)
    
    #Means, Standard Deviation, Absolute Distance
    table = data[[category,numeric]]
    
    means = table.groupby(category).mean()
    stds = table.groupby(category).std()
    
    s1_mean = means.loc[1]
    s1_std = stds.loc[1]
    
    s2_mean = means.loc[0]
    s2_std = means.loc[0]
    
    print("%s Mean: %.2f (+/- %.2f)" % (category + " == " + str(means.index[0]),s1_mean, s1_std))
    print("%s Mean : %.2f (+/- %.2f)" % (category + " == " + str(means.index[1]), s2_mean, s2_std))
    print("Absolute Mean Diferrence Distance: %.2f" % abs(s1_mean - s2_mean))
    