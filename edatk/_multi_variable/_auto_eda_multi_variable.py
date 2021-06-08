import edatk._core as core
import edatk._multi_variable._visuals as viz

_auto_relationship_ops = {
    'pairgrid-numeric': {
        'Pair Plot': viz._plot_numeric_relationships
    },
    'pairgrid-numeric-condensed': {
        'Pair Plot': lambda df: viz._plot_numeric_relationships(df, col_type='numeric-condensed')
    },
    'pairgrid-string': {
        'Pair Plot': lambda df: viz._plot_numeric_relationships(df, col_type='string')
    }
}

def _auto_eda_mutli_variable(df, html_report=None, ignore_errors=True, show_chart=True):
    core._bind_to_console_html(section='multi_variable', run_type='chart', run_dict=_auto_relationship_ops['pairgrid-numeric'], html_report=html_report, show_chart=show_chart, header_text="Numeric to Numeric Relationships", df=df)
    core._bind_to_console_html(section='multi_variable', run_type='chart', run_dict=_auto_relationship_ops['pairgrid-numeric-condensed'], html_report=html_report, show_chart=show_chart, header_text="Categorical to Numeric Relationships", df=df)
    core._bind_to_console_html(section='multi_variable', run_type='chart', run_dict=_auto_relationship_ops['pairgrid-string'], html_report=html_report, show_chart=show_chart, df=df)
