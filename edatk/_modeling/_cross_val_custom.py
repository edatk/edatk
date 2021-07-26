from typing import Callable
from sklearn.model_selection import KFold
import pandas as pd
from typing import Callable


def cross_validate_custom(
        X: pd.DataFrame, 
        y: pd.Series, 
        model: object, 
        scorer: Callable[[float, float], float], 
        fit_method_name: str = 'fit', 
        predict_method_name: str ='predict'
    ) -> list[float]:
    """Run cross validate loop for given X, y, model, and methods.

    Args:
        X (pd.DataFrame): Features dataframe.
        y (pd.Series): target series.
        model (object): Model to use in cv loop.
        scorer (Callable[[float, float], float]): Scorer function (y_true, y_pred)
        fit_method_name (str, optional): Method name contained in model to use as fit. Defaults to 'fit'.
        predict_method_name (str, optional): Method name contained in model used in predict/scoring. Defaults to 'predict'.

    Raises:
        Exception: No fit method.
        Exception: No predict method.

    Returns:
        list[float]: List of cross val scores (typically floats).
    """

    # Make sure model has fit and predict method
    if not hasattr(model, fit_method_name):
        raise Exception("Model must have fit method")
    if not hasattr(model, predict_method_name):
        raise Exception("Model must have predict method")
    
    # Bind functions
    fit_method = getattr(model, fit_method_name)
    predict_method = getattr(model, predict_method_name)

    # Default KFold 5 split
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    # Loop through splits and append scores
    score_list = []
    for train_idx, test_idx in kf.split(X):

        # Split objects by idx
        X_train = X.iloc[train_idx, :]
        y_train = y.iloc[train_idx]
        X_test = X.iloc[test_idx, :]
        y_test = y.iloc[test_idx]

        # Fit model
        fit_method(X_train, y_train)

        # Score model
        preds = predict_method(X_test)
        score = scorer(y_test, preds)
        score_list.append(score)

    return score_list

