import seaborn as sns
from edatk._single_variable._summary_statistics import _op_get_column_data_type, _op_distinct_count


def _plot_numeric_relationships(df, col_type='numeric'):
    """Plot numeric pair relationships

    Args:
        df (pandas dataframe): pandas dataframe to plot
        col_type (str, optional): column type to plot (numeric, numeric-consensed, string). Defaults to 'numeric'.

    Returns:
        None or sns.pairgrid result (fig): None if no results or sns pairgrid result if it exists
    """

    col_names = [col for col in df.columns if _op_get_column_data_type(df, col) == col_type]

    if col_type == 'numeric':
        if col_names:
            fig = sns.PairGrid(df, vars=col_names, aspect=1.5)
            fig.map_lower(sns.scatterplot)
            fig.map_diag(sns.kdeplot)
            fig.map_upper(sns.kdeplot)
            return fig
    elif col_type in ['numeric-condensed', 'string']:
        # Only plot string columns if they have < N unique values
        if col_type == 'string':
            col_type = [col for col in col_names if _op_distinct_count(df, col) <= 10]
        
        # Numeric columns to plot against
        col_names_numeric = [col for col in df.columns if _op_get_column_data_type(df, col) == 'numeric']
        
        # Plot if at least one of each
        if col_names and col_names_numeric:
            fig = sns.PairGrid(df, x_vars=col_names, y_vars=col_names_numeric, aspect=1.5)
            fig.map_diag(sns.kdeplot)
            fig.map_offdiag(sns.barplot, color='grey')
            return fig

    return None