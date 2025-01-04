## @ingroup Library-Plots-Performance-Common
# RCAIDE/Library/Plots/Performance/Common/plot_style.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Framework.Core import Data 
 
# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Library-Plots-Performance-Common
def plot_style():
    """
    Create standardized plotting style parameters for visualizations using RCAIDE's standard conventions.

    Returns
    -------
    plot_parameters : Data
        Style parameters with fields:
            - line_width : int
                Width of plot lines, default 2
            - line_style : str
               Style of plot lines, default '-'
            - marker_size : int
                  Size of plot markers, default 8
            - legend_font_size : int
                  Font size for legends, default 12
            - axis_font_size : int
                  Font size for axis labels, default 14
            - title_font_size : int
                  Font size for plot titles, default 18
            - markers : list
                  Collection of marker styles for distinguishing data series
            - color : str
                  Default line color, default 'black'

    Notes
    -----
    Provides consistent styling across all RCAIDE plots including:
         - Line properties (width, style)
         - Marker properties (size, styles)
         - Text properties (font sizes)
         - Color schemes

    The marker list includes a comprehensive set of matplotlib markers
    for distinguishing multiple data series on the same plot.

    **Definitions**

    'Marker'
        Symbol used to highlight individual data points
    
    'Line Style'
        Pattern used for connecting data points

    See Also
    --------
    RCAIDE.Library.Plots.Common.set_axes : Complementary axis styling
    """

    # Universal Plot Settings  
    plot_parameters                  = Data()
    plot_parameters.line_width       = 2 
    plot_parameters.line_style       = '-'
    plot_parameters.marker_size      = 8
    plot_parameters.legend_font_size = 12
    plot_parameters.axis_font_size   = 14
    plot_parameters.title_font_size  = 18    
    plot_parameters.markers          = ['o', 's', '^', 'X', 'd', 'v', 'P', '>','.', ',', 'o', 'v', '^', '<',\
                                        '>', '1', '2', '3', '4', '8', 's', 'p', '*', 'h'\
                                         , 'H', '+', 'x', 'D', 'd', '|', '_'] 
    plot_parameters.color            = 'black'
    
    return plot_parameters