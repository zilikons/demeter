import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from params import URBAN_ATLAS_LAND_USE
import seaborn as sns
from params import FEATURE_COLUMN_NAMES
import numpy as np
from sklearn.preprocessing import OneHotEncoder

#Function 1: Dissolving (=groupby) the data
def dissolve_and_reset_index(data, by):
    data_group_geometry = data.dissolve(by=by)
    data_group_geometry = data_group_geometry.reset_index()
    return data_group_geometry


#Histplot single feature
def feature_histogram(data, feature_column_name1,feature_column_name2):
    feature_name1 = FEATURE_COLUMN_NAMES[feature_column_name1]
    feature_name2 = FEATURE_COLUMN_NAMES[feature_column_name2]
    plt.figure(figsize=(14, 4))

    plt.title(feature_column_name1)
    sns.histplot(np.log1p(data[FEATURE_COLUMN_NAMES[feature_column_name1]]), kde=True);

#Histplot with two features side-by-side
def feature_histogram_side_by_side(data, feature_column_name1,feature_column_name2):
    feature_name1 = FEATURE_COLUMN_NAMES[feature_column_name1]
    feature_name2 = FEATURE_COLUMN_NAMES[feature_column_name2]
    plt.figure(figsize=(14, 4))

    plt.subplot(1, 2, 1)
    plt.title(feature_column_name1)
    sns.histplot(np.log1p(data[FEATURE_COLUMN_NAMES[feature_column_name1]]), kde=True);

    plt.subplot(1, 2, 2)
    plt.title(feature_column_name2)
    sns.histplot(np.log1p(data[FEATURE_COLUMN_NAMES[feature_column_name2]]), kde=True);
    fig = plt.gcf()
    return fig
#plotting feature map
def plot_feature(data, feature):
    fig, ax = plt.subplots(1, 1)
    plt.title(f'{feature} Overview')
    plt.xticks([])
    plt.yticks([])
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.1)
    data.plot(column=feature, ax=ax, legend=True, cax=cax, legend_kwds={'label': feature})
    plt.show()

#plotting scatterplot of feature given by land use code, and target y Occurences
def plot_scatter_by_code(data, land_use_code_int):
    land_use_name = URBAN_ATLAS_LAND_USE[land_use_code_int]
    data_subset = data[data['land_use_code'] == str(land_use_code_int)]
    data_sorted = data_subset.sort_values(by=['y'])
    ax = data_sorted.plot(kind='scatter', x='land_use_code', y='y', xlabel=land_use_name, ylabel='Occurrences')
    plt.title(f'Correlation with {land_use_name}')
    for label in ax.get_xticklabels(which='major'):
        label.set(rotation=35, horizontalalignment='right')
    plt.show()

#alternatively to plot_scatter_by_code, the scatterplot is plotted by land use name
def plot_scatter_by_name(data, land_use_name):
    land_use_code_int = [key for key, value in URBAN_ATLAS_LAND_USE.items() if value == land_use_name][0]
    data_subset = data[data['land_use_code'] == str(land_use_code_int)]
    data_sorted = data_subset.sort_values(by=['y'])
    fig, ax = plt.subplots()
    ax.scatter(x=data_sorted['land_use_code'], y=data_sorted['y'])
    ax.set(xlabel=land_use_name, ylabel='Occurrences')
    ax.set_title(f'Correlation Land Use ({land_use_name})')
    for label in ax.get_xticklabels(which='major'):
        label.set(rotation=35, horizontalalignment='right')
    plt.show()


#correlation of specific feature with target
def plot_correlation(data, feature_column_name, cmap='coolwarm'):
    corr_group = data.corr()[[feature_column_name]]
    sns.set(style='white')
    fig, ax = plt.subplots(figsize=(10,10))
    sns.heatmap(corr_group, cmap=cmap, annot=True, fmt='.2f', linewidths=.5, ax=ax)
    ax.set_title(f'Correlation of {feature_column_name}')
    return fig
