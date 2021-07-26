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
df = sns.load_dataset('iris')

# Run auto eda, optionally pass in path for saving html report and target column
eda.auto_eda(df, save_path='C:\\Users\\username\\Documents\\edatk', target_column='species')
```

## Feature Overview

> Feature [**status**]
- Tabular data [**partial**]
    - Column by column analysis [**partial**]
        - Basic descriptive statistics (mean, median, min, max, etc) [**completed**]
        - Distribution charts (numeric) and most frequent values (categorical) [**completed**]
        - Normality Tests [**planned**].
    - Relationships between columns [**completed**]
    - TSNE [**planned**]
    - Basic feature -> target analysis and feature importance [**planned**]
    - Autofind interesting relationships and features [**planned**]
    - Basic exploratory NLP for text columns [**planned**]
- Exploring Predicted vs. True Results [**planned**]
    - Classification Results Plots
        - True vs. Predicted Heatmap by Class
        - Mosiac Plot
- Time Series [**planned**]
- Performance Improvements [**planned**]
    - Operation timeouts

## Contributing
If you are interested in contributing, please see the [contributing documentation](/docs/developer/CONTRIBUTING.md).

## Stability
This library is not yet ready for production use. Treat with caution and for non production purposes aiding in deeper, more formal data analysis.

## Author

* **Barrett Studdard** - [@bstuddard](https://github.com/bstuddard)