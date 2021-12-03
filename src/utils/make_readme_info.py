# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 13:39:52 2021

@author: VTulus
"""
__all__ = ["make_readme_info"]

import datetime

import ipynbname
import pandas as pd


def make_readme_info(
        filename: str,
        file_description: str = "",
        author: str = "Tulus, V."
):
    """
    Create a readme dataframe for an output excel file.

    Parameters
    ----------
    filename : str
        File name with extension (destination excel file)
    file_description: str, (optional)
        Relevant information about the data in the file
    author : str, default "Tulus, V."
        Author's name

    Returns
    -------
    pandas.DataFrame with
        - file name
        - absolute path to the python script which generated the file
        - date of generation of the file
        - description of the data in the file
        - name of the author
    """

    nb_path = ipynbname.path()  # full path to the notebook where this code is executed
    date = datetime.datetime.now().strftime("%Y-%m-%d (%A), %H:%M:%S")
    _dict = {
        "file name": [filename],
        "python script": [nb_path],
        "file generation date": [date],
        "file description": [file_description],
        "author": [author],
    }

    return pd.DataFrame(data=_dict).T.reset_index()

# the problem below was solved after restarting the PC...
# ipynbname takes around 20s to run, find a better solution later

# !pip install line_profiler
# in notebook:
# %load_ext line_profiler
# %lprun -f make_readme_info make_readme_info(args)

# output:
# Timer unit: 1e-07 s
# Total time: 20.7545 s
# File: C:\Users\ViteksPC\Documents\00-ETH_projects\17-LCIA_methods_analysis
# \src\utils\make_readme_info.py
# Function: make_readme_info at line 13

# Line #      Hits         Time  Per Hit   % Time  Line Contents
# ==============================================================
#     13                                           def make_readme_info(
#     14                                                   filename: str,
#     15                                                   file_description: str = "",
#     16                                                   author: str = "Tulus, V."
#     17                                           ):
#     18                                               """
#     19-37                                            Description...
#     38                                               """
#     39
#     40         1  207493230.0 207493230.0    100.0      nb_path = ipynbname.path()
#                      # full path to the notebook where this code is executed
#     41         1        335.0    335.0      0.0      date = datetime.datetime.now()
#                                                .strftime("%Y-%m-%d (%A), %H:%M:%S")
#     42         1         10.0     10.0      0.0      _dict = {
#     43         1          8.0      8.0      0.0          "file name": [filename],
#     44         1          6.0      6.0      0.0          "python script": [nb_path],
#     45         1          6.0      6.0      0.0          "file generation date": [date],
#     46         1          6.0      6.0      0.0          "file description": [file_description],
#     47         1          5.0      5.0      0.0          "author": [author],
#     48                                               }
#     49
#     50         1      51155.0  51155.0      0.0      return pd.DataFrame(data=_dict)
#                                                                     .T.reset_index()
