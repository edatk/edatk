import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype, is_numeric_dtype, is_bool_dtype, is_categorical_dtype


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
    if is_bool_dtype(df[column_name]):
        return None
    else:
        return np.nanquantile(df[column_name],quantile_value)


def _op_distinct_count(df, column_name):
    """Return the distinct count given a dataframe and column name string. Ignores NAs.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized

    Returns:
        int: number of unique values
    """
    return df[column_name].nunique()


def _op_get_column_data_type(df, column_name):
    """Return the data type given a dataframe and column name string.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be analyzed

    Returns:
        string: data type of the column
    """
    if is_string_dtype(df[column_name]):
        return 'string'
    elif is_numeric_dtype(df[column_name]):
        return 'numeric'
    elif is_categorical_dtype(df[column_name]):
        return 'string'
    elif is_bool_dtype(df[column_name]):
        return 'string'
    else:
        return str(df[column_name].dtype)