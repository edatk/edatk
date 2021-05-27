from setuptools import setup


with open("README.md", "r") as readme_file:
    readme = readme_file.read()


requirements = [
    'seaborn>=0.11',
    'numpy>=1.20'
]

setup(
    name="edatk",
    version="0.0.2",
    author="Barrett Studdard",
    author_email="barrettstuddard@gmail.com",
    description="edatk: python exploratory data analysis toolkit",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/edatk/edatk/",
    packages=['edatk'],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)