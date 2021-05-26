import numpy as np


def _op_mean(df, column_name):
    return np.mean(df[column_name])


def _op_median(df, column_name):
    return np.median(df[column_name])