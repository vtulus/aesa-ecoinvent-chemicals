# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 20:22:09 2021

@author: VTulus
"""
__all__ = ["create_glo_market"]

import pandas as pd


def create_glo_market(
    df_in: pd.DataFrame,
    columns_to_allocate: list,
    activity_column: str = "Activity",
    refprod_column: str = "referenceProduct",
    geo_column: str = "geo",
    prodvol_column: str = "referenceProduct_prodVolume",
    comment_column: str = "activity_generalComment",
):
    """Return extended_df populated with new GLO markets.

    Create a GLO market for an activity from 2 or more non-GLO markets of the same activity.
    WARNING (!): columns not selected for allocation will be populated with
    the values of one of the non-GLO market or left empty

    Parameters
    ----------
    df_in : DataFrame
        Dataframe with metadata and LCIA scores
    columns_to_allocate : list
        List of columns with LCIA scores to be allocated
    activity_column : str, default "Activity"
        Column with activity names of a respective market
    refprod_column : str, default "referenceProduct"
        Column with reference product names of a respective market
    geo_column : str, default "geo"
        Column with location of the market
    prodvol_column : str, default "referenceProduct_prodVolume"
        Column with production volumes of a respective market
    comment_column : str, default "activity_generalComment"
        Column where to include the comment about allocation

    Returns
    -------
    extended_df : pd.DataFrame
        Dataframe with additional GLO markets
    """
    df_in = df_in.copy()

    list_inserted_columns = list(
        columns_to_allocate
        + [activity_column, refprod_column, geo_column, prodvol_column, comment_column,]
    )

    if not all(elem in df_in.columns for elem in list_inserted_columns):
        raise ValueError(
            "Some of the provided column labels are not in df_in."
            "\n\tCheck (default) column labels, the inserted `df_in` or `columns_to_allocate`."
        )
    removed_market_groups = []
    for idx in df_in.index:
        if "market group for" in df_in[activity_column][idx]:
            removed_market_groups.append(idx)
    df_in.drop(
        index=removed_market_groups, inplace=True
    )  # drop all "market group for", if any

    duplicated_names = list(
        df_in[df_in[refprod_column].duplicated(keep=False)][refprod_column].unique()
    )  # if a market name has a duplicate, then it should not have GLO market

    # TODO: check this later!!!
    #     nonGLO_market_names = df_in[df_in[geo_column] != "GLO"][refprod_column].tolist()
    #     GLO_market_names = df_in[df_in[geo_column] == "GLO"][refprod_column]
    #     duplicated_nonGLO_market_names = nonGLO_market_names - list(set(nonGLO_market_names))

    duplicated_names_nonGLO = df_in[
        df_in[geo_column] != "GLO"
    ]  # pylint: disable=invalid-name
    single_names_nonGLO = list(  # pylint: disable=invalid-name
        duplicated_names_nonGLO[
            ~duplicated_names_nonGLO[refprod_column].duplicated(keep=False)
        ][refprod_column].unique()
    )  # if a market name has NO duplicates and his geo_column is not "GLO",
    # then it can be considered as GLO market directly, without allocation

    names_to_make_GLO = (
        duplicated_names + single_names_nonGLO
    )  # pylint: disable=invalid-name

    # all not specified columns will take as proxy the values from the first non-GLO market
    columns_to_populate_with_proxy_data = [
        i
        for i in df_in.columns
        if i not in list_inserted_columns and "comment"
        # all columns with comments,except one selected
        not in str(i).lower()
        and "filename" not in str(i).lower()  # column with sourceFilename
    ]

    # ----------------
    extended_df = df_in.copy()
    df_newGLOmarket = pd.DataFrame(
        columns=df_in.columns
    )  # pylint: disable=invalid-name

    for name in names_to_make_GLO:
        # index of duplicated chemical names
        idx = df_in[df_in[refprod_column] == name].index.values
        # sum of production volumes of a chemical with non-GLO markets
        tot_prodvol = df_in.loc[idx][prodvol_column].sum()
        # mass allocation of non-GLO markets
        mass_alloc = df_in.loc[idx][prodvol_column] / tot_prodvol
        # LCIA scores according to mass allocation
        scores = (df_in.loc[idx][columns_to_allocate].mul(mass_alloc, axis=0)).sum()

        # ---- creation of a new GLO market for the chemical ----
        df_newGLOmarket[df_in.columns] = [None] * df_in.columns.size

        # reference product name
        df_newGLOmarket[refprod_column] = [name]

        # change location to GLO
        df_newGLOmarket[geo_column] = ["GLO"]
        # new activity name
        df_newGLOmarket[activity_column] = [name + ", combined to GLO market"]
        # change total production volume to the sum of non-GLO markets
        df_newGLOmarket[prodvol_column] = [tot_prodvol]
        # add new activity comment
        df_newGLOmarket[comment_column] = [
            "Combined activity, mass allocated from "
            + ", ".join(df_in.loc[idx][geo_column])
            + " locations"
        ]
        # include allocated LCIA scores
        df_newGLOmarket[columns_to_allocate] = [scores]

        # columns with proxy metadata values from the first non-GLO market
        df_newGLOmarket[columns_to_populate_with_proxy_data] = [
            df_in.loc[idx[0]][columns_to_populate_with_proxy_data]
        ]

        # append new GLO market to analysis df_in
        extended_df = extended_df.append(df_newGLOmarket, ignore_index=True)

    return extended_df
