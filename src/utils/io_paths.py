# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 08:46:44 2021

@author: VTulus
"""
__all__ = ["explore_dir", "set_outputs_dir"]

import glob
import os
import pprint
from pathlib import Path


def explore_dir(
    path_to_dir: str,
    file_extension: str = "xlsx",
    print_files_list=True,
):
    """Explores a directory for specific file types.

    Returns absolute path of the explored directory.
    Returns the list of files matching the desired extension (if any) and
    (optionally) prints out this list.

    Parameters
    ----------
    path_to_dir : str
        Path of a directory to explore. Accepts valid absolute paths or
        paths relative to the executed script, i.e., '../path/to/dir'
        (empty string = current directory)
    file_extension : str, default "xlsx"
        Extension of files to search inside `path_to_dir`
    print_files_list  : bool, default True
        If True, prints the list of found files
        If False, does not print anything

    Raises
    ------
    FileNotFoundError
        If `path_to_dir` does not exist

    Returns
    -------
    path_explored_dir : str
        Absolute path of the explored directory
    files_list : list
        List of files with matching extension

    Note
    ----
    If backslashes are used while providing a relative path,
    the string must be raw, i.e., prefixed with 'r'.
    If forwardslashes (/) are used, the string does not has to be raw.

    Example
    -------
    p_explored, f_lst = explore_dir(
        path_to_dir=r"path/to/directory", # absolute or relative path
        file_extension="xlsx",
        print_files_list=True, # print out files as list
        )
    """
    current_dir = Path("").resolve(strict=True)  # abspath to current directory
    passed_path = Path(path_to_dir)
    try:
        path_explored_dir = passed_path.resolve(
            strict=True)  # make the path absolute
    except FileNotFoundError:
        raise FileNotFoundError("The system cannot find the specified directory:"
                                "{}"
                                "\nCheck `path_to_dir`, if relative path is provided, "
                                "it must be relative to the current "
                                "script's directory.".format(passed_path)) from None
    os.chdir(path_explored_dir)  # move cd to path_explored_dir
    files_list = glob.glob("*.{}".format(file_extension))
    if print_files_list:
        pprint.pprint(files_list)

    os.chdir(current_dir)  # return to current directory

    return path_explored_dir, files_list


def set_outputs_dir(
        use_default: bool = True,
        **kwargs
):
    """Returns absolute path for an output directory.

    By default, tries to resolve the abspath to '..data/interim'. If another
    relative path is provided, requires it to be valid, otherwise
    FileNotFoundError is raised. (cannot create new output directory)

    Parameters
    ----------
    use_default : bool, default True
        If True, default '..data/interim' is set as output

    **kwargs
    --------
    rel_path_output : str
        Manually provide a relative path to the output directory

    Raises
    ------
    FileNotFoundError
        If the provided or the default paths are not valid

    Returns
    -------
    abs_path_output : str
        Absolute path of the output directory

    Note
    ----
    If backslashes are used while providing a relative path,
    the string must be raw, i.e., prefixed with 'r'.
    If forwardslashes (/) are used, the string does not has to be raw.

    Example
    -------
    p_output = outputs_dir() # points to default '../data/interim'
    p_output = outputs_dir(use_default=False, rel_path_output='../other/rel/path')
    """
    if use_default:
        rel_path_output = r"..\data\interim"
    else:
        rel_path_output = kwargs.get("rel_path_output", "not provided")
    try:
        abs_path_output = Path(rel_path_output).resolve(strict=True)
    except FileNotFoundError:
        raise FileNotFoundError("The system cannot find the specified directory:"
                                "{}"
                                "\nIf `use_default=False`, must provide a valid "
                                "relative path to output directory using "
                                "`rel_path_output` kwarg.\nIf `use_default=True`, "
                                "make sure that the relative path '../data/interim' "
                                "exists. If it doesn't, set `use_default` "
                                "to False and provide a valid `rel_path_output`"
                                ".".format(rel_path_output)) from None
    return abs_path_output
