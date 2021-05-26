import pytest
import pandas as pd

from edatk._single_variable._summary_statistics import _op_mean, _op_median


def _get_test_df():
    SAMPLE_LIST = [5.1,4.9,4.7,4.6,5.0]
    return pd.DataFrame(SAMPLE_LIST, columns=['metric'])


def test_mean():
    assert round(_op_mean(_get_test_df(),'metric'),2) == 4.86


def test_median():
    assert round(_op_median(_get_test_df(),'metric'),2) == 4.9