import warnings
warnings.filterwarnings( "ignore", module = "matplotlib\..*" )
warnings.filterwarnings( "ignore", module = "seaborn\..*" )

from ._single_variable._auto_eda import auto_eda_columns


__all__ = [
    "auto_eda_columns"
]

__version__ = '0.0.2'