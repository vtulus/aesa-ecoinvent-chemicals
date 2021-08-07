# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 19:57:58 2021

@author: VTulus
"""
__all__ = ["filter_dataframe"]

import numpy as np
import pandas as pd


def filter_dataframe(
    df_in: pd.DataFrame,
    col_name: str,
    filter_in: list = None,
    filter_out: list = None,
    exact_match: bool = False,
    print_unique: bool = False,
):
    """Return dataframe filtered by the contents in a specified column.

    Filter `df_in[col_name]` according to filter parameters.

    Parameters
    ----------
    df_in: pd.DataFrame
        Input dataframe
    col_name : str
        Label of the column to be filtered
    filter_in : list, default None
        List of items to include in the filter
    filter_out : list, default None
        List of items to exclude from the filter

        For both, filter_in and filter_out:
        If a list is passed, its items are connected with OR operator
        If a list of sub-lists is passed, the items of every sub-list are
            connected with AND operator
        If None, filtering is not performed

    exact_match : bool, default False
        If True, passed items in filter_in and/or filter_out should
            match exactly the content of a cell in column
        If False, passed items in filter_in and/or filter_out are
            matched approximately to the content of a cell in column (case-sensitive)
    print_unique : bool, default False
        Print the list of unique values in filtered column

    Returns
    -------
    Filtered df_in

    Example
    -------
    df_out = filter_dataframe(
        df_in,
        col_name="Column1",
        filter_in=["a", "b", "c"],
        filter_out=None,
        exact_match=True,
        print_unique=False
        )
    """

    df_old = df_in.copy()
    data = df_in[col_name].replace(
        np.nan, "(empty)", regex=True, inplace=False
    )  # take care of NaN rows
    if exact_match:
        if filter_in:
            list_included = []
            for item in data:
                for it_in in filter_in:
                    if isinstance(it_in, list):
                        # Raise error: Cannot pass sub-lists for exact match
                        raise ValueError(
                            "Cannot pass sub-lists as part of the filter when `exact_match=True`"
                        )
                    if it_in == item:
                        list_included.append(item)
            unique_list_included = list(set(list_included))
        else:
            unique_list_included = data
        if filter_out:
            list_removed = []
            for item in unique_list_included:
                for it_out in filter_out:
                    if isinstance(it_out, list):
                        # Raise error: Cannot pass sub-lists for exact match
                        raise ValueError(
                            "Cannot pass sub-lists as part of the filter when `exact_match=True`"
                        )
                    if it_out == item:
                        list_removed.append(item)
            filtered = [
                x for x in unique_list_included if x not in list_removed]
        else:
            filtered = unique_list_included
        unique_filtered_items = list(set(filtered))  # unique
    else:
        if filter_in:
            list_included = []
            for item in data:
                for it_in in filter_in:
                    if isinstance(it_in, list):
                        if all(sub_it_in in item for sub_it_in in it_in):
                            list_included.append(item)
                    else:
                        if it_in in item:
                            list_included.append(item)
            unique_list_included = list(set(list_included))
        else:
            unique_list_included = data
        if filter_out:
            list_removed = []
            for item in unique_list_included:
                for it_out in filter_out:
                    if isinstance(it_out, list):
                        if all(sub_it_out in item for sub_it_out in it_out):
                            list_removed.append(item)
                    else:
                        if it_out in item:
                            list_removed.append(item)
            filtered = [
                x for x in unique_list_included if x not in list_removed]
        else:
            filtered = unique_list_included
        unique_filtered_items = list(set(filtered))  # unique

    if print_unique:
        print(
            "List of unique items matching your request:\n\t\t",
            unique_filtered_items,
            "\n",
        )
    idx_list = []
    for item in unique_filtered_items:
        for idx in df_old.index:
            if item == df_old[col_name].loc[idx]:
                idx_list.append(idx)
    df_out = df_old.loc[idx_list]
    return df_out
