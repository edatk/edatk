import seaborn as sns
import numpy as np

def _plot_distributions(df, column_name):
    """Return boxplot ax given a dataframe and column name string. Ignores NAs.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized
    """
    filtered_col = df[column_name].dropna()
    ax = sns.boxplot(data=filtered_col).set_title(f'{column_name} Box Plot')
    return ax