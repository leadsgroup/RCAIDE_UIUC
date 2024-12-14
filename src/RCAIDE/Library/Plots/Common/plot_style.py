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
def plot_style():
    """Helper function for automatically setting the style of plots to the
    RCAIDE standard style.

    Use immediately before showing the figure to ensure all necessary
    information is available and to avoid over-writing style when
    constructing the figure. 

    Assumptions:
    None

    Source:
    None

    Inputs:
       None 

    Outputs: 
       Plotting style parameters 

    Properties Used:
    N/A	
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