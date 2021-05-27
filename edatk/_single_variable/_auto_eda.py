import edatk._single_variable._summary_statistics as sst

_auto_eda_column_ops = {
    'Row Count': sst._op_rowcount,
    'Missing Values': sst._op_missing_rows,
    'Mean': sst._op_mean,
    'Median': sst._op_median,
    'Min': sst._op_min,
    'Max': sst._op_max,
    'Standard Deviation': sst._op_standard_deviation
}

def auto_eda_single_column(df, column_name):
    """Print summary statistics given a dataframe and column name string. Ignores NAs besides missing count row.

    Args:
        df (pandas dataframe): input dataframe
        column_name (string): column name to be summarized
    """
    result = ''
    for k, op in _auto_eda_column_ops.items():
        result += f'{k}: {op(df, column_name):.2f}'
        result += '\n'
    print(result)