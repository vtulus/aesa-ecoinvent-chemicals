# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 11:22:28 2021

@author: VTulus
"""
__all__ = ["create_fig"]

import matplotlib as mpl
import matplotlib.pyplot as plt


def create_fig(size_in_mm=(171, 200),
               dpi=600,
               label_fontsize=7,
               legend_fontsize=8,
               tick_fontsize=6
               ):
    """Creates a figure and passes some basic specifications.

    Parameters
    ----------
    size_in_mm : tuple, default (171,200)
        Size of the figure in mm, (width, height)
    dpi : float, default 600
        Resolution of the figure in dpi (dots-per-inch)
    label_fontsize : float, default 7
        Font size of the labels on all Axes
    legend_fontsize : float, default 8
        Font size of the text in the legend
    tick_fontsize : float, default 6
        Font size of the x and y ticks

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object with no Axes
    """
    # Figure specifications (fonts, sizes, figsize, etc.)
    mpl.rc("xtick", labelsize=tick_fontsize)
    mpl.rc("ytick", labelsize=tick_fontsize)
    mpl.rc("axes", labelsize=label_fontsize, linewidth=0.6)
    mpl.rc("font", family="Arial")
    mpl.rc("mathtext", default="regular")
    mpl.rc("legend", fontsize=legend_fontsize)

    fig = plt.figure(
        figsize=[x / 25.4 for x in size_in_mm],
        dpi=dpi,
        #  tight_layout = {'pad': 0}
    )

    return fig
