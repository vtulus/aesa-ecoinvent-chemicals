# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 11:57:52 2021

@author: VTulus
"""
__all__ = ["linear_regr"]

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

if __package__:
    from .turn_to_scientific import turn_to_scientific
else:
    from turn_to_scientific import turn_to_scientific


def linear_regr(x_in: pd.Series, y_in: pd.Series):
    """Performs linear regression on series of x and y data.

    Parameters
    ----------
    x_in : pandas.Series
        X values
    y_in : pandas.Series
        Y values

    Returns
    -------
    (X, y_pred) : tuple of numpy.ndarrays
        Points to plot the line
    r_square_scientific : str
        R^2 value in scientific notation, can be used to print on the plot
    (slope, intercept) : tuple of numpy.ndarrays
        Slope and intercept of the linear regression
    """

    #     if type(x_in) == np.ndarray: # check type .... ADD LATER
    if isinstance(x_in, pd.Series) and isinstance(y_in, pd.Series):
        x = x_in.to_numpy()  # pylint: disable=invalid-name
        y = y_in.to_numpy()  # pylint: disable=invalid-name

        # Mask NaN values
        mask = ~np.isnan(x) & ~np.isnan(y)

        X = x[mask].reshape(-1, 1)  # pylint: disable=invalid-name
        Y = y[mask].reshape(-1, 1)  # pylint: disable=invalid-name

        lr = LinearRegression()  # pylint: disable=invalid-name
        lr.fit(X, Y)
        y_pred = lr.predict(X)

        r_square = lr.fit(X, Y).score(X, Y)
        slope = lr.fit(X, Y).coef_
        intercept = lr.fit(X, Y).intercept_
    #     r_square_scientific = "$R^{2}$ = " + str("{:.2e}".format(r_square))
        r_square_scientific = "$R^{2}$ = " + \
            str("{:s}".format(turn_to_scientific(r_square, 2)))

    return (X, y_pred), r_square_scientific, (slope, intercept)
