# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 17:42:28 2021

@author: VTulus
"""
__all__ = ["plot_categories", "filter_by_geo_and_fu",
           "excluded_products", "find_chemicals"]

import pandas as pd


def plot_categories(
        df_in: pd.DataFrame,
        groupby: str = "category",
        cutoff_value: int = 0,
        **kwargs
):
    """
    Fast bar plot of the number of chemicals per arbitrary category.

    The plot requires a column with categorical values.

    Parameters
    ----------
    df_in : pandas.DataFrame
        DataFrame with categorical data to plot
    groupby: str, default "category"
        Column name of df_in to plot (categorical data)
    cutoff_value : int, default 0
        Hide categories with number of items less than cutoff_value
        0 shows all categories

    Returns
    -------
    A bar plot

    **kwargs
    --------
    Any kwargs for `pandas.DataFrame.plot.barh`
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html#pandas.DataFrame.plot
    """

    data = df_in.groupby(
        by=groupby, sort=True).size().sort_values(ascending=True)

    data_plot = data.where(data >= cutoff_value).dropna()
    data_plot.plot.barh(
        grid=True, title="ºn markets per type of chemical", **kwargs)

    print(df_in.groupby(by=groupby, sort=True).size().sort_values(ascending=False))
    print("Total: ", df_in.shape[0])
    print(
        "\nShares in % for ",
        round(df_in.groupby(by=groupby, sort=True).size() /
              df_in.shape[0] * 100, 2),
    )

# ALTERNATIVE with seaborn ==========================
# counter = pd.DataFrame(df_analysis.groupby(by='category').count().Activity)
# .sort_values(by='Activity', ascending=False)

# dims = (11, 5)
# fig = sns.set_style('whitegrid')
# fig, ax = plt.subplots(figsize=dims)
# ax = sns.countplot(y='category', data=df_analysis, order=counter.index, palette='dark:salmon_r')
# ax.set_xlabel('ºn of activities', fontsize=15, fontweight='bold');
# ax.set_ylabel('Category', fontsize=15, fontweight='bold');
# ax.tick_params(labelsize=12)

# # fig = sns.color_palette("Blues", as_cmap=True)#("dark:salmon_r", as_cmap=True)
# # fig = sns.set(font_scale=2)
# # ax = sns.despine(offset=10, trim=True);
# plt.tight_layout()


def filter_by_geo_and_fu(
        df_in: pd.DataFrame,
        geo: str = "GLO",
        funit: str = "kg"
) -> pd.DataFrame:
    """
    Filter pandas:DataFrame by location(geo) and functional unit(unit).

    Parameters
    ----------
    df_in : pandas.DataFrame
        Input dataframe
    geo : str, default GLO
        Location, df_in should have a column `geo`
    funit : str, default kg
        Funtional unit, df_in should have a column `referenceProductUnit`

    Returns
    -------
    df_filtered_geo_fu : pandas.DataFrame
        Filtered dataframe
    """
    df_filtered_geo = dict(list(df_in.groupby("geo")))[
        geo]  # filtered by selected location
    df_filtered_geo_fu = df_filtered_geo[df_filtered_geo.referenceProductUnit == funit]

    return df_filtered_geo_fu


def excluded_products(
        df_raw: pd.DataFrame,
        df_filtered: pd.DataFrame
):
    """
    Compare products in two pandas.DataFrames

    Compare products in the original (raw) df to products in the filtered df,
    and identify left-out products.

    It is assumed that df_raw and df_filtered have columns:
        `referenceProduct`, `geo` and `referenceProductUnit`

    Parameters
    ----------
    df_raw : pd.DataFrame
        Raw, unfiltered dataframe
    df_filtered : pd.DataFrame
        Filtered dataframe

    Returns
    -------
    df_excluded : pandas.DataFrame
        Dataframe with filtered-out products
    """

    df_raw_refprod = df_raw.referenceProduct
    df_filtered_refprod = df_filtered.referenceProduct
    df_raw_geo = df_raw.geo
    df_raw_funit = df_raw.referenceProductUnit

    print(df_raw_refprod.nunique(), "unique reference products in df_raw")
    print(df_filtered_refprod.nunique(),
          "unique reference products in df_filtered")

    missing = [
        item for item in df_raw_refprod.unique() if item not in df_filtered_refprod.unique()
    ]
    print("-".center(25, "-"))
    print(len(missing), "not included products")
    print("(because they don't satisfy the filtering criteria): \n")

    dictmissing = {}
    for m in missing:
        idx = df_raw_refprod[df_raw_refprod == m].index
        geo = df_raw_geo.loc[idx].values
        unit = df_raw_funit.loc[idx].values
        dictmissing[m] = [geo[0], unit[0]]
    df_excluded = pd.DataFrame.from_dict(
        dictmissing, orient="index", columns=["geo", "unit"]
    )
    df_excluded.index.name = "product"
    df_excluded = df_excluded.sort_values(by=["unit", "geo"])

    return df_excluded


def find_chemicals(
        df_in: pd.DataFrame,
        lst_chemicals: list,
        colname: str = "referenceProduct"
):
    """Filter pandas.DataFrame by list of chemicals.

    Check if chemicals from `lst_chemicals` are in `df_in[colname]`.
    By default, it is assumed that df_in has `referenceProduct` column.
    
    `find_chemicals()` has similar functionality as `filter_dataframe()`
    (!) Consider replacing

    Parameters
    ----------
    df_in : pandas.DataFrame
        Input dataframe
    lst_chemicals : list
        List of chemicals to filter-in
    colname: str, default "referenceProduct"

    Returns
    -------
    Filtered df_in.
    """
    idss = []
    for item in lst_chemicals:
        for idx in df_in.index:
            if item == df_in[colname].loc[idx]:
                idss.append(idx)

    return df_in.loc[idss]
