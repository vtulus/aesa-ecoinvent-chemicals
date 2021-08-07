# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 12:41:45 2021

@author: VTulus
"""
# incorporate this funtion to histogram func
__all__ = ["fix_hist_cdf_drop_line_at_end"]

import matplotlib as mpl


def fix_hist_cdf_drop_line_at_end(ax):
    """Removes the vertical line at the end of a CDF plotted with `plot_histogram`.

    `plot_histogram` IS NOT IMPLEMENTED YET.

    Parameters
    ----------
    ax : mpl.axes
        DESCRIPTION. Pending...

    Returns
    -------
    None

    References
    ----------
    Adapted from https://stackoverflow.com/a/52921726/14485040
    """
    axpolygons = [
        poly for poly in ax.get_children() if isinstance(poly, mpl.patches.Polygon)
    ]
    for poly in axpolygons:
        poly.set_xy(poly.get_xy()[:-1])
