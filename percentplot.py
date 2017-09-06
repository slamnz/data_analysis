# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 10:46:37 2017

@author: Sunny Lam
"""

from seaborn import countplot, color_palette, despine

def percentplot(series):
        
    if series.unique().size > 10:
        ax = countplot(data=series, palette=color_palette("colorblind"))
        ax.set_title(ax.get_ylabel())
        ax.set_ylabel("",visible=False)
        
        last_tick = int(round(ax.get_xticks()[-1]/len(series),1) * 10) + 1
        ax.set_xticks([i * (len(series) * 0.1) for i in range(0,last_tick)])
        ax.set_xticklabels(["{:.0f}%".format((tick / len(series)) * 100) for tick in ax.get_xticks()])
        
        despine(left=True)
    
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
        
    return ax