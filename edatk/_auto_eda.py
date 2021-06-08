from edatk._single_variable._auto_eda_single_variable import _auto_eda_columns
from edatk._multi_variable._auto_eda_multi_variable import _auto_eda_mutli_variable
from edatk._core import _check_for_pandas_df
import edatk._html_report._report_builder as html_build


def auto_eda(df, column_list=None, save_path=None, ignore_errors=True, show_chart=True):

     # Initiate html file ops if needed
    if save_path:
        html_report = html_build.HTMLReport(save_path)
    else:
        html_report = None

    # Error checking
    _check_for_pandas_df(df)

    # Run single column to console and bind to html if needed
    _auto_eda_columns(df, column_list, html_report, ignore_errors, show_chart)

    # Run multi column
    _auto_eda_mutli_variable(df, html_report, ignore_errors, show_chart)

    # Save off final html template
    if html_report:
        html_report.build_final_template()