import pandas as pd
from typing import Optional

from edatk._single_variable._auto_eda_single_variable import _auto_eda_columns
from edatk._multi_variable._auto_eda_multi_variable import _auto_eda_mutli_variable
from edatk._single_variable._cardinality_reduction import _add_low_cardinality_target_column
from edatk._core import _check_for_pandas_df
import edatk._html_report._report_builder as html_build


def auto_eda(
        df: pd.DataFrame, 
        column_list: Optional[list[str]] = None, 
        target_column: Optional[str] = None, 
        target_low_cardinality_visuals: int = 3, 
        save_path: Optional[str] = None, 
        ignore_errors: bool = True, 
        show_chart: bool = True):
    """Run auto eda on a dataframe

    Args:
        df (pd.DataFrame): input dataframe
        column_list (list, optional): List of columns, if none runs for all. Defaults to None.
        target_column (str, optional): Column name string of target. If none runs pair plots for all, otherwise runs only against target. Defaults to None.
        target_low_cardinality_visuals (int): Cardinality of additional target column (if specified) to be added to visualizations where appropriate. Defaults to 3.
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

    # Grab column list if not passed
    if column_list is None:
        column_list = list(df2.columns)

    # Add new target column for large cardinality
    if target_column is not None:

        # Add an additional target column that is low cardinality for visualization
        _add_low_cardinality_target_column(df=df2, target_column=target_column, desired_cardinality=target_low_cardinality_visuals)
            
        # Check that target is in column list
        if target_column not in column_list:
            column_list.append(target_column)

    # Run single column to console and bind to html if needed
    _auto_eda_columns(df=df2, column_list=column_list, html_report=html_report, ignore_errors=ignore_errors, show_chart=show_chart)

    # Run multi column
    df2.head()
    _auto_eda_mutli_variable(df=df2, column_list=column_list, target_column=target_column, html_report=html_report, ignore_errors=ignore_errors, show_chart=show_chart)

    # Save off final html template
    if html_report:
        html_report.build_final_template()

    # Clean up
    del df2
