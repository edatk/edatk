import matplotlib.pyplot as plt

import edatk._core as core
import edatk._single_variable._summary_statistics as sst
import edatk._single_variable._visuals as viz
import edatk._html_report._report_builder as html_build

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
        'Box Plot': viz._plot_distributions,
        'Histogram': viz._plot_histogram
    },
    'string': {
        'Count Plot': viz._plot_categorical_counts,
        'Count Plot %': viz._plot_categorical_percent_counts
    }
}


def _auto_eda_single_column(df, column_name, html_report):
    """Print summary statistics and charts given a dataframe and column name string. Ignores NAs besides missing count row.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized
        html_report (object): html report object to hold data and write to file
    """

    # Operation header
    header_text = f'========== {column_name} =========='
    print(header_text)
    if html_report:
        html_report.save_title(column_name)

    # Determine column data type and summary ops
    data_type = sst._op_get_column_data_type(df, column_name)
    column_operations = _auto_eda_column_ops[data_type]

    # Initiate console and html description string
    result = ''
    if html_report:
        table_list_of_dict = []
        table_list_of_dict.append({'metric':'Column Name', 'value':column_name})
    
    for k, op in column_operations.items():
        # Execute op
        op_result = op(df, column_name)
        
        # String format
        if type(op_result) is str:
            result += f'{k:20}: {op_result}'
            if html_report:
                table_list_of_dict.append({'metric':k, 'value':op_result})
        elif k[-1:] == '%':
            op_result *= 100.0
            result += f'{k:20}: {op_result:.2f}%'
            if html_report:
                table_list_of_dict.append({'metric':k, 'value':round(op_result,2)})
        elif type(op_result) is int:
            result += f'{k:20}: {op_result}'
            if html_report:
                table_list_of_dict.append({'metric':k, 'value':op_result})
        else:
            result += f'{k:20}: {op_result:.2f}'
            if html_report:
                table_list_of_dict.append({'metric':k, 'value':round(op_result,2)})

        # New line for next result
        result += '\n'
    
    # Print combined string back to console (and save to file if needed)
    print(result)
    if html_report:
        html_report.save_table(table_list_of_dict)

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

    # Save figure if needed
    if html_report:
        html_report.save_chart_to_image(fig, f'single_var_{column_name}')
    
    # Chart to console and offset newline
    plt.show()
    print('\n')


def auto_eda_columns(df, column_list=None, save_path=None):
    """Print summary statistics and charts given a dataframe and list of column name strings. Ignores NAs besides missing count row.

    Args:
        df (pandas dataframe): input dataframe
        column_list (list): list of column names to be summarized
    """

    # Initiate html file ops if needed
    if save_path:
        html_report = html_build.HTMLReport(save_path)
    else:
        html_report = None

    # Check if user pased in list
    if column_list: 
        # Single column
        if type(column_list) is str and column_list in df.columns:
            _auto_eda_single_column(df, column_list, html_report)
        else:
            # Multiple defined columns
            for col in column_list:
                _auto_eda_single_column(df, col, html_report)
    else:
        # Run all columns
        for col in df.columns:
            _auto_eda_single_column(df, col, html_report)

    # Save off final html template
    if save_path:
        html_report.build_final_template()
