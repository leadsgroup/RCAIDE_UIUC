## @ingroup Library-Plots-Geometry
# RCAIDE/Library/Plots/Geometry/plot_3d_nacelle.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
import RCAIDE
from RCAIDE.Library.Plots.Geometry.Common.contour_surface_slice import contour_surface_slice
from RCAIDE.Library.Methods.Geometry.Airfoil import import_airfoil_geometry
from RCAIDE.Library.Methods.Geometry.Airfoil import compute_naca_4series 

import numpy as np 
import plotly.graph_objects as go 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Plots-Geometry 
def plot_3d_nacelle(plot_data,nacelle,tessellation = 24,number_of_airfoil_points = 21,color_map= 'darkmint'):
    """ This plots a 3D surface of a nacelle  

    Assumptions:
    None

    Source:
    None 
    
    Inputs:
    axes                       - plotting axes 
    nacelle                    - RCAIDE nacelle data structure
    tessellation               - azimuthal discretization of lofted body 
    number_of_airfoil_points   - discretization of airfoil geometry 
    color_map                  - face color of nacelle  

    Properties Used:
    N/A
    """

    nac_pts = generate_3d_nacelle_points(nacelle,tessellation,number_of_airfoil_points)    

    num_nac_segs = len(nac_pts[:,0,0])
    tesselation  = len(nac_pts[0,:,0]) 
    for i_seg in range(num_nac_segs-1):
        for i_tes in range(tesselation-1):
            X = np.array([[nac_pts[i_seg  ,i_tes  ,0],nac_pts[i_seg+1,i_tes  ,0]],
                 [nac_pts[i_seg  ,i_tes+1,0],nac_pts[i_seg+1,i_tes+1,0]]])
            Y = np.array([[nac_pts[i_seg  ,i_tes  ,1],nac_pts[i_seg+1,i_tes  ,1]],
                 [nac_pts[i_seg  ,i_tes+1,1],nac_pts[i_seg+1,i_tes+1,1]]])
            Z = np.array([[nac_pts[i_seg  ,i_tes  ,2],nac_pts[i_seg+1,i_tes  ,2]],
                 [nac_pts[i_seg  ,i_tes+1,2],nac_pts[i_seg+1,i_tes+1,2]]])
             
            values = np.zeros_like(X) 
            verts = contour_surface_slice(X, Y, Z ,values,color_map)
            plot_data.append(verts)    

    return plot_data

## @ingroup Library-Plots-Geometry 
def generate_3d_nacelle_points(nac,tessellation = 24 ,number_of_airfoil_points = 21):
    """ This generates the coordinate points on the surface of the nacelle

    Assumptions:
    None

    Source:
    None

    Inputs:
    nac                        - Nacelle data structure 
    tessellation               - azimuthal discretization of lofted body 
    number_of_airfoil_points   - discretization of airfoil geometry 
    
    Properties Used:
    N/A 
    """ 
    
    num_nac_segs = len(nac.Segments.keys())   
    theta        = np.linspace(0,2*np.pi,tessellation) 
    
    if num_nac_segs == 0:
        num_nac_segs = int(np.ceil(number_of_airfoil_points/2))
        nac_pts      = np.zeros((num_nac_segs,tessellation,3))
        naf          = nac.Airfoil
        
        if type(naf) == RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil: 
            a_geo        = compute_naca_4series(naf.coordinate_file,num_nac_segs)
            xpts         = np.repeat(np.atleast_2d(a_geo.x_coordinates[0]).T,tessellation,axis = 1)*nac.length
            zpts         = np.repeat(np.atleast_2d(a_geo.y_coordinates[0]).T,tessellation,axis = 1)*nac.length  
        
        elif naf.coordinate_file != None: 
            a_geo        = import_airfoil_geometry(naf.coordinate_file,num_nac_segs)
            xpts         = np.repeat(np.atleast_2d(np.take(a_geo.x_coordinates,[0],axis=0)).T,tessellation,axis = 1)*nac.length
            zpts         = np.repeat(np.atleast_2d(np.take(a_geo.y_coordinates,[0],axis=0)).T,tessellation,axis = 1)*nac.length
        
        else:
            # if no airfoil defined, use super ellipse as default
            a =  nac.length/2 
            b =  (nac.diameter - nac.inlet_diameter)/2 
            b = np.maximum(b,1E-3) # ensure 
            xpts =  np.repeat(np.atleast_2d(np.linspace(-a,a,num_nac_segs)).T,tessellation,axis = 1) 
            zpts = (np.sqrt((b**2)*(1 - (xpts**2)/(a**2) )))*nac.length 
            xpts = (xpts+a)*nac.length  

        if nac.flow_through: 
            zpts = zpts + nac.inlet_diameter/2  
                
        # create geometry 
        theta_2d = np.repeat(np.atleast_2d(theta),num_nac_segs,axis =0) 
        nac_pts[:,:,0] =  xpts
        nac_pts[:,:,1] =  zpts*np.cos(theta_2d)
        nac_pts[:,:,2] =  zpts*np.sin(theta_2d)  
                
    else:
        nac_pts = np.zeros((num_nac_segs,tessellation,3))  
        for i_seg, segment in enumerate(nac.Segments):  
            a = segment.width/2
            b = segment.height/2
            n = segment.curvature
            theta    = np.linspace(0,2*np.pi,tessellation) 
            nac_ypts =  (abs((np.cos(theta)))**(2/n))*a * ((np.cos(theta)>0)*1 - (np.cos(theta)<0)*1) 
            nac_zpts =  (abs((np.sin(theta)))**(2/n))*b * ((np.sin(theta)>0)*1 - (np.sin(theta)<0)*1)  
            nac_pts[i_seg,:,0] = segment.percent_x_location*nac.length
            nac_pts[i_seg,:,1] = nac_ypts + segment.percent_y_location*nac.length 
            nac_pts[i_seg,:,2] = nac_zpts + segment.percent_z_location*nac.length  
            
    # rotation about y to orient propeller/rotor to thrust angle
    rot_trans =  nac.nac_vel_to_body()
    rot_trans =  np.repeat( np.repeat(rot_trans[ np.newaxis,:,: ],tessellation,axis=0)[ np.newaxis,:,:,: ],num_nac_segs,axis=0)    
    
    NAC_PTS  =  np.matmul(rot_trans,nac_pts[...,None]).squeeze()  
     
    # translate to body 
    NAC_PTS[:,:,0] = NAC_PTS[:,:,0] + nac.origin[0][0]
    NAC_PTS[:,:,1] = NAC_PTS[:,:,1] + nac.origin[0][1]
    NAC_PTS[:,:,2] = NAC_PTS[:,:,2] + nac.origin[0][2]
     
    return NAC_PTS 