from setuptools import setup


with open("README.md", "r") as readme_file:
    readme = readme_file.read()


requirements = [
    'seaborn>=0.11',
    'numpy>=1.20',
    'matplotlib>=3.4.2',
    'pandas>=1.2.4',
    'jinja2>=3.0.1',
    'scipy>=1.6.3'
]

setup(
    name="edatk",
    version="0.0.5",
    author="Barrett Studdard",
    author_email="barrettstuddard@gmail.com",
    description="edatk: python exploratory data analysis toolkit",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/edatk/edatk/",
    packages=['edatk', 'edatk._html_report', 'edatk._single_variable'],
    package_data={'edatk': ['_html_report/*.html']},
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)