import pathlib
import os
import re

from edatk._html_report._template_ops import _build_template

class HTMLReport:
    """Class for capturing html details and rendering + saving file.
    """
    def __init__(self, save_path=None):
        """Create new instance of HTML Report

        Args:
            save_path (string, optional): Path to save off finalized html report and all assets. Defaults to None.
        """
        self._create_report_directory(save_path)
        self._single_variable_charts = []


    def _create_report_directory(self, save_path):
        """Create report repository at path

        Args:
            save_path (string): Path to save off finalized html report and all asets
        """
        # Calc Save path
        if save_path:
            save_path = os.path.join(save_path, 'html_report')
        else:
            save_path = os.path.join(os.getcwd(), 'html_report')
        
        # Create parent rerport path
        pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)

        # Create underlying assets path
        pathlib.Path(os.path.join(save_path, 'assets')).mkdir(parents=True, exist_ok=True)

        # Save off paths
        self.root_path =  save_path
        self.asset_path = os.path.join(save_path, 'assets')


    def save_title(self, title):
        """Save title to html rendering.

        Args:
            text (string): Text to render as paragraph.
        """
        title = title.replace("\n",' <br> ')
        self._single_variable_charts.append({'render_type':'title', 'render_value': title})


    def save_text(self, text):
        """Save text to html rendering.

        Args:
            text (string): Text to render as paragraph.
        """
        text = text.replace("\n",' <br> ')
        self._single_variable_charts.append({'render_type':'text', 'render_value': text})


    def save_chart_to_image(self, fig, chart_name):
        """Save chart to html rendering.

        Args:
            fig (matplotlib fig): Fig to save as png.
            chart_name (string): Chart name to use as file name.
        """

        # Save off chart
        image_file_name = f'{chart_name}.png'
        fig.savefig(os.path.join(self.asset_path, image_file_name))

        # Add to render pipeline
        self._single_variable_charts.append({'render_type': 'png', 'render_value': image_file_name})
        self._single_variable_charts.append({'render_type': 'lb', 'render_value': 'None'})


    def save_table(self, table_list_of_dict):
        """Save table to html rendering.

        Args:
            table_list_of_dict(list of dictionary objects): metric, value combination
        """
        self._single_variable_charts.append({'render_type':'table', 'render_value': table_list_of_dict})

    
    def build_final_template(self):
        """Build final template and write to file
        """
        template = _build_template(single_variable_charts=self._single_variable_charts)
        write_path = os.path.join(self.root_path, 'report.html')
        with open(write_path, 'w') as f:
            f.write(template)
        print(f'Report written to {write_path}. Open to view as a webpage.')