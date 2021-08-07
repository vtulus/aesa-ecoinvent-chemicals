# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 12:45:00 2021

@author: VTulus
"""
__all__ = ["calculate_transgression_pb"]

import re
import warnings

import numpy as np
import pandas as pd

if __package__:
    from .pb_constants import CURRENT_PB_SCORE, SOS_PB_LCIA, SOS_PB_SALA


def calculate_transgression_pb(
    df_in: pd.DataFrame, sharing_principle=None, **kwargs,
):
    """Calculate transgression levels (TLs) of detected PB-method columns.

    Applicable ONLY to Planetary Boundaries methods
    (detected automatically):
    - based on Ryberg et al. 2018
    https://doi.org/10.1016/j.ecolind.2017.12.065
    - based on Sala et al. 2020
    https://doi.org/10.1016/j.jenvman.2020.110686

    Parameters
    ----------
    df_in : pandas.DataFrame
        Dataframe with at least 1 column containing PBs-LCIA
        category impacts. These impact scores will be compared
        against a specific safe operating space (SOS) values.
    sharing_principle : str or None, default None
        If None, no sharing principle is applied, i.e.,
            TLs = PB impact scores / SOS_total for each detected PB
        IF "epc", equal-per-capita sharing principle is applied, i.e.,
            TLs = PB impact scores * `gva_world` / (SOS_total * prices) for each PB
        If "gf", grandfathering sharing principle is applied, i.e.,
            TLs =  `CURRENT_PB_SCORE` / SOS_total for each PB (one TL per PB)

    **kwargs
    --------
    price_column_label : str, default "referenceProduct_price"
        Column label with price values, only needed for `epc`
    gva_world : float, default 7.38e13
        Gross value added at basic prices of the world, default currency: Int$2018
        Only needed for `epc`
        Refs:
            GVA data: https://data.worldbank.org/indicator/NY.GDP.FCST.CD
            Int$ == USD, see https://www.wikiwand.com/en/International_dollar
        Data should be for the same year as currency of passed prices.

    Raises
    ------
    KeyError
        If `price_column_label` column label does not exist in `df_in`
    ValueError
        If `sharing_principle` is not a valid string

    Returns
    -------
    df_transgression_pb : DataFrame
        Data frame with calculated transgression levels (TL)
    tl_method_labels : list
        List of auto-detected PB method label(s), for which TL was calculated

    Notes
    -----
    - `gf` does not work with Sala et al. method, no current PB values are provided.
    - more recent GVA not available...

    Other (NOT USED)
    -----
    - GDP world for 2019
    - GDP2020 = 13.835e+13 Int$
    ref: https://www.statista.com/statistics/268750/global-gross-domestic-product-gdp/
    """
    all_columns = list(df_in.columns)

    # Auto-match the PB method and its categories
    dict_sos, dict_current_pb = _match_pb_method(all_columns)

    df_sos = pd.DataFrame.from_dict(dict_sos, orient="index", dtype=float).T
    df_current_pb = pd.DataFrame.from_dict(
        dict_current_pb, orient="index", dtype=float
    ).T
    df_impact_pb = df_in[df_sos.columns]

    tl_method_labels = ["TL in " + column for column in df_sos.columns]

    if not sharing_principle:  # use the total SOS
        # Compute transgression level
        df_transgression_pb = df_impact_pb.div(df_sos.to_numpy(), axis=1)
        df_transgression_pb.columns = tl_method_labels  # rename columns

    elif sharing_principle == "epc":  # equal-per-capita principle
        # Extract kwargs
        price_column_label = kwargs.get("price_column_label", "referenceProduct_price")
        gva_world = kwargs.get("gva_world", 7.38e13)  # USD2018
        try:
            df_prices = df_in[price_column_label]
        except KeyError:
            raise KeyError(
                "`{}` column label does not exist in `df_in`."
                "\nA valid `price_column_label` has to be passed as "
                "dtype=str when using `sharing_principle='epc'`"
                ".".format(price_column_label)
            ) from None
        if gva_world == 7.38e13:
            warnings.warn(
                "With `sharing_principle='epc' you are using the "
                "default `gva_world=7.38e13` (USD2018) parameter. "
                "Make sure the currency of used prices is also USD2018."
            )
        else:
            warnings.warn(
                "With `sharing_principle='epc' you are using the "
                "`gva_world={}` parameter. Make sure its value is "
                "correct and its currency matches the prices currency"
                ".".format(gva_world)
            )
        # Compute transgression level
        df_transgression_pb = (
            df_impact_pb.mul(gva_world)
            .div(df_prices.to_numpy(), axis=0)
            .div(df_sos.to_numpy(), axis=1)
        )
        tl_method_labels = ["(epc) " + label for label in tl_method_labels]
        df_transgression_pb.columns = tl_method_labels  # rename columns

    elif sharing_principle == "gf":  # grandfathering principle
        # Compute transgression level
        df_transgression_pb = pd.DataFrame(
            np.repeat(
                df_current_pb.to_numpy() / df_sos.to_numpy(), df_in.index.size, axis=0
            ),
            index=df_in.index,
            columns=df_sos.columns,
        )
        tl_method_labels = ["(gf) " + label for label in tl_method_labels]
        df_transgression_pb.columns = tl_method_labels  # rename columns

    else:
        raise ValueError(
            "`sharing_principle` must be a valid "
            "string or None."
            "\nAvailable string options: `epc` for "
            "equal-per-capita, `gf` for "
            "grandfathering sharing principles."
        )

    not_altered_columns = list(filter(lambda a: a not in tl_method_labels, all_columns))

    # Concat TL methods to `df_in`
    df_out = pd.concat([df_in[not_altered_columns], df_transgression_pb], axis=1)

    return df_out, tl_method_labels


def _match_pb_method(all_columns: list,):
    """Auto-match the PB method and its categories.

    Possible options are:
        - Ryberg et al. 2018, which contains `PBs-LCIA` in its labels
        - Sala et al. 2020, which contains `PBs - Alternative` in its labels

    Parameters
    ----------
    all_columns : list
        List of all `df_in`'s columns passed as parameter in
        `calculate_transgression_pb` func.

    Raises
    ------
    ValueError
        If `df_in` does not contain at least one column with
        a category of PB-type method

    Returns
    -------
    dict_sos : dict
        Dictionary of keys dependent on the detected PB method and respective
        values of safe operating space (SOS)
    dict_current_pb : dict
        Dictionary of keys dependent on the detected PB method and respective
        values of safe operating space (SOS)

    Notes
    -----
    `dict_current_pb` not available for Sala et al. method, no current PB
    values are provided
    """
    # Ryberg et al. 2018, which contains `PBs-LCIA`
    ryberg_method = re.compile(r"^(?!TL in )(.*PBs-LCIA.*)")
    # Sala et al. 2020, which contains `PBs - Alternative`
    sala_method = re.compile(r"^(?!TL in )(.*PBs - Alternative.*)")

    # Auto-match PB category depending on matched method
    dict_sos = {}
    dict_current_pb = {}
    for label in all_columns:
        mo_r = ryberg_method.match(label)
        mo_s = sala_method.match(label)
        if mo_r:  # match Ryberg method
            for key, value in SOS_PB_LCIA.items():
                regex_key = re.compile("(.*" + key + ".*)")
                mobj = regex_key.match(label)
                if mobj:
                    dict_sos[label] = value
            for key, value in CURRENT_PB_SCORE.items():
                regex_key = re.compile("(.*" + key + ".*)")
                mobj = regex_key.match(label)
                if mobj:
                    dict_current_pb[label] = value
        elif mo_s:  # match Sala method
            for key, value in SOS_PB_SALA.items():
                regex_key = re.compile("(.*" + key + ".*)")
                mobj = regex_key.match(label)
                if mobj:
                    dict_sos[label] = value
    if not dict_sos:
        raise ValueError(
            "None of `df_in`'s column labels could be matched "
            "against Ryberg et al. 2018 or Sala et al. 2020 "
            "methods. \nNo transgression levels are calculated."
        )

    return dict_sos, dict_current_pb
