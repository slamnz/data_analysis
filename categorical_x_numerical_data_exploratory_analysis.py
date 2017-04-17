# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 14:30:42 2017

@author: Sunny Lam
"""

def get_samples(data, category, feature):
    samples = {}
    for c in data[category].unique():
        key = category + "_" + str(c)
        series = data[data[category] == c][feature]
        samples[key] = series.rename(str(c))
    return samples

def display_categorical_and_numerical_analysis(data, feature, category):
    
    from seaborn import pointplot, boxplot, cubehelix_palette, set_style, kdeplot
    from matplotlib.pyplot import show, figure, rc_context, subplot

    chosen_palette = cubehelix_palette(rot = 3)
    set_style("whitegrid")

    fig = figure(figsize=(12.5,12.5))
    fig.suptitle(feature)

    order = data.groupby(category)[feature].mean().sort_values(ascending=False).index
    
    with rc_context({'lines.linewidth': 0.8}):
        
        subplot(221)
        point_plot = pointplot(x=category, y=feature, order=order, data=data, capsize=.14, color = chosen_palette[5])
        point_plot.set_ylabel(feature)
        point_plot.set_xlabel("")
        point_plot.set_xticklabels(point_plot.get_xticklabels(),rotation=30)

        subplot(222)
        
        box_plot = boxplot(x=category, y=feature, order=order, palette = chosen_palette, data=data)
        box_plot.set_ylabel(feature)
        box_plot.set_xlabel("")
        box_plot.set_xticklabels(box_plot.get_xticklabels(),rotation=30)

        samples = get_samples(data, category,feature)
        subplot(223)
        for key in samples.keys():
            kde_plot = kdeplot(samples[key], shade=True)
            
        #
        
        from seaborn import heatmap,diverging_palette
        from matplotlib import colors
        from numpy import float32
        from scipy.stats import ttest_ind
        from pandas import DataFrame

        subplot(224)

        p = diverging_palette(10, 220, sep=80, n=10)
        myColors = [p[4], p[1]]
        cmap = colors.LinearSegmentedColormap.from_list('Custom', myColors, len(myColors))
        
        p_value_table = DataFrame(index = samples.keys(), columns = samples.keys())
        
        from scipy.stats import ttest_ind

        def is_statistically_significant(p):

            if p < 0.05:
                return 1
            else:
                return 0

        from itertools import permutations
        
        for c1,c2 in permutations(samples.keys(),2):
                    
            t,p = ttest_ind(samples[c1],samples[c2])
            p_value_table[c1][c2] = is_statistically_significant(p)
            
        heat_map = heatmap(p_value_table.fillna(float32(None)), linewidths=2, cmap=cmap, cbar=False, square=True)
        cbar = heat_map.figure.colorbar(heat_map.collections[0])
        cbar.set_ticks([1, 0])
        cbar.set_ticklabels(["p < 0.05", "p >= 0.05"])
        
    show()
    
    #
    
    from scipy.stats import f_oneway

    keys = iter(samples.keys())
    
    f, p = f_oneway(samples[next(keys)],
                    samples[next(keys)],
                    samples[next(keys)],
                    samples[next(keys)],
                    samples[next(keys)],
                    samples[next(keys)])
    from IPython.display import display
    display(DataFrame(data = {feature:{"F score":f,"p-value":p}}).round(2).T)