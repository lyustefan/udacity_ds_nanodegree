
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

def plot_missing(df):

    fig, ax = plt.subplots(figsize = (15,8))
    miss = df.apply(lambda x: x.isnull().sum() / len(df)).sort_values(ascending = False)

    # Formatting ax
    ax = sns.barplot(y = miss.values, x = miss.index)

    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.2%'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    xytext = (0, 10), 
                    textcoords = 'offset points')

    ax.set_xticklabels(ax.get_xticklabels(), rotation = 45)
    ax.set_ylim(0,1)  
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])
    ax.set_ylabel('Percentage of Missing')

    # formatting ax2
    ax2 = ax.twinx()
    ax2.set_ylim(0, len(df))
    ax2.set_ylabel('Count of Missing')

    # Use a MultipleLocator to ensure a tick spacing of 10
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(10000))
    ax2.set_yticklabels(['{:,.0f}K'.format(x/1000) for x in ax2.get_yticks()])

    plt.title('Missing Value')
    fig.tight_layout()
    sns.despine()
    plt.show()

def plot_corr(df, figsize):
    '''
    This function plots the correlation plot between numeric variables
    
    '''
    corr = df.select_dtypes(['float64', 'int64']).corr()
    
    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype = np.bool)
    
    mask[np.triu_indices_from(mask)] = True
    
    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize = figsize)
    
    # Generate a custome diverging colormap
    cmap = sns.diverging_palette(220, 10 , as_cmap = True)
    
    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask = mask, cmap = cmap, vmax = 1, vmin = -1, center = 0,
               square = True, linewidths = 0.5, cbar_kws = {'shrink':0.5})
    
    plt.title('Correlation Plot of Numeric Variables')
    
    sns.despine()
    plt.tight_layout()
    plt.show()