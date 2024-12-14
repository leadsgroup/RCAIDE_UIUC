# RCAIDE/Library/Plots/Geometry/Common/contour_surface_slices.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
import plotly.graph_objects as go   

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------  -Common
def contour_surface_slice(x,y,z,values,color_scale, showscale = False , colorbar_title = None, colorbar_location = 'right', colorbar_orientation = 'v'):
    return go.Surface(x=x,y=y,z=z,surfacecolor=values,colorscale=color_scale, showscale=showscale,
                      colorbar = dict(title = colorbar_title, titleside = "right", orientation = "v")) 

   
