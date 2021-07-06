import seaborn as sns
import numpy as np
import pandas as pd
from pandas.api.types import is_bool_dtype
import matplotlib.ticker as mtick
import math

from edatk._core import _rotate_x_axis_labels, _integer_y_axis_format
from edatk._single_variable._summary_statistics import _op_missing_rows as na_rows
from edatk._single_variable._summary_statistics import _get_theoritical_distributions


def _split_top_others(s, topn=10, na_row_count=None):
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
        'Other': other_values_sum
    }
    other_value_series = pd.Series(other_value_dict)

    # Add in NA rows if requested
    missing_value_dict = {
        'Missing': na_row_count
    }
    missing_value_series = pd.Series(missing_value_dict)

    # Return combined values series
    return pd.concat([top_values, other_value_series, missing_value_series])


def _get_percentage_from_counts(vcounts):
    """Given value counts, get the corresponding percentages.

    Args:
        vcounts (pandas series): pandas value counts

    Returns:
        pandas series: value counts as a percentage of total
    """
    return vcounts / np.sum(vcounts)


def _annotate_bars(ax, colors, force_int=False):
    """For a bar chart drawn to ax, annotate labels at top of bar with same colors.

    Args:
        ax (matplotlib ax object): ax object with bars to be annotated
        colors (list): list of color strings
        force_int (bool): force lables to round to nearest int or not
    """
    for p, c in zip(ax.patches, colors):
        if force_int:
            format_str = int(round(p.get_height(),0))
        else:
            format_str = "%.2f" % p.get_height()
        ax.annotate(format_str, (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=11, color=c, xytext=(0, 20),
                    textcoords='offset points')


def _plot_distributions(df, column_name, ax):
    """Return boxplot ax given a dataframe and column name string. Ignores NAs.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized
        ax (matplotlib ax object): ax to plot chart on
    """
    if not is_bool_dtype(df[column_name]):
        # Filter out nas and grab correct column
        filtered_col = df[column_name].dropna()

        # Plot and clean up chart formatting
        ct = sns.boxplot(x=filtered_col, ax=ax)
        ct.set_title(f'{column_name} Box Plot')
        ct.set(xlabel=None)


def _plot_categorical_counts(df, column_name, ax):
    """Plot bars with counts of the various values in the column.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized
        ax (matplotlib ax object): ax to plot chart on
    """

    # Filter out nas and translate topn
    na_row_count = na_rows(df, column_name)
    filtered_col = df[column_name].dropna()
    summarized_col = _split_top_others(filtered_col, topn=5, na_row_count=na_row_count)

    # Change y axis to integer format and pad
    ymax = math.ceil(np.max(summarized_col) * 1.25)
    ymin = math.floor(np.min(summarized_col))
    if ymin > 0.0:
        ymin = 0
    ax.set_ylim(ymin, ymax)
    _integer_y_axis_format(ax)
    
    # Fix x axis labels from overlapping
    _rotate_x_axis_labels(ax)
    
    # Calc color palette
    cpalette = ['tab:blue' if x == 'Other' else 'red' if x == 'Missing' else 'grey' for x in summarized_col.index]

    # Plot chart
    sns.barplot(x=summarized_col.index, y=summarized_col, ax=ax, palette=cpalette).set_title(f'{column_name} Count Plot')

    # Add labels
    _annotate_bars(ax, cpalette, force_int=True)


def _plot_simple_bar(s, title, ax):
    """Plot simple bars from series.

    Args:
        s (pandas series): input dataframe
        title (string): title to add to plot
        ax (matplotlib ax object): ax to plot chart on
    """

    # Filter out nas
    summarized_col = s.dropna()

    # Y axis pad
    ymax = np.max(summarized_col) * 1.25
    ymin = math.floor(np.min(summarized_col))
    if ymin > 0.0:
        ymin = 0
    ax.set_ylim(ymin, ymax)
    
    # Fix x axis labels from overlapping
    _rotate_x_axis_labels(ax)

    # Calc color pallete
    cpalette = ['grey' for x in summarized_col]
    
    # Plot chart
    ct = sns.barplot(x=summarized_col.index, y=summarized_col, ax=ax, palette=cpalette)
    ct.set_title(title)
    ct.set(xlabel=None)
    ct.set(ylabel=None)

    # Add labels
    _annotate_bars(ax, cpalette, force_int=False)


def _plot_categorical_percent_counts(df, column_name, ax):
    """Plot bars with count percents of the various values in the column.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized
        ax (matplotlib ax object): ax to plot chart on
    """

    # Filter out nas and translate to topn percent of total counts
    na_row_count = na_rows(df, column_name)
    filtered_col = df[column_name].dropna()
    summarized_col = _get_percentage_from_counts(_split_top_others(filtered_col, topn=5, na_row_count=na_row_count))
    summarized_col *= 100.0

    # Change y axis to percent format
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    # Pad y axis
    ymax = math.ceil(np.max(summarized_col) * 1.25)
    ymin = math.floor(np.min(summarized_col))
    if ymin > 0.0:
        ymin = 0
    ax.set_ylim(ymin, ymax)
    
    # Fix x axis labels from overlapping
    _rotate_x_axis_labels(ax)
    
    # Calc color palette
    cpalette = ['tab:blue' if x == 'Other' else 'red' if x == 'Missing' else 'grey' for x in summarized_col.index]

    # Plot chart
    sns.barplot(x=summarized_col.index, y=summarized_col, ax=ax, palette=cpalette).set_title(f'{column_name} % Count Plot')

    # Add labels
    _annotate_bars(ax, cpalette)


def _plot_histogram(df, column_name, ax):
    """Plot histogram.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized
        ax (matplotlib ax object): ax to plot chart on
    """

    # Plot chart and clean up formatting
    ct = sns.histplot(data=df[column_name].dropna(), kde=True, ax=ax)
    ct.set_title(f'{column_name} Histogram')
    ct.set(xlabel=None)
    ct.set(ylabel=None)


def _plot_distribution_overlay(df, column_name, ax, best_only=False):
    """Plot distribution overlay.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized
        ax (matplotlib ax object): ax to plot chart on
        best_only (bool): whether to plot the best fit only or all distributions
    """

    # Calculate various lines for distribution
    all_distributions, rankings = _get_theoritical_distributions(df, column_name)

    # filter to just one if needed
    if best_only:
        best_text = rankings['distribution_type'].values[0]
        best_idx = all_distributions['distribution_type'] == best_text
        default_idx = all_distributions['distribution_type'] == 'original data'
        all_distributions = all_distributions[best_idx | default_idx]

    # Plot chart and clean up formatting
    ct = sns.lineplot(data=all_distributions, x=column_name, y='distribution', hue='distribution_type', ax=ax)
    if best_only:
        ct.set_title(f'{column_name} Closest Distribution')
    else:
        ct.set_title(f'{column_name} Distribution Overlays')
    ct.set(xlabel=None)
    ct.set(ylabel=None)


def _plot_ecdf(df, column_name, ax):
    """Plot ecdf.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized
        ax (matplotlib ax object): ax to plot chart on
    """
    ct = sns.ecdfplot(data=df[column_name].dropna(), ax=ax)
    ct.set_title(f'{column_name} ECDF')
    ct.set(xlabel=None)
    ct.set(ylabel=None)


def _plot_swarm(df, column_name, ax):
    """Plot swarmplot.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized
        ax (matplotlib ax object): ax to plot chart on
    """
    # Sampling
    s = df[column_name].dropna()
    max_sample = 1000
    if len(s) <= max_sample:
        max_sample = len(df)
        sample_string = ''
        t=s
    else:
        t = s.sample(n=max_sample, random_state=42)
        sample_string = f' {max_sample} max sample'

    # Plot chart and clean up formatting
    ct = sns.swarmplot(y=t, ax=ax)
    ct.set_title(f'{column_name} Swarmplot{sample_string}')
    ct.set(xlabel=None)
    ct.set(ylabel=None)