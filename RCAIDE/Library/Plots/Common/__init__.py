## @defgroup Library-Plots-Performance-Common Common 
# RCAIDE/Library/Plots/Performance/Common/__init__.py
# 

"""
RCAIDE Common Plotting Utilities

This module provides standardized plotting utilities used across RCAIDE's visualization 
capabilities. It includes functions for consistent axis formatting and plot styling.

Modules
-------
set_axes
    Standardized axis formatting function that applies consistent grid lines, 
    tick marks, and numerical formatting across all RCAIDE plots.

plot_style
    Returns standardized plotting parameters including line styles, markers, 
    colors, and font sizes to maintain visual consistency.

Notes
-----
These utilities should be used in all RCAIDE plotting functions to ensure
consistent visualization appearance throughout the package.

**Usage Example**
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
from .set_axes            import set_axes
from .plot_style          import plot_style  