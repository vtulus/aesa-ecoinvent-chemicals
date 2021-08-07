# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 12:21:35 2021

@author: VTulus
"""
__all__ = ["calculate_stats"]

import numpy as np
import pandas as pd
from scipy import stats

if __package__:
    from .turn_to_scientific import turn_to_scientific
else:
    from turn_to_scientific import turn_to_scientific


def calculate_stats(data: pd.Series, excl_power_range: int = (-1, 1)):  # pylint: disable=too-many-locals
    """Returns calculated statistical data as dict and block of text.

    The returned block of text if formatted to be used in a plot.

    Parameters
    ----------
    data : pandas.Series
        Data with numerical values to perform the analysis on
    excl_power_range : tuple of int, default (-1,1)
        (optional) Power range not to be transformed to scientific notation
        By default [-1,1) powers will not be transformed

    Returns
    -------
    stat_text : str
        Statistical results in text form
    dict_stats : dict
        Statistical results as dictionary

    References
    ----------
    https://www.wikiwand.com/en/Skewness
    https://www.wikiwand.com/en/Kurtosis
    https://www.wikiwand.com/en/Variance
    https://www.wikiwand.com/en/Coefficient_of_variation
    https://www.wikiwand.com/en/Median
    """
    # mean_vals = []
    # Calculate statistical data
    stat_data = stats.describe(data, axis=0, nan_policy="omit")

    observations = stat_data.nobs
    min_val = stat_data.minmax[0]
    max_val = stat_data.minmax[1]
    mean_val = stat_data.mean  # mu
    var_val = stat_data.variance  # sigma squared
    std_val = np.sqrt(var_val)  # sigma
    cv_val = round(std_val / mean_val * 100)  # in %
    skew_val = stat_data.skewness
    kurt_val = stat_data.kurtosis
    median_val = np.median(data, axis=0)
    # mean_vals.append(mean_val)

    dict_stats = {
        "observations": observations,
        "min_val": min_val,
        "max_val": max_val,
        "mean_val": mean_val,
        "var_val": var_val,
        "std_val": std_val,
        "cv_val": cv_val,
        "skew_val": skew_val,
        "kurt_val": kurt_val,
        "median_val": median_val,
    }

    # ----------------- add-on ------------------------
    summary = {
        "observations": observations,
        "min_val": min_val,
        "max_val": max_val,
        "mean_val": mean_val,
        #         "var_val": var_val,
        #         "std_val": std_val,
        "cv_val": cv_val,
        #         "skew_val": skew_val,
        #         "kurt_val": kurt_val,
    }

    formatted_summary = {}
    num_decimals = 2

    for key in summary:
        if key in ["observations", "cv_val"]:
            formatted_summary[key] = summary[
                key
            ]  # leave "observations" and "cv_val" as they are
        else:
            formatted_summary[key] = turn_to_scientific(
                summary[key], num_decimals, excl_power_range=excl_power_range
            )
    # -------------------------------------------
    # look for symbols here https://matplotlib.org/stable/tutorials/text/mathtext.html
    stat_text = (
        " n = {observations}\n"  # Samples
        #         "\n---------"
        "min = {min_val}\n"
        "max = {max_val}\n"
        r"$\bar x$ = {mean_val}" + "\n"  # $\mu$
        # '\nVariance: {:.2e}'
        #         r"$\sigma$ = {std_val}" + "\n"  ## s
        r"$c_v$ = {cv_val}%"  # + "\n"   ## $c_v$ or $\^{{c_v}}$
        #         "Skewness = {skew_val}\n"
        #         "Kurtosis = {kurt_val}"
    ).format(**formatted_summary)

    return stat_text, dict_stats
