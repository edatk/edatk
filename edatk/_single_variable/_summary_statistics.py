import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype, is_numeric_dtype, is_bool_dtype, is_categorical_dtype
import scipy.stats as stats

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


def _op_skew(df, column_name):
    """Return the scipy skew given a dataframe and column name string. Ignores NAs.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized

    Returns:
        float: skew
    """
    return stats.skew(df[column_name])


def _op_kurtosis(df, column_name):
    """Return the scipy kurtosis given a dataframe and column name string. Ignores NAs.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized

    Returns:
        float: kurtosis
    """
    return stats.kurtosis(df[column_name])


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
    elif is_bool_dtype(df[column_name]):
        return 'bool'
    elif is_numeric_dtype(df[column_name]):
        if _op_distinct_count(df, column_name) <= 10:
            if _op_distinct_count(df, column_name) == 2:
                if _op_min(df, column_name) == 0 and _op_max(df, column_name) == 1:
                    return 'bool'
            return 'numeric-condensed'
        else:
            return 'numeric'
    elif is_categorical_dtype(df[column_name]):
        return 'string'
    else:
        return str(df[column_name].dtype)


def _get_theoritical_distributions(df, column_name):
    """Compare frequencies of column against theoritical freqencies to determine best fit distribution.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be analyzed

    Returns:
        pandas dataframe: dataframe containing distribtion points
        pandas dataframe: dataframe containing distribution and rmse, sorted descending 
    """
    # Init df concat list to hold distributions and remove NAs from column
    df_concat_list = []
    col_wo_nas = df[column_name].dropna()

    # Calculate the number of bins using numpy defaults
    num_bins = len(np.histogram_bin_edges(np.array(col_wo_nas), bins='auto'))

    # Get histogram from dataframe
    y, x = np.histogram(col_wo_nas, bins=num_bins, density=True)
    midpoints = (x[:-1] + x[1:]) / 2.0

    # Add original distribution to the df concat list
    y_df = pd.DataFrame(y, columns=['distribution']).set_index(pd.Series(midpoints))
    y_df['distribution_type'] = 'original data'
    df_concat_list.append(y_df)

    # Loop through distributions
    dist_list = ['norm', 'expon', 'uniform', 'lognorm', 't']
    for dist_name in dist_list:

        # Fit Dist
        dist = getattr(stats.distributions, dist_name)
        dist_parms = dist.fit(col_wo_nas)

        # Generate pdf from modpoints and distribution parms
        pdf = dist.pdf(midpoints, *dist_parms)

        # Add results to df concat list
        df_dist = pd.DataFrame(pdf, columns=['distribution']).set_index(pd.Series(midpoints))
        df_dist['distribution_type'] = dist_name
        df_concat_list.append(df_dist)


    # Combine into one df
    all_distributions = pd.concat(df_concat_list).reset_index().rename(columns={'index': column_name})

    # Split data by orig and distributions
    orig_data_idx = all_distributions['distribution_type'] == 'original data'
    df_orig_data = all_distributions.loc[orig_data_idx, :]
    df_other_data = all_distributions.loc[~orig_data_idx]

    # Calculate sse
    combined_df = pd.merge(df_other_data, df_orig_data, how='left', on=column_name, suffixes=['_dist','_orig'])
    combined_df['squared_errors'] = (combined_df['distribution_dist'] - combined_df['distribution_orig']) ** 2
    df_se = pd.DataFrame(combined_df.groupby(['distribution_type_dist'])['squared_errors'].mean().reset_index())
    df_se['rmse'] = np.sqrt(df_se['squared_errors']) 
    df_se.drop(['squared_errors'], axis=1, inplace=True)
    df_se = df_se.rename(columns={'distribution_type_dist': 'distribution_type'})
    df_se = df_se.sort_values(by='rmse', ascending=True)

    return all_distributions, df_se