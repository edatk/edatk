# edatk: Python Exploratory Data Analysis Toolkit

edatk is a open source project for exploratory data analysis in Python. This is a new project and while features are simple now, the goal is to automate and organize as much of the traditional eda workflow as possible. 

## Installation
```
pip install edatk
```

## Examples and Getting Started
```python
# Import library
import edatk as eda

# Load in your dataframe (using seaborn below as an example)
import seaborn as sns
df = sns.load_dataset('diamonds')

# Run auto eda, pass in path for saving html report
eda.auto_eda(df, save_path='C:\\Users\\username\\Documents\\edatk')
```

## Feature Overview

> Feature [status]

- Column by column analysis [partial]
    - Basic descriptive statistics (mean, median, min, max, etc) [completed]
    - Distribution charts (numeric) and most frequent values (categorical) [partial]
    - Normality Tests and additional metrics (skew, kurtosis) [partial]
- Relationships between columns
    - Pair grid [partial]
    - Correlation heatmap [planned]
- Basic feature -> target analysis and feature importance [planned]
- Autofind interesting relationships and features [planned]


## Contributing
If you are interested in contributing, please see the [contributing documentation](/docs/developer/CONTRIBUTING.md).

## Stability
This library is not yet ready for production use. Treat with caution and for non production purposes aiding in deeper, more formal data analysis.

## Author

* **Barrett Studdard** - [@bstuddard](https://github.com/bstuddard)