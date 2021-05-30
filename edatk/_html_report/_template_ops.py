from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('edatk', '_html_report'),
    autoescape=select_autoescape()
)

def _build_template(**kwargs):
    """Render and return html template given keyword args.

    Returns:
        string: rendered html
    """
    template = env.get_template('report_template.html')
    return template.render(**kwargs)