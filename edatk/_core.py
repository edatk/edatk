import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import math


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
    rows = _get_rows_calc(total_num_plots, columns)

    # Figsize override
    fig_size_d = _get_fig_size_dynamic(rows * columns, columns)

    # Get fig and axs given rows and cols
    sns.set_theme()
    sns.set_style('darkgrid')
    fig, axs = plt.subplots(rows, columns, squeeze=False, figsize=fig_size_d)
    sns.despine(left=True, bottom=True) # must be done after fig to avoid printing dims

    # For number of charts and dims, generate row col tuples
    row_col_dict = {}
    for i in range(rows * columns):
        row = int(i // columns)
        column = int(i % columns)
        row_col_dict[i] = (row, column)

    # Turn off last axis if odd number
    if total_num_plots % columns != 0:
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
