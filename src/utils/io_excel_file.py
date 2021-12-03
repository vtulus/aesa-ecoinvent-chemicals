# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 17:15:36 2021

@author: VTulus
"""
__all__ = ["read_excel_to_pandas", "write_pandas_to_excel"]

from pathlib import Path

import pandas as pd


def read_excel_to_pandas(
        path_to_file: str,
        filename: str,
        sheets=0,
        show_readme=True,
        **kwargs
):
    """Reads an Excel file and returns pandas dataframe per sheet.

    If multiple sheets are read, returns a dict with k=sheet_name, v=pd.DataFrame.
    Based on `pandas.read_excel` function.
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html

    Parameters
    ----------
    path_to_file : str
        Absolute path to the Excel file
    filename : str
        File name with extension
    sheets : str, int, list, or None, default 0
        Sheet name(s) to read
        If 0, read 1st sheet {omits "readme" sheet if present}
        If "Sheet1", read sheet with name "Sheet1"
        If [0,1, "Sheet5"], read 1st, 2nd, and sheet named "Sheet5"
        If None, read all sheets
    show_readme : bool, default True
        If True, prints out readme information (if available)
        If False, does not print anything

    **kwargs
    --------
    engine : str, default None
        Supported engines: "xlrd", "openpyxl", "odf", "pyxlsb"
    Other kwargs as in
    https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html

    Returns
    -------
    df_out : DataFrame
        Pandas dataframe with sheet(s) content

    Example
    -------
    If 1 sheet is read:
    df_out = read_excel_to_pandas(
        "path/to/excel/file",
        "file.xlsx",
        sheets="Sheet1", # or sheets=0,
        show_readme=True,
        engine="openpyxl"
        )
    If all/multiple sheets are read:
    dict_out = read_excel_to_pandas(
        "path/to/excel/file",
        "file.xlsx",
        sheets=None, # or sheets=["Sheet1", "Sheet3"]
        show_readme=False,
        engine="openpyxl"
        )
    """

    # Default kwargs ----
    engine = kwargs.get("engine", None)
    kwargs_pass_on = {
        k: v for k, v in kwargs.items() if k not in ["engine"]
    }  # for pd.read_excel

    excel_file_path = Path(path_to_file, filename)
    xl_obj = pd.ExcelFile(excel_file_path, engine=engine)
    # if default (first sheet) is selected, remove "readme" sheet in case it exists
    if sheets == 0:
        sheets_list = xl_obj.sheet_names
        # sheet with information about the dataset
        sheets_list.remove("readme")
        df_out = pd.read_excel(
            xl_obj, sheet_name=sheets_list[sheets], **kwargs_pass_on)
    else:
        df_out = pd.read_excel(xl_obj, sheet_name=sheets, **kwargs_pass_on)

    # try printing out the description of the excel file

    if show_readme and "readme" in xl_obj.sheet_names:
        print("\n===> Trying to load 'readme' data... ===")
        df_readme = pd.read_excel(
            xl_obj, sheet_name="readme", header=None, index_col=0)
        try:
            # based on index labels returned
            # by make_readme_info() func
            print("File: {} from\n{}\n"
                  "Generated on {} by {}\n"
                  "Includes:\n<<<\n{}\n>>>".format(
                      df_readme.loc["file name"][1],
                      df_readme.loc["python script"][1],
                      df_readme.loc["file generation date"][1],
                      df_readme.loc["author"][1],
                      df_readme.loc["file description"][1]
                  )
                  )
        except:  # pylint: disable=bare-except
            print("Couldn't automatically get the 'readme' data...\n"
                  "\tHint: 'readme' was not created with "
                  "`make_readme_info()` or was manually altered.")
        print("========================================\n")
    return df_out


def write_pandas_to_excel(
        path_to_file: str,
        filename: str,
        dict_data_to_write: dict,
        readme_info=("readme", pd.DataFrame()),
        engine="xlsxwriter",
        **readme_kwargs,
):
    """Writes pandas dict into an Excel file.

    Pandas dict_data_to_write with k=sheet_name, v=pd.DataFrame has to be provided.
    Based on `pandas.ExcelWriter` class.
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.ExcelWriter.html

    Parameters
    ----------
    path_to_file : str
        Absolute path to the Excel file
    filename : str
        File name with extension
    dict_data_to_write : dict
        Dictionary with k=sheet_name, v=pd.DataFrame
    readme_info : tuple, default ("readme", pd.DataFrame())
        Tuple with first element `str`-like, second element readme information of type(pd.DataFrame)
    engine : str, default "xlsxwriter"
        Engine to use for writing.

    **readme_kwargs passed as arguments to pandas.DataFrame.to_excel
    ---------------
    header : bool or list of str, default False
        Write out the column names.
        If a list of string is given it is assumed to be aliases
        for the column names.
    index : bool, default False
        Write row names (index).
    startrow : int, default 0
        Upper left cell row to dump data frame.
    Other arguments here
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html

    Returns
    -------
    Creates xlsx file

    Example
    -------
    write_pandas_to_excel(
        path_to_file="path/to/output/directory",
        filename="new_file.xlsx",
        dict_data_to_write={"Sheet1": pd.DataFrame, "Sheet2": pd.DataFrame},
        readme_info=("Sheet_readme", pd.DataFrame),
        engine="xlsxwriter",
        startrow=1
        )
    """

    # Default readme_kwargs ----
    header = readme_kwargs.get("header", False)
    index = readme_kwargs.get("index", False)
    startrow = readme_kwargs.get("startrow", 0)
    readme_kwargs_pass_on = {
        k: v
        for k, v in readme_kwargs.items()
        if k not in ["header", "index", "startrow"]
    }

    with pd.ExcelWriter(  # pylint: disable=abstract-class-instantiated
        Path(path_to_file, filename),
        engine=engine,
        options={
            "strings_to_urls": False,  # when df contains too many URLs
            "strings_to_formulas": False,
        },
        # **excel_writer_kwargs_pass_on,
    ) as writer:
        if not isinstance(readme_info[1], pd.DataFrame):
            raise TypeError("The second element of `readme_info` must be a "
                            "pandas.DataFrame containing optional readme information."
                            "\nIf readme to be omitted, leave default settings, i.e.,"
                            "`('readme', pd.DataFrame())`")
        if not readme_info[1].empty:
            readme_info[1].to_excel(
                writer,
                sheet_name=readme_info[0],
                header=header,
                index=index,
                startrow=startrow,
                **readme_kwargs_pass_on
                #                 encoding="UTF-8",
            )
        else:  # readme_info[1] is empty, readme_info is omitted
            pass
        for k in dict_data_to_write:
            dict_data_to_write[k].to_excel(
                writer,
                sheet_name=k,
                index=False,
                #                 encoding="UTF-8",
            )

    print("File: {} successfully created in "
          "\n{}".format(filename, path_to_file))
