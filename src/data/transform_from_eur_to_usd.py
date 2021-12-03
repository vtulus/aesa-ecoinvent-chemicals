# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 16:41:52 2021

@author: VTulus
"""

__all__ = ["transform_from_eur_to_usd"]

import re
import warnings

import pandas as pd


def transform_from_eur_to_usd(
        prices_in: pd.Series,
        currency_in: str,
        year_out: int = 2018,
        usd_per_eur: float = 1.1811,
        adjust_inflation: bool = True,
        **inflation_kwargs):
    """Transforms prices from `currency_in` to USD`year_out`.

    Returns pd.Series of transformed prices and a string of the `currency_out`.
    `currency_in` is expected to be EURyyyy.
    Optionally performs an adjustment for inflation using Producer Price Index from
    Eurostat (in EU28).

    Parameters
    ----------
    prices_in : pandas.Series
        Series of prices to be transformed from `currency_in` to USD`year_out`
    currency_in : str
        Currency of `prices_in` in format [A-Z]{3}[0-9]{4}
    year_out : int, default 2018
        Year for the adjusted prices `prices_out`
    usd_per_eur : float, default 1.1811
        Average exchange rate EUR`year_out` to USD`year_out`. Default value is for `year_out=2018`
    adjust_inflation : bool, default True
        If True, inflation is taken into account using PPI from Eurostat (in EU28)

    **inflation_kwargs
    ------------------
    ppi_in : float, default 86.0
        Producer Price Index from Eurostat (in EU28), in EUR2005
        Value should be for the same year as `currency_in`
    ppi_out : float, default 104.5
        Producer Price Index from Eurostat (in EU28), in EUR2018
        Value should be for the same year as `year_out`

    Raises
    ------
    AttributeError
        If the format of `currency_in` is not correct
    ValueError
        - If `ppi_in` and/or `ppi_out` are not passed, or passed not as float type
        - If `adjust_inflation=False`, but year_in and year_out do not match

    Returns
    -------
    prices_out : pandas.Series
        Series of transformed prices, in USD for year `years_from_to[1]`
    currency_out : str
        Currency of `prices_out` in format [A-Z]{3}[0-9]{4}

    Notes
    -----
    `prices_in` by default are expected to be in EUR2005, they are conveniently:
        1. adjusted to current year EURO (default: EUR2018) and
        2. converted to USD2018
    1. Adjustment of prices according to the Producer Price Index from Eurostat, where
    PPI EU28 2005 = 86.0
    PPI EU28 2018 = 104.5
    Refs:
    https://ec.europa.eu/eurostat/statistics-explained/index.php/Industrial_producer_price_index_overview
    https://ec.europa.eu/eurostat/web/products-datasets/-/sts_inpp_a
    2. Average exchange rate in 2018:
    1 EUR = 1.1811 USD
    Ref:
    https://www.exchangerates.org.uk/EUR-USD-spot-exchange-rates-history-2018.html
    """
    currency_out = "USD"+str(year_out)

    if currency_in != currency_out:
        regex_currency = re.compile(r"([A-Z]{3})([\d]{4})")
        mobj = regex_currency.match(currency_in)
        # should match 2 groups: (1) 3-digit currency and (2) 4-digit year
        try:
            year_in = int(mobj.group(2))
        except AttributeError:
            raise AttributeError("The format of `currency_in` is not correct. Must be "
                                 "[A-Z]{3}[0-9]{4}, e.g., EUR2005.") from None

        warnings.warn("(!) Make sure that passed `usd_per_eur={}` is for {}\n"
                      "".format(usd_per_eur, year_out))

        if adjust_inflation:
            if (year_in, year_out) == (2005, 2018):
                ppi_in = 86.0  # from Eurostat (in EU28), in EUR2005
                ppi_out = 104.5  # from Eurostat (in EU28), in EUR2018
            else:
                ppi_in = inflation_kwargs.get("ppi_in", "not provided")
                ppi_out = inflation_kwargs.get("ppi_out", "not provided")
            if not all(isinstance(var, float) for var in [ppi_in, ppi_out]):
                raise ValueError("`ppi_in` for {} and `ppi_out` for {} must be provided "
                                 "as dtype=float, because `adjust_inflation=True`."
                                 "".format(year_in, year_out))
            inflation_ratio = ppi_out/ppi_in
            print("You transformed the prices from {0} to USD{2} and applied an "
                  "adjustment for inflation using Producer Price Index for years "
                  "{1}-{2}".format(currency_in, year_in, year_out))
        else:
            if year_in != year_out:
                raise ValueError("You decided to avoid adjustment for inflation "
                                 "(`adjust_inflation=False`), but the years of "
                                 "`currency_in` ({}) and `year_out={}` do not match..."
                                 "\nThis must be corrected.".format(year_in, year_out))
            inflation_ratio = 1  # do not adjust for inflation
            print("You transformed the prices from {0} to USD{2} without any adjustment "
                  "for inflation, because year_in({1}) and year_out({2}) are the same."
                  "".format(currency_in, year_in, year_out))
        # --- Adjust prices ---
        prices_out = prices_in.mul(inflation_ratio).mul(usd_per_eur)
    else:
        print("`currency_in` is already in a {}. No transformation is performed..."
              "".format(currency_out))
        prices_out = prices_in

    return prices_out, currency_out
