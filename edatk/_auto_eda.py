from edatk._single_variable._auto_eda_single_variable import _auto_eda_columns
from edatk._core import _check_for_pandas_df
import edatk._html_report._report_builder as html_build


def auto_eda(df, column_list=None, save_path=None, ignore_errors=True, show_chart=True):

     # Initiate html file ops if needed
    if save_path:
        html_report = html_build.HTMLReport(save_path)
    else:
        html_report = None

    _check_for_pandas_df(df)
    _auto_eda_columns(df, column_list, html_report, ignore_errors, show_chart)