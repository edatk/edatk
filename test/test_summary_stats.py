import pytest
import pandas as pd

import edatk._single_variable._summary_statistics as sst
import edatk._single_variable._auto_eda as auto_col


def _get_test_df():
    SAMPLE_LIST = [5.1,4.9,4.7,4.6,5.0, None]
    return pd.DataFrame(SAMPLE_LIST, columns=['metric'])


def test_mean():
    assert round(sst._op_mean(_get_test_df(),'metric'),2) == 4.86


def test_median():
    assert round(sst._op_median(_get_test_df(),'metric'),2) == 4.9


def test_rowcount():
    assert sst._op_rowcount(_get_test_df(),'metric') == 6
    assert type(sst._op_rowcount(_get_test_df(),'metric')) is int


def test_min():
    assert round(sst._op_min(_get_test_df(),'metric'), 2) == 4.6


def test_max():
    assert round(sst._op_max(_get_test_df(),'metric'),2) == 5.1


def test_variance():
    assert round(sst._op_variance(_get_test_df(),'metric'),4) == 0.0344


def test_standard_deviation():
    assert round(sst._op_standard_deviation(_get_test_df(),'metric'),4) == 0.1855


def test_missing():
    assert int(sst._op_missing_rows(_get_test_df(),'metric')) == 1
    assert type(sst._op_missing_rows(_get_test_df(),'metric')) is int


def test_75th_percentile():
    assert round(sst._op_quantile(_get_test_df(),'metric',0.75),4) == 5.0
