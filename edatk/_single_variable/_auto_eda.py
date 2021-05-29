import matplotlib.pyplot as plt

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
    return f'|{min} --||{tf} ~ {med} ~ {sf}||-- {max}|'


_auto_eda_column_ops = {
    'numeric': {
        'Data Type': sst._op_get_column_data_type,
        'Row Count': sst._op_rowcount,
        'Distinct Count': sst._op_distinct_count,
        'Missing Values': sst._op_missing_rows,
        'Missing Value %': lambda x, y: float(sst._op_missing_rows(x, y)) / float(sst._op_rowcount(x, y)),
        'Mean': sst._op_mean,
        'Median': sst._op_median,
        'Min': sst._op_min,
        'Max': sst._op_max,
        'Standard Deviation': sst._op_standard_deviation,
        'Text Box Plot': _text_box_plot
    },
    'string': {
        'Data Type': sst._op_get_column_data_type,
        'Row Count': sst._op_rowcount,
        'Distinct Count': sst._op_distinct_count,
        'Missing Values': sst._op_missing_rows,
        'Missing Value %': lambda x, y: float(sst._op_missing_rows(x, y)) / float(sst._op_rowcount(x, y)),
        'Min': sst._op_min,
        'Max': sst._op_max
    }
}

_auto_eda_column_visuals = {
    'numeric': {
        'Box Plot': viz._plot_distributions
    },
    'string': {
        'Count Plot': viz._plot_categorical_counts,
        'Count Plot %': viz._plot_categorical_percent_counts
    }
}


def _auto_eda_single_column(df, column_name):
    """Print summary statistics and charts given a dataframe and column name string. Ignores NAs besides missing count row.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized
    """
    # Operation header
    print(f'========== {column_name} ==========')

    # Determine column data type and summary ops
    data_type = sst._op_get_column_data_type(df, column_name)
    column_operations = _auto_eda_column_ops[data_type]

    # Build description string
    result = ''
    for k, op in column_operations.items():
        # Execute op
        op_result = op(df, column_name)
        
        # String format
        if type(op_result) is str:
            result += f'{k:20}: {op_result}'
        elif k[-1:] == '%':
            result += f'{k:20}: {op_result*100.0:.2f}%'
        elif type(op_result) is int:
            result += f'{k:20}: {op_result}'
        else:
            result += f'{k:20}: {op_result:.2f}'
        
        #New line for next result
        result += '\n'
    
    # Print combined string back to console
    print(result)

    # Visual layout
    visual_dict = _auto_eda_column_visuals[data_type]
    fig, axs, row_col_dict = core.get_fig_ax(len(visual_dict), 2)

    # Build visuals
    for i, (k, visual) in enumerate(visual_dict.items()):
        # Find chart placement
        row, col = row_col_dict[i]
        ax = axs[row, col]

        # Plot chart
        visual(df, column_name, ax)

    plt.show()
    print('\n')


def auto_eda_columns(df, column_list=None):
    """Print summary statistics and charts given a dataframe and list of column name strings. Ignores NAs besides missing count row.

    Args:
        df (pandas dataframe): input dataframe
        column_list (list): list of column names to be summarized
    """

    # Check if user pased in list
    if column_list: 
        # Single column
        if type(column_list) is str and column_list in df.columns:
            _auto_eda_single_column(df, column_list)
        else:
            # Multiple defined columns
            for col in column_list:
                _auto_eda_single_column(df, col)
    else:
        # Run all columns
        for col in df.columns:
            _auto_eda_single_column(df, col)
