import math
from typing import Optional
import numpy as np
import pandas as pd
import seaborn as sns
from seaborn.miscplot import palplot
from seaborn.palettes import color_palette
from edatk._single_variable._summary_statistics import _op_get_column_data_type, _op_distinct_count


def _plot_relationship(
        df: pd.DataFrame, 
        column_name_one: str, 
        column_name_two: str, 
        ax: object, 
        target_column: Optional[str] = None
    ):
    """Plot relationship columns given df and two column names

    Args:
        df (pd.DataFrame): input dataframe
        column_name_one (str): name of column 1 to be compared.
        column_name_two (str): name of column 2 to be compared
        ax (matplotlib ax): chart to plot to.
    """
    # Determine data types of two cols
    dt_one = _op_get_column_data_type(df, column_name_one)
    dt_two = _op_get_column_data_type(df, column_name_two)

    # Set col names as title
    ax.set_title(f'{column_name_one}-{column_name_two}')

    # Hue color column
    if target_column is not None:
        if (target_column != column_name_one) and (target_column != column_name_two):
            hue_color_column = f'{target_column}_lc'
            hue_order = df[hue_color_column].value_counts().index.to_list()
            colors = ['tab:orange', 'tab:purple', 'tab:cyan']
            colors = colors[:len(hue_order)]
            color_palette = {hue:color for hue, color in zip(hue_order, colors)}
        else:
            hue_color_column = None
            hue_order = None
            color_palette = sns.color_palette('tab10')
    else:
        hue_color_column = None
        hue_order = None
        color_palette = sns.color_palette('tab10')

    # --Both numeric = scatter--
    if dt_one == 'numeric' and dt_two == 'numeric':
        
        # X and y fix at zero if possible
        force_axis_to_zero = False # could be later exposed in api
        if force_axis_to_zero: 
            xmax = math.ceil(np.max(df[column_name_one].dropna()) * 1.25)
            xmin = math.floor(np.min(df[column_name_one].dropna()))
            if xmin > 0.0:
                xmin = 0
            ymax = math.ceil(np.max(df[column_name_two].dropna()) * 1.25)
            ymin = math.floor(np.min(df[column_name_two].dropna()))
            if ymin > 0.0:
                ymin = 0
            ax.set_xlim(xmin, xmax)
            ax.set_ylim(ymin, ymax)

        # Plot scatter
        max_sample = 1000
        if len(df) <= max_sample:
            sns.scatterplot(data=df, x=column_name_one, y=column_name_two, hue=hue_color_column, hue_order=hue_order, palette=color_palette, ax=ax)
        else:
            ct = sns.scatterplot(data=df.sample(n=max_sample, random_state=42), x=column_name_one, y=column_name_two, hue=hue_color_column, hue_order=hue_order, palette=color_palette, ax=ax)
            ct.set_title(f'{ct.get_title()}, n={max_sample} of {len(df)}')
        

    # --Numeric and Condensed = split a kde plot--
    elif (dt_one == 'numeric' and dt_two == 'numeric-condensed') or (dt_one == 'numeric-condensed' and dt_two == 'numeric'):
        if dt_one == 'numeric-condensed':
            string_col = column_name_one
            numeric_col = column_name_two
        else:
            string_col = column_name_two
            numeric_col = column_name_one
        
        sns.kdeplot(data=df, x=numeric_col, hue=string_col, common_norm=False, ax=ax)

    # --Text/Bool as one column, countplot/boxplot/kdeplot depending on data types and unique counts--
    elif (dt_one in ['string', 'bool'] and dt_two in ['numeric', 'numeric-condensed']) or (dt_one in ['numeric', 'numeric-condensed'] and dt_two in ['string', 'bool']):
        if dt_one in ['string', 'bool']:
            string_col = column_name_one
            numeric_col = column_name_two
        else:
            string_col = column_name_two
            numeric_col = column_name_one

        # Replace topn with other
        topn=4
        group_df = df.groupby(string_col)[numeric_col].agg(['sum', 'count']).reset_index()
        top_categories = group_df.sort_values(by='count', ascending=False)[:topn][string_col].astype('str').values.tolist()
        df2 = df.copy()
        df2[string_col] = df2[string_col].astype('str')
        df2[string_col].fillna('Missing', inplace=True)
        top_categories.append('Missing')
        df2.loc[~df2[string_col].isin(top_categories),string_col] = 'Other'

        # Get count of string categories
        distinct_string_count = _op_distinct_count(df2, string_col)

        # Plot distributions with boxplot (string, numeric) or countplot (string, bool)
        if (dt_one == 'bool' or dt_two == 'bool') and (dt_one != 'numeric' and dt_two != 'numeric'):
            sns.countplot(y=df2[numeric_col], hue=df2[string_col], ax=ax)
        elif (dt_one == 'bool' or dt_two == 'bool' or distinct_string_count == 2) and (dt_one == 'numeric' or dt_two == 'numeric'):
            sns.kdeplot(data=df2, x=numeric_col, hue=string_col, common_norm=False, ax=ax)
        else:

            # Box plot categories vs. numeric
            sort_order = df2[string_col].value_counts().reset_index()['index'].values.tolist()
            cpalette = ['red' if 'Missing' in x else 'tab:blue' if 'Other' in x else 'grey' for x in sort_order]
            sns.boxplot(data=df2, x=string_col, y=numeric_col, palette=cpalette, order=sort_order, ax=ax)
            
            # Swarm plot target
            max_sample = 75
            if len(df) > max_sample:
                if hue_color_column is not None:
                    num_groups = _op_distinct_count(df, hue_color_column)
                    group_sample = int(max_sample / num_groups * 1.0)
                    ct = sns.swarmplot(data=df.groupby(hue_color_column).apply(lambda x: x.sample(group_sample, replace=True, random_state=42)), x=string_col, y=numeric_col, hue=hue_color_column, hue_order=hue_order, palette=color_palette, order=sort_order, ax=ax)
                    ct.set_title(f'{ct.get_title()}, swarm n={group_sample * num_groups} (with resampling) of {len(df)}')
                else:
                    ct = sns.swarmplot(data=df2.sample(n=max_sample, random_state=42), x=string_col, y=numeric_col, hue=hue_color_column, hue_order=hue_order, order=sort_order, ax=ax)
                    ct.set_title(f'{ct.get_title()}, swarm n={max_sample} of {len(df)}')
            else:
                sns.swarmplot(data=df2, x=string_col, y=numeric_col, hue=hue_color_column, hue_order=hue_order, order=sort_order, ax=ax)

    # --Both Text/Bool = countplot--
    elif dt_one in ['string', 'bool', 'numeric-condensed'] and dt_two in ['string', 'bool', 'numeric-condensed']:

        # Replace topn with other
        topn=2
        group_df = df.groupby(column_name_one)[column_name_one].agg(['count']).reset_index()
        top_categories = group_df.sort_values(by='count', ascending=False)[:topn][column_name_one].astype('str').values.tolist()
        df2 = df.copy()
        df2[column_name_one] = df2[column_name_one].astype('str')
        df2[column_name_one].fillna('Missing', inplace=True)
        top_categories.append('Missing')
        df2.loc[~df2[column_name_one].isin(top_categories),column_name_one] = 'Other'

        group_df_2 = df.groupby(column_name_two)[column_name_two].agg(['count']).reset_index()
        top_categories_2 = group_df_2.sort_values(by='count', ascending=False)[:topn][column_name_two].astype('str').values.tolist()
        df2[column_name_two] = df2[column_name_two].astype('str')
        df2[column_name_two].fillna('Missing', inplace=True)
        top_categories_2.append('Missing')
        df2.loc[~df2[column_name_two].isin(top_categories_2),column_name_two] = 'Other'
        
        # Plot distributions with barplot (target) or countplot (default)
        df2['combinations'] = df2[column_name_one] + '\n' + df2[column_name_two]
        sort_order = df2['combinations'].value_counts().reset_index()['index'].values.tolist()
        cpalette = ['red' if 'Missing' in x else 'tab:blue' if 'Other' in x else 'grey' for x in sort_order]
        _ = [label.set_fontsize(10) for label in ax.get_yticklabels()]
        if hue_color_column:
            grouped_df = df2.groupby(hue_color_column)['combinations'].value_counts(normalize=True).rename('percentage').reset_index()
            sns.barplot(data=grouped_df, y='combinations', x='percentage', orient='h', hue=hue_color_column, hue_order=hue_order, palette=color_palette, ax=ax)
        else:
            sns.countplot(data=df2, y='combinations', hue=hue_color_column, hue_order=hue_order, order=sort_order, ax=ax)


def _plot_heatmap(
        df: pd.DataFrame, 
        ax: object, 
        column_list: Optional[list[str]] = None, 
        target_column: Optional[str]=None
    ):
    """Plot a heatmap of columns. If target passed, then one col heatmap.

    Args:
        df (pd.DataFrame): input dataframe
        ax (matplotlib ax): ax to plot to
        column_list (str, optional): Columns to be analyzed. Defaults to None.
        target_column (str, optional): Name of target column. Defaults to None.
    """
    if column_list is None:
        column_list = df.columns.values
    
    if target_column:
        ct = sns.heatmap(df.loc[:,column_list].corr()[[target_column]].sort_values(by=target_column, ascending=False), ax=ax, vmin=-1, vmax=1, annot=True, cmap='Spectral')
    else:
        mask = np.triu(np.ones_like(df.loc[:,column_list].corr(), dtype=np.bool))
        ct = sns.heatmap(df.loc[:,column_list].corr(), ax=ax, vmin=-1, vmax=1, annot=True, cmap='Spectral', mask=mask)

    # Fix label rotation
    ct.set_yticklabels(ct.get_yticklabels(), rotation=0)