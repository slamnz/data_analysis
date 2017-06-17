from IPython.display import display
from scipy.stats import kruskal, f_oneway, ttest_ind
from matplotlib import colors, legend, patches
from numpy import float32
from pandas import DataFrame
from seaborn import pointplot, boxplot, cubehelix_palette, set_style, kdeplot, color_palette, heatmap, diverging_palette
from matplotlib.pyplot import show, figure, rc_context, subplot, suptitle, title
from itertools import permutations
from scipy.stats import ttest_ind
from statsmodels.stats.weightstats import ztest

def get_samples(data, category, numeric):
    samples = {}
    for c in data[category].unique():
        key = category + "_" + str(c)
        series = data[data[category] == c][numeric]
        samples[key] = series.rename(str(c))
    return samples

def different_means_test_for_groups(dataframe,category,numeric):
    
    samples = get_samples(dataframe,category,numeric)
    
    if type(samples) == dict:
        output = []
        for key in samples.keys(): output += [samples[key]]
        samples = output
    
    scores = {"kruskal" : kruskal(*samples), 
              "f_oneway" : f_oneway(*samples)}
    
    return DataFrame(scores, index=("statistic","p-value")).T.round(2)

        
    # === === #

def display_multi_category_x_numeric_analysis(data, category, numeric):
    
    data = data[(data[category].notnull()) | (data[numeric].notnull())]

    set_style("whitegrid")
    subcategory_count = len(data[category].unique())
    chosen_palette = color_palette("colorblind",subcategory_count, desat=0.85)

    figure(figsize=(12.5,12.5))
    suptitle(numeric, y=0.94, fontsize=16)

    order = data.groupby(category)[numeric].mean().sort_values(ascending=False).index

    with rc_context({'lines.linewidth': 0.8}):
    
        # === Box Plot === #

        cell_0_1 = subplot(222)
        
        box_plot = boxplot(x=category, y=numeric, order=order, palette = chosen_palette, data=data)
        box_plot.set_xlabel(box_plot.get_xlabel, visible=False)
        box_plot.set_ylabel(numeric + " (mg)", visible=False)
        box_plot.set_xticklabels(box_plot.get_xticklabels())
        
        # === Point Plot === #
        
        subplot(221, sharey=cell_0_1)
        point_plot = pointplot(x=category, y=numeric, order=order, data=data, capsize=.14, color="#383838")
        point_plot.set_ylabel(numeric + " mean")
        point_plot.set_xlabel(point_plot.get_xlabel(), visible=False)
        point_plot.set_xticklabels(point_plot.get_xticklabels())
        
        # === Kernel Density Plot === #
    
        samples = get_samples(data, category, numeric)
        subplot(223)
        i = iter(chosen_palette)
        for key in [label.get_text() for label in box_plot.get_xticklabels()]:
            kde_plot = kdeplot(samples[category + "_" + str(key)], color=next(i), shade=True, linewidth=1.5)
            
        # === Different Means Grid === #
    
        subplot(224)
        
        p_value_table = DataFrame(index = samples.keys(), columns = samples.keys())
        
        for c1,c2 in permutations(samples.keys(),2):
                    
            if (len(samples[c1]) > 30 and len(samples[c2]) > 30):
                z, p = ztest(samples[c1], samples[c2])
            else:
                t, p = ttest_ind(samples[c1],samples[c2])
                
            from random import sample
            
            p_value_table[c1][c2] = round(p,2)
        
        df = p_value_table.fillna(float32(None))
        heat_map = heatmap(df, annot=True, annot_kws={"size" : 24}, linewidths=2, cmap=colors.ListedColormap([diverging_palette(10, 220, sep=80, n=10)[4]]), cbar=False, square=True)
        heatmap(df, mask = df > 0.05, cmap=colors.ListedColormap([diverging_palette(10, 220, sep=80, n=10)[8]]), annot=True, annot_kws={"size" : 24}, linewidths=2, cbar=False, square=True)
        title("DiffMeans p-value Grid", fontsize=14, loc="left")

        p = diverging_palette(10, 220, sep=80, n=10)
        myColors = [p[8],p[4]]
        classes = ['p < 0.05', 'p >= 0.05']
        recs = []
        for i in range(0,len(myColors)):
            recs.append(patches.Rectangle((0,0),1,1,fc=myColors[i]))
        heat_map.legend(recs, classes, loc=4, bbox_to_anchor=(1, 1))
    
        show()
    
        if len(data[category].unique()) > 2:
            display(different_means_test_for_groups(data,category,numeric))