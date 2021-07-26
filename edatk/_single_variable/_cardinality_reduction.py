import pandas as pd

import edatk._single_variable._summary_statistics as sst


def _top_value_or_other(x: str, top_value_list: list[str]) -> str:
    if x in top_value_list:
        return x
    else:
        return 'Other'


def _range_classifier(x: float, low: float, high: float, column_name: str) -> str:
    if x < low:
        return f'low ({column_name}<{float(round(low,2))})'
    elif x < high:
        return f'medium ({float(round(low,2))}<{column_name}<{float(round(high,2))})'
    else:
        return f'high ({column_name}>{float(round(high,2))})'


def _get_column_reduced_cardinality(
        df: pd.DataFrame, 
        column_name: str, 
        cardinality: int, 
        desired_cardinality: int
    ) -> pd.Series:
    """Return a series that is the reduced cardinality version of a supplied df[column_name]

    Args:
        df (pd.DataFrame): input df
        column_name (str): string column name to reduce cardinality on
        cardinality (int): cardinality of the input column
        desired_cardinality (int): desired cardinality

    Returns:
        pd.Series: reduced cardinality pandas series
    """
    if cardinality <= desired_cardinality:
        return df[column_name]
    else:
        target_dtype = sst._op_get_column_data_type(df, column_name)
        s = df[column_name].dropna()
        reduced_cardinality_series = None

        if target_dtype == 'string':
            # Count all values (presort)
            vcounts = s.value_counts()
            top_values = vcounts[:(desired_cardinality-1)]
            reduced_cardinality_series = s.apply(lambda x: _top_value_or_other(x, top_values))

        elif 'numeric' in target_dtype:
            mean_value = sst._op_mean(df, column_name)
            std = sst._op_standard_deviation(df, column_name)
            low = mean_value - std
            high = mean_value + std
            reduced_cardinality_series = s.apply(lambda x: _range_classifier(x, low, high, column_name))

        else:
            reduced_cardinality_series = 'NA'

        return reduced_cardinality_series


def _add_low_cardinality_target_column(df: pd.DataFrame, target_column: str, desired_cardinality: int):
    """Add an additional low cardinality derived column in place.

    Args:
        df (pd.DataFrame): input dataframe
        target_column (str): string name of the target column
        desired_cardinality (int): desired cardinality (numeric will always be 3 though).
    """
    
    # Get information about the target column
    inferred_col_name = f'{target_column}_lc'
    target_distinct_count = sst._op_distinct_count(df, target_column)
    
    # Cardinality > desired, reduce cardinality
    if target_distinct_count > desired_cardinality:
        df[inferred_col_name] = _get_column_reduced_cardinality(
            df=df, 
            column_name=target_column, 
            cardinality=target_distinct_count, 
            desired_cardinality=desired_cardinality
        )
    else:
        # If cardinality <= desired, leave as is
        df[inferred_col_name] = df[target_column]