import pytest
import pandas as pd
import seaborn as sns

import warnings
warnings.filterwarnings("ignore", module = "matplotlib\..*" )
warnings.filterwarnings("ignore", module = "seaborn\..*" )
warnings.filterwarnings("ignore", message="FixedFormatter should only be used together with FixedLocator")

import edatk._single_variable._summary_statistics as sst
from edatk._auto_eda import auto_eda

def _get_sns_test_datasets(small_list=False):
    if small_list:
        return [sns.load_dataset('iris'), sns.load_dataset('diamonds'), sns.load_dataset('titanic')]
    else:
        return [sns.load_dataset(ds_name) for ds_name in sns.get_dataset_names()]

def _get_test_df():
    SAMPLE_LIST = [5.1,4.9,4.7,4.6,5.0, None]
    SAMPLE_CAT = ['a', 'b', 'c', 'd', 'e', 'a']
    return pd.DataFrame(list(zip(SAMPLE_LIST,SAMPLE_CAT)), columns=['metric', 'category'])


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


def test_distinct_count():
    assert int(sst._op_distinct_count(_get_test_df(), 'category')) == 5


def test_data_type():
    assert sst._op_get_column_data_type(_get_test_df(), 'category') == 'string'
    assert sst._op_get_column_data_type(_get_test_df(), 'metric') == 'numeric'


def test_auto_column_text_eda():
    try:
        auto_eda(_get_test_df())
    except Exception as e:
        pytest.fail(f'Unexpected error...')
    try:
        auto_eda(_get_test_df(), 'metric')
    except Exception as e:
        pytest.fail(f'Unexpected error...')
    try:
        auto_eda(_get_test_df(), ['metric', 'category'])
    except Exception as e:
        pytest.fail(f'Unexpected error...')


def test_sns_datasets():
    ds_list = _get_sns_test_datasets()
    for ds in ds_list:
        auto_eda(ds, ignore_errors=False, show_chart=False)