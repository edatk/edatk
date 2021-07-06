import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import math
from datetime import datetime


def _check_for_pandas_df(df):
    """Check that input is a pandas dataframe

    Args:
        df (pandas dataframe): object to check instance against
    """
    assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"


def _get_fig_size_dynamic(num_plots, columns):
    """Calculate x and y figure size based on plots and columns.

    Args:
        num_plots (int): number of visual plots in total.
        columns (int): number of columns that will be displayed.

    Returns:
        tuple: calculated x and y size in float format.
    """
    current_fig_size = plt.rcParamsDefault['figure.figsize']
    x, y = current_fig_size
    return 11.0, y * num_plots / float(columns)


def _get_rows_calc(num_plots, columns):
    """Calculate number of rows for subplots given total plots and columns.

    Args:
        num_plots (int): number of visual plots in total.
        columns (int): number of columns that will be displayed.

    Returns:
        int: number of rows to use.
    """
    rows = math.ceil(num_plots / float(columns))
    return rows


def get_fig_ax(total_num_plots, columns=2):
    """Get fig, axs, and row/column dict given total plots and number of columns.

    Args:
        total_num_plots (int): number of visual plots in total.
        columns (int, optional): number of columns that will be displayed. Defaults to 2.

    Returns:
        tuple: fig, axs, row_col_dict
    """

    # Rows and columns from plot count
    if total_num_plots > 1:
        rows = _get_rows_calc(total_num_plots, columns)
    else:
        rows = 1
        columns = 1

    # Figsize override
    fig_size_d = _get_fig_size_dynamic(rows * columns, columns)

    # Get fig and axs given rows and cols
    sns.set_theme()
    sns.set_style('darkgrid')
    fig, axs = plt.subplots(rows, columns, squeeze=False, figsize=fig_size_d)
    sns.despine(left=True, bottom=True) # must be done after fig to avoid printing dims
    plt.tight_layout(pad=5.0)

    # For number of charts and dims, generate row col tuples
    row_col_dict = {}
    for i in range(rows * columns):
        row = int(i // columns)
        column = int(i % columns)
        row_col_dict[i] = (row, column)

    # Turn off last axis if odd number and > 1
    if (total_num_plots % columns != 0) and (total_num_plots > 1):
        axs[-1,-1].axis('off')
    
    return fig, axs, row_col_dict


def _rotate_x_axis_labels(ax):
    """Rotate the x axis labels slightly to prevent overlapping.

    Args:
        ax (matplotlib ax object): ax object to have x labels rotated
    """
    ax.set_xticklabels(ax.get_xticklabels(),rotation=30)


def _integer_y_axis_format(ax):
    """Force y axis into integer format.

    Args:
        ax (matplotlib ax object): ax object to force integers on y axis
    """
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))


def _bind_to_console_html(section, run_type, run_dict, html_report, show_chart=True, header_text=None, **kwargs):
    """Bind result of a run dict to consule or html

    Args:
        section (string): section grouping, used for html partitioning
        run_type (string): 'table' or 'charts'
        run_dict (dict): dictionary of operation names and functions
        html_report (HTMLReport class): html report instance or None if should just print to console
        show_chart (bool): Whether to show chart or not when running in console mode
        header_text (string): If not none, will print or title with a header text
        **kwargs: any arguments that should be passed into each row in run_dict
    """
    
    # Check for only valid run types
    assert run_type in ['table', 'chart', 'charts'], "Invalid run type, must be table or charts"

    # Operation header
    if header_text:
        if html_report:
            html_report.save_title(header_text, section=section)
        else:
            print('\n')
            header_text = f'========== {header_text} =========='
            print(header_text)

    
    if run_type == 'table':
        
        # Initiate console and html description string
        if html_report:
            table_list_of_dict = []
        else:
            result = ''
        
        # Loop through operations
        for k, op in run_dict.items():
            
            # Execute op
            op_result = op(**kwargs)
            
            # Dynamic format bind
            if isinstance(op_result, str):
                if html_report:
                    table_list_of_dict.append({'metric':k, 'value':op_result})
                else:
                    result += f'{k:20}: {op_result}'
            elif k[-1:] == '%':
                op_result *= 100.0
                if html_report:
                    table_list_of_dict.append({'metric':k, 'value':f'{round(op_result,2)}%'})
                else:
                    result += f'{k:20}: {op_result:.2f}%'
            elif isinstance(op_result, int):
                if html_report:
                    table_list_of_dict.append({'metric':k, 'value':op_result})
                else:
                    result += f'{k:20}: {op_result}'
            elif isinstance(op_result, float):
                if html_report:
                    table_list_of_dict.append({'metric':k, 'value':round(op_result,2)})
                else:
                    result += f'{k:20}: {op_result:.2f}'
            else:
                if html_report:
                    table_list_of_dict.append({'metric':k, 'value':op_result})
                else:
                    result += f'{k:20}: {op_result}'

            # New line for next result
            if not html_report:
                result += '\n'
        
        # save to file if needed or print combined string back to console
        if html_report:
            html_report.save_table(table_list_of_dict, section=section)
        else:
            print(result)


    elif run_type in['chart', 'charts']:
       
        # Visual layout
        fig, axs, row_col_dict = get_fig_ax(len(run_dict), 2)

        # Build visuals
        for i, (k, visual) in enumerate(run_dict.items()):
            # Find chart placement
            row, col = row_col_dict[i]
            ax = axs[row, col]

            # Plot chart
            visual(**kwargs, ax=ax)

    elif run_type == 'chartx':

        # Single chart bind to fig
        for i, (k, visual) in enumerate(run_dict.items()):
            fig = visual(**kwargs)


    if run_type in ['chart', 'charts']:

        # Save figure if needed
        if html_report and fig:
            html_report.save_chart_to_image(fig, f'edatk_{run_type}_{section}_{datetime.utcnow().strftime("%m_%d_%Y_%H_%M_%S_%f")}', section=section)
        else:
            if show_chart and fig:
                plt.show()
        
        # Cleanup    
        plt.close('all')
