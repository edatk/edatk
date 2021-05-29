import warnings
warnings.filterwarnings( "ignore", module = "matplotlib\..*" )
warnings.filterwarnings( "ignore", module = "seaborn\..*" )

from ._single_variable._auto_eda import auto_eda_columns
from ._core import get_fig_ax


__all__ = [
    "auto_eda_columns",
    "get_fig_ax"
]

__version__ = '0.0.2'