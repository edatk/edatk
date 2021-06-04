# edatk: Python Exploratory Data Analysis Toolkit

edatk is a open source project for exploratory data analysis in Python. This is a new project and while features are simple now, the goal is to automate and organize as much of the traditional eda workflow as possible. 

## Installation
```
pip install edatk
```

## Running edatk
```python
# Import library
import edatk as eda

# Load in your dataframe (using seaborn below as an example)
import seaborn as sns
df = sns.load_dataset('diamonds')

# Run auto eda, pass in path for saving html report
eda.auto_eda(df, save_path='C:\\Users\\username\\Documents\\edatk')
```

## Contributing
If you are interested in contributing, please see the [contributing documentation](/docs/developer/CONTRIBUTING.md).