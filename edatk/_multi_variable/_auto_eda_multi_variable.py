from itertools import combinations

import edatk._core as core
import edatk._multi_variable._visuals as viz


def _get_column_combinations(df):
    """Given a dataframe, get a list of column combinations in tuples

    Args:
        df (pd.DataFrame): dataframe to analyze

    Returns:
        list[tuple[str, str]]: List of column name tuples
    """
    col_list = list(df.columns.values)
    return list(combinations(col_list, 2))


def _bind_chart_function(col_a, col_b):
    """For a given set of two columns, wrap those columns as parms into the plot relationship function

    Args:
        col_a (str): column_name_one
        col_b (str): column_name_two

    Returns:
        function: wrapped inner function
    """
    def inner_func(df, ax):
        return viz._plot_relationship(df=df, column_name_one=col_a, column_name_two=col_b, ax=ax)
    return inner_func


def _auto_eda_mutli_variable(df, html_report=None, ignore_errors=True, show_chart=True):
    _relationship_ops = {}
    
    # Get column combination tuples
    column_list = _get_column_combinations(df)
    # Loop through tuples
    for col_set in column_list:
        # Parse tuple
        col_a, col_b = col_set
        # Enclose function with tuple (df and ax is populated by caller)
        _relationship_ops[f'{col_a}-{col_b}'] = _bind_chart_function(col_a, col_b)
    
    # Run all chart functions
    core._bind_to_console_html(section='multi_variable', run_type='charts', run_dict=_relationship_ops, html_report=html_report, show_chart=show_chart, header_text="Column Relationships", df=df)
