# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 11:46:12 2021

@author: VTulus
"""
__all__ = ["turn_to_scientific"]


def turn_to_scientific(val: float, n_decimals: int, excl_power_range: int = (-1, 1)) -> str:
    """Converts values to scientific notation of the type N x 10^m.

    Parameters
    ----------
    val : float
        Value to (possibly) transform to scientific notation
    n_decimals : int
        Number of decimals of the leading digit
    excl_power_range : tuple of int, default (-1,1)
        (optional) Power range not to be transformed to scientific notation
        By default [-1,1) powers will not be transformed

    Returns
    -------
    sci_val: str
        Value transformed into scientific notation of the type n.nn x 10^m

    Notes
    -----
    Adapted from https://stackoverflow.com/a/31453961/14485040
    """

    left, right = excl_power_range

    s = "{x:.{ndp:d}e}".format(
        x=val, ndp=n_decimals)  # pylint: disable=invalid-name
    digits, power = s.split("e")
    if (
        int(power) not in range(left, right)
    ):  # power is not in provided range -> transform
        sci_val = r"${dig:s}\times 10^{{{pw:d}}}$".format(
            dig=digits, pw=int(power))
    else:  # -> leave unchanged
        sci_val = "{x:.{ndp:d}f}".format(x=val, ndp=n_decimals)

    return sci_val
