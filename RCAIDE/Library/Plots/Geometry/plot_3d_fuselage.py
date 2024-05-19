## @ingroup Library-Plots-Geometry 
# RCAIDE/Library/Plots/Geometry/plot_3d_fuselage.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Framework.Core import Data
from RCAIDE.Library.Plots.Geometry.Common.contour_surface_slice import contour_surface_slice
import numpy as np  
import plotly.graph_objects as go 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Plots-Geometry 
def plot_3d_fuselage(plot_data,fuselage, tessellation = 24 ,color_map = 'teal'):
    """ This plots the fuselage surface

    Assumptions:
    None

    Source:
    None

    Inputs:
    fuselage             - fuselage data structure
    fuselage_points      - coordinates of fuselage points
    color_map            - color of panel 


    Properties Used:
    N/A
    """
    fuselage_points      = generate_3d_fuselage_points(fuselage,tessellation = 24 )
    num_fus_segs = len(fuselage_points[:,0,0])
    if num_fus_segs > 0:
        tesselation  = len(fuselage_points[0,:,0])
        for i_seg in range(num_fus_segs-1):
            for i_tes in range(tesselation-1):
                X = np.array([[fuselage_points[i_seg  ,i_tes,0],fuselage_points[i_seg+1,i_tes  ,0]],
                              [fuselage_points[i_seg  ,i_tes+1,0],fuselage_points[i_seg+1,i_tes+1,0]]])
                Y = np.array([[fuselage_points[i_seg  ,i_tes  ,1],fuselage_points[i_seg+1,i_tes  ,1]],
                              [fuselage_points[i_seg  ,i_tes+1,1],fuselage_points[i_seg+1,i_tes+1,1]]])
                Z = np.array([[fuselage_points[i_seg  ,i_tes  ,2],fuselage_points[i_seg+1,i_tes  ,2]],
                              [fuselage_points[i_seg  ,i_tes+1,2],fuselage_points[i_seg+1,i_tes+1,2]]])  
                 
                values = np.ones_like(X) 
                verts  = contour_surface_slice(X, Y, Z,values,color_map )
                plot_data.append(verts)          

    return plot_data 

def generate_3d_fuselage_points(fuselage ,tessellation = 24 ):
    """ This generates the coordinate points on the surface of the fuselage

    Assumptions:
    None

    Source:
    None

    Inputs:
    fuselage                  - fuselage data structure

    Properties Used:
    N/A
    """
    num_fus_segs = len(fuselage.Segments.keys())
    fuselage_points      = np.zeros((num_fus_segs,tessellation ,3))

    if num_fus_segs > 0:
        for i_seg, segment in enumerate(fuselage.Segments): 
            a = segment.width/2
            b = segment.height/2
            n = segment.curvature
            theta    = np.linspace(0,2*np.pi,tessellation) 
            fus_ypts =  (abs((np.cos(theta)))**(2/n))*a * ((np.cos(theta)>0)*1 - (np.cos(theta)<0)*1) 
            fus_zpts =  (abs((np.sin(theta)))**(2/n))*b * ((np.sin(theta)>0)*1 - (np.sin(theta)<0)*1)  
            fuselage_points[i_seg,:,0] = segment.percent_x_location*fuselage.lengths.total + fuselage.origin[0][0]
            fuselage_points[i_seg,:,1] = fus_ypts + segment.percent_y_location*fuselage.lengths.total + fuselage.origin[0][1]
            fuselage_points[i_seg,:,2] = fus_zpts + segment.percent_z_location*fuselage.lengths.total + fuselage.origin[0][2]

    return fuselage_points
