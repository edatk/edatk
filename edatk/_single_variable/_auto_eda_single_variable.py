import matplotlib.pyplot as plt
from seaborn.external.docscrape import header

import edatk._core as core
import edatk._single_variable._summary_statistics as sst
import edatk._single_variable._visuals as viz

def _text_box_plot(df, column_name):
    """Return the text box plot given a dataframe and column name string.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be analyzed

    Returns:
        string: box plot as a simple string
    """
    min = sst._op_min(df, column_name)
    tf = sst._op_quantile(df, column_name, 0.25)
    med = sst._op_median(df, column_name)
    sf = sst._op_quantile(df, column_name, 0.75)
    max = sst._op_max(df, column_name)
    try:
        return f'|{min:.2f} --||{tf:.2f} ~ {med:.2f} ~ {sf:.2f}||-- {max:.2f}|'
    except:
        return f'|{min} --||{tf} ~ {med} ~ {sf}||-- {max}|'


def _dist_rank_wrapper(df, column_name, ax):
    _, dist_df = sst._get_theoritical_distributions(df, column_name)
    dist_series = dist_df.set_index('distribution_type')['rmse'].squeeze()
    if dist_series is not None:
        viz._plot_simple_bar(dist_series, f"{column_name} Distribution Fit (RMSE of Density Deltas)", ax)


_auto_eda_column_ops = {
    'numeric': {
        'Column Name': lambda df, column_name: str(column_name),
        'Data Type Grouping': sst._op_get_column_data_type,
        'Data Type': lambda df, column_name: str(df[column_name].dtype),
        'Row Count': sst._op_rowcount,
        'Distinct Count': sst._op_distinct_count,
        'Missing Values': sst._op_missing_rows,
        'Missing Value %': lambda df, column_name: float(sst._op_missing_rows(df, column_name)) / float(sst._op_rowcount(df, column_name)),
        'Mean': sst._op_mean,
        'Median': sst._op_median,
        'Min': sst._op_min,
        'Max': sst._op_max,
        'Standard Deviation': sst._op_standard_deviation,
        'Text Box Plot': _text_box_plot
    },
    'numeric-condensed': {
        'Column Name': lambda df, column_name: str(column_name),
        'Data Type Grouping': sst._op_get_column_data_type,
        'Data Type': lambda df, column_name: str(df[column_name].dtype),
        'Row Count': sst._op_rowcount,
        'Distinct Count': sst._op_distinct_count,
        'Missing Values': sst._op_missing_rows,
        'Missing Value %': lambda df, column_name: float(sst._op_missing_rows(df, column_name)) / float(sst._op_rowcount(df, column_name)),
        'Mean': sst._op_mean,
        'Median': sst._op_median,
        'Min': sst._op_min,
        'Max': sst._op_max,
        'Standard Deviation': sst._op_standard_deviation,
        'Text Box Plot': _text_box_plot
    },
    'string': {
        'Column Name': lambda df, column_name: str(column_name),
        'Data Type Grouping': sst._op_get_column_data_type,
        'Data Type': lambda df, column_name: str(df[column_name].dtype),
        'Row Count': sst._op_rowcount,
        'Distinct Count': sst._op_distinct_count,
        'Missing Values': sst._op_missing_rows,
        'Missing Value %': lambda df, column_name: float(sst._op_missing_rows(df, column_name)) / float(sst._op_rowcount(df, column_name))
    },
    'bool': {
        'Column Name': lambda df, column_name: str(column_name),
        'Data Type Grouping': sst._op_get_column_data_type,
        'Data Type': lambda df, column_name: str(df[column_name].dtype),
        'Row Count': sst._op_rowcount,
        'Distinct Count': sst._op_distinct_count,
        'Missing Values': sst._op_missing_rows,
        'Missing Value %': lambda df, column_name: float(sst._op_missing_rows(df, column_name)) / float(sst._op_rowcount(df, column_name))
    }
}

_auto_eda_column_visuals = {
    'numeric': {
        'Box Plot': viz._plot_distributions,
        'Histogram': viz._plot_histogram,
        'Distributions': viz._plot_distribution_overlay,
        'Best Distribution': lambda df, column_name, ax: viz._plot_distribution_overlay(df, column_name, ax, best_only=True),
        'Distribution Fits': _dist_rank_wrapper
    },
    'numeric-condensed': {
        'Histogram': viz._plot_histogram,
    },
    'string': {
        'Count Plot': viz._plot_categorical_counts,
        'Count Plot %': viz._plot_categorical_percent_counts
    },
    'bool': {
        'Histogram': viz._plot_histogram
    }
}


def _auto_eda_single_column(df, column_name, html_report, show_chart):
    """Print summary statistics and charts given a dataframe and column name string. Ignores NAs besides missing count row.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized
        html_report (object): html report object to hold data and write to file
        show_chart (bool): whether to call plt.show, can be useful to disable in command line interactions
    """
    # Used for separating portions of html doc
    section = 'single_variable'

    # Determine column data type
    data_type = sst._op_get_column_data_type(df, column_name)

    # Try to find operations to do to summarize data type in question
    if data_type in _auto_eda_column_ops:
        column_operations = _auto_eda_column_ops[data_type]
    else:
        error_str = f'{column_name} data type ({data_type}) cannot be parsed.'
        print(error_str)
        if html_report:
            html_report.save_text(error_str, section=section)
        return None

    # Run metric table
    core._bind_to_console_html(section='single_variable', run_type='table', run_dict=column_operations, html_report=html_report, show_chart=show_chart, header_text=column_name, df=df, column_name=column_name)

    # Visual layout
    visual_dict = _auto_eda_column_visuals[data_type]
    core._bind_to_console_html('single_variable', 'charts', visual_dict, html_report, show_chart=show_chart, df=df, column_name=column_name)


def _single_col_ops_error_wrap(df, col, html_report, show_chart):
    section = 'single_variable'
    try:
        _auto_eda_single_column(df, col, html_report, show_chart)
    except:
        error_str = f'{col} was not able to be profiled due to errors'
        print(error_str)
        if html_report:
            html_report.save_text(error_str, section=section)
        plt.close('all')


def _auto_eda_columns(df, column_list=None, html_report=None, ignore_errors=True, show_chart=True):
    """Print summary statistics and charts given a dataframe and list of column name strings. Ignores NAs besides missing count row.

    Args:
        df (pandas dataframe): input dataframe
        column_list (list): list of column names to be summarized
        html_report (HTMLReport class): html report object to write data to
        ignore_errors (bool): whether to ignore errors and run what is possible or raise excpetions
        show_chart (bool): whether to call plt.show, can be useful to disable in command line interactions
    """

    # Check if user pased in list
    if column_list: 
        # Single column
        if isinstance(column_list, str) and column_list in df.columns:
            if ignore_errors:
                _single_col_ops_error_wrap(df, column_list, html_report, show_chart)
            else:
                _auto_eda_single_column(df, column_list, html_report, show_chart)
        else:
            # Multiple defined columns
            for col in column_list:
                if ignore_errors:
                    _single_col_ops_error_wrap(df, col, html_report, show_chart)
                else:
                    _auto_eda_single_column(df, col, html_report, show_chart)
    else:
        # Run all columns
        for col in df.columns:
            if ignore_errors:
                _single_col_ops_error_wrap(df, col, html_report, show_chart)
            else:
                _auto_eda_single_column(df, col, html_report, show_chart)
