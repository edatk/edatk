import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.ticker as mtick
import math


def _split_top_others(s, topn=10):
    """Split a pandas series by topn and others value counts.

    Args:
        s (pandas series): series containing categories (strings).
        topn (int, optional): number to include as individual items, grouping others into one All Other. Defaults to 10.

    Returns:
        pandas series: pandas series with value counts
    """
    # Edge case of under topn values
    if len(s) <= topn:
        return s.value_counts()

    # Count all values (presort) to be split
    vcounts = s.value_counts()

    # Grab slice for top values
    top_values = vcounts[:topn]
    
    # Build series for other values, with combined counts
    other_values_sum = np.sum(vcounts[topn:].values)
    other_value_dict = {
        'All Other Values': other_values_sum
    }
    other_value_series = pd.Series(other_value_dict)

    # Return combined values series
    return pd.concat([top_values, other_value_series])


def _get_percentage_from_counts(vcounts):
    """Given value counts, get the corresponding percentages.

    Args:
        vcounts (pandas series): pandas value counts

    Returns:
        pandas series: value counts as a percentage of total
    """
    return vcounts / np.sum(vcounts)


def _annotate_bars(ax, colors):
    for p, c in zip(ax.patches, colors):
        ax.annotate("%.2f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=11, color=c, xytext=(0, 20),
                    textcoords='offset points')


def _plot_distributions(df, column_name, ax):
    """Return boxplot ax given a dataframe and column name string. Ignores NAs.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized
        ax (matplotlib ax object): ax to plot chart on
    """

    # Filter out nas and grab correct column
    filtered_col = df[column_name].dropna()

    sns.boxplot(data=filtered_col, ax=ax).set_title(f'{column_name} Box Plot')


def _plot_categorical_counts(df, column_name, ax):
    """Plot bars with counts of the various values in the column.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized
        ax (matplotlib ax object): ax to plot chart on
    """

    # Filter out nas and translate topn
    filtered_col = df[column_name].dropna()
    summarized_col = _split_top_others(filtered_col, topn=2)

    # Change y axis to integer format and pad
    ymax = math.ceil(np.max(summarized_col) * 1.25)
    ax.set_ylim(0, ymax)

    # Calc color palette
    cpalette = ['grey' if x != 'All Other Values' else 'red' for x in summarized_col.index]

    # Plot chart
    sns.barplot(x=summarized_col.index, y=summarized_col, ax=ax, palette=cpalette).set_title(f'{column_name} Count Plot')

    # Add labels
    _annotate_bars(ax, cpalette)


def _plot_categorical_percent_counts(df, column_name, ax):
    """Plot bars with count percents of the various values in the column.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized
        ax (matplotlib ax object): ax to plot chart on
    """

    # Filter out nas and translate to topn percent of total counts
    filtered_col = df[column_name].dropna()
    summarized_col = _get_percentage_from_counts(_split_top_others(filtered_col, topn=2))
    summarized_col *= 100.0

    # Change y axis to percent format
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    # Pad y axis
    ymax = math.ceil(np.max(summarized_col) * 1.25)
    ax.set_ylim(0, ymax)
    
    # Calc color palette
    cpalette = ['grey' if x != 'All Other Values' else 'red' for x in summarized_col.index]

    # Plot chart
    sns.barplot(x=summarized_col.index, y=summarized_col, ax=ax, palette=cpalette).set_title(f'{column_name} % Count Plot')

    # Add labels
    _annotate_bars(ax, cpalette)
