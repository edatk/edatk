from itertools import combinations
from pandas.api.types import is_numeric_dtype

import edatk._core as core
import edatk._multi_variable._visuals as viz


def _get_column_combinations(df, column_list=None, target_column=None):
    """Given a dataframe, get a list of column combinations in tuples

    Args:
        df (pd.DataFrame): dataframe to analyze
        column_list (list[str], optional): List of columns to filter combinations down to
        target_column (str, optional): String name of the target column. If None, returns combinations on all columns

    Returns:
        list[tuple[str, str]]: List of column name tuples
    """
    # Filter down columns if needed
    if column_list:
        col_list_init = list(df.columns.values)
        col_list = [col for col in col_list_init if col in column_list]
    else:
        col_list = list(df.columns.values)

    # Filter list to target column in combination if needed
    init_list = list(combinations(col_list, 2))
    if target_column:
        final_list = []
        for combo in init_list:
            col_a, col_b = combo
            if (col_a == target_column) or (col_b == target_column):
                final_list.append(combo)
    else:
        final_list = init_list
    return final_list


def _bind_chart_function(arg_func, **kwargs):
    """For a given set of two columns, wrap those columns as parms into the plot relationship function

    Args:
        func: func to wrap with normal df and ax inputs
        kwargs: passed along to charting function in addition to df and ax

    Returns:
        function: wrapped inner function
    """
    def inner_func(df, ax):
        return arg_func(df=df, ax=ax, **kwargs)
    return inner_func


def _auto_eda_mutli_variable(df, column_list=None, target_column=None, html_report=None, ignore_errors=True, show_chart=True):
    _relationship_ops = {}
    _heatmap_ops = {}
    
    # Get column combination tuples
    column_combinations = _get_column_combinations(df, column_list=column_list)
    target_only_combinations = _get_column_combinations(df, column_list=column_list, target_column=target_column)
    # Loop through tuples
    for col_set in column_combinations:
        # Parse tuple
        col_a, col_b = col_set
        # Enclose function with tuple (df and ax is populated by caller)
        _relationship_ops[f'{col_a}-{col_b}'] = _bind_chart_function(viz._plot_relationship, column_name_one=col_a, column_name_two=col_b, target_column=target_column)
    
    # Run all pair chart functions
    core._bind_to_console_html(section='multi_variable', run_type='charts', run_dict=_relationship_ops, html_report=html_report, show_chart=show_chart, header_text="Column Relationships", df=df)

    # Run heatmap
    # Check for numeric columns
    if column_list is None:
        column_list = df.columns.values
    numeric_col_count = len([col for col in df.columns if col in column_list and is_numeric_dtype(df[col])])
    if numeric_col_count > 0:
        # Standard heatmap
        _heatmap_ops = {
            'Correlation Heatmap': _bind_chart_function(viz._plot_heatmap, column_list=column_list)
        }
        # Target heatmap
        if target_column:
            if is_numeric_dtype(df[target_column]):
                _heatmap_ops['Target Heatmap'] = _bind_chart_function(viz._plot_heatmap, column_list=column_list, target_column=target_column)
        # Visualize all
        for k,v in _heatmap_ops.items():
            core._bind_to_console_html(section='multi_variable', run_type='chart', run_dict={k:v}, html_report=html_report, show_chart=show_chart, header_text=k, df=df)
