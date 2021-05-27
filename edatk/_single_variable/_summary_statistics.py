import numpy as np
import pandas as pd


def _op_mean(df, column_name):
    """Return the numpy mean given a dataframe and column name string. Ignores NAs.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized

    Returns:
        float: mean value
    """
    return np.nanmean(df[column_name])


def _op_median(df, column_name):
    """Return the numpy median given a dataframe and column name string. Ignores NAs.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized

    Returns:
        float: median value
    """
    return np.nanmedian(df[column_name])


def _op_rowcount(df, column_name):
    """Return the numpy row shape given a dataframe and column name string.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized

    Returns:
        int: row count
    """
    return np.array(df[column_name]).shape[0]


def _op_min(df, column_name):
    """Return the numpy min given a dataframe and column name string. Ignores NAs.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized

    Returns:
        float: min value
    """
    return np.nanmin(df[column_name])


def _op_max(df, column_name):
    """Return the numpy max given a dataframe and column name string. Ignores NAs.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized

    Returns:
        float: min value
    """
    return np.nanmax(df[column_name])


def _op_variance(df, column_name):
    """Return the numpy varaiance given a dataframe and column name string. Ignores NAs.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized

    Returns:
        float: variance
    """
    return np.nanvar(df[column_name])


def _op_standard_deviation(df, column_name):
    """Return the numpy standard deviation given a dataframe and column name string. Ignores NAs.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized

    Returns:
        float: standard deviation
    """
    return np.nanstd(df[column_name])


def _op_missing_rows(df, column_name):
    """Return the pandas NA values given a dataframe and column name string.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized

    Returns:
        int: number of rows with missing value
    """
    return int(np.sum(pd.isna(df[column_name])))


def _op_quantile(df, column_name, quantile_value=0.75):
    """Return the quantile (0 to 1 percentile) values given a dataframe and column name string. Ignores NAs.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized

    Returns:
        float: quantile cuttoff point
    """
    return np.nanquantile(df[column_name],quantile_value)

