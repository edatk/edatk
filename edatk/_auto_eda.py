from edatk._single_variable._auto_eda_single_variable import _auto_eda_columns
from edatk._multi_variable._auto_eda_multi_variable import _auto_eda_mutli_variable
from edatk._core import _check_for_pandas_df
import edatk._html_report._report_builder as html_build


def auto_eda(df, column_list=None, save_path=None, ignore_errors=True, show_chart=True):
    """Run auto eda on a dataframe

    Args:
        df (pd.DataFrame): input dataframe
        column_list (list, optional): List of columns, if none runs for all. Defaults to None.
        save_path (str, optional): Directory to save html report to. If none then results printed to console instead. Defaults to None.
        ignore_errors (bool, optional): Ignores errors and runs as much as possible. Defaults to True.
        show_chart (bool, optional): Display charts, likely always want this as True unless testing or working with very large datasets. Defaults to True.
    """
     # Initiate html file ops if needed
    if save_path:
        html_report = html_build.HTMLReport(save_path)
    else:
        html_report = None

    # Error checking
    df2 = df.copy()
    _check_for_pandas_df(df2)

    # Run single column to console and bind to html if needed
    _auto_eda_columns(df2, column_list, html_report, ignore_errors, show_chart)

    # Run multi column
    _auto_eda_mutli_variable(df2, html_report, ignore_errors, show_chart)

    # Save off final html template
    if html_report:
        html_report.build_final_template()

    # Clean up
    del df2
