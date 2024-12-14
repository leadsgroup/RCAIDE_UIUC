# RCAIDE/Library/Plots/Geometry/plot_3d_nacelle.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
import RCAIDE
from RCAIDE.Framework.Core import Data 
from RCAIDE.Library.Plots.Geometry.Common.contour_surface_slice import contour_surface_slice
from RCAIDE.Library.Methods.Geometry.Airfoil import import_airfoil_geometry
from RCAIDE.Library.Methods.Geometry.Airfoil import compute_naca_4series  
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------   
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
    
    if type(nacelle) == RCAIDE.Library.Components.Nacelles.Stack_Nacelle: 
        G = generate_3d_stack_nacelle_points(nacelle,tessellation,number_of_airfoil_points)
    elif type(nacelle) == RCAIDE.Library.Components.Nacelles.Body_of_Revolution_Nacelle: 
        G = generate_3d_BOR_nacelle_points(nacelle,tessellation,number_of_airfoil_points)
    else:
        G= generate_3d_basic_nacelle_points(nacelle,tessellation,number_of_airfoil_points)
        
               
    num_nac_segs = len(G.PTS[:,0,0])
    tesselation  = len(G.PTS[0,:,0]) 
    for i_seg in range(num_nac_segs-1):
        for i_tes in range(tesselation-1):
            X = np.array([[G.PTS[i_seg  ,i_tes  ,0],G.PTS[i_seg+1,i_tes  ,0]],
                 [G.PTS[i_seg  ,i_tes+1,0],G.PTS[i_seg+1,i_tes+1,0]]])
            Y = np.array([[G.PTS[i_seg  ,i_tes  ,1],G.PTS[i_seg+1,i_tes  ,1]],
                 [G.PTS[i_seg  ,i_tes+1,1],G.PTS[i_seg+1,i_tes+1,1]]])
            Z = np.array([[G.PTS[i_seg  ,i_tes  ,2],G.PTS[i_seg+1,i_tes  ,2]],
                 [G.PTS[i_seg  ,i_tes+1,2],G.PTS[i_seg+1,i_tes+1,2]]])
             
            values = np.zeros_like(X) 
            verts = contour_surface_slice(X, Y, Z ,values,color_map)
            plot_data.append(verts)    

    return plot_data
 
def generate_3d_stack_nacelle_points(nac,tessellation = 24 ,number_of_airfoil_points = 21):
    """ This generates the coordinate points on the surface of the stack nacelle

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
 
    nac_pts = np.zeros((num_nac_segs,tessellation,3))  
    for i_seg, segment in enumerate(nac.Segments): 
        a = segment.width/2
        b = segment.height/2
        n = segment.curvature
        theta                   = np.linspace(0,2*np.pi,tessellation) 
        section_points          = np.zeros((24, 3, 1))
        section_points[:, 1, 0] = (abs((np.cos(theta)))**(2/n))*a * ((np.cos(theta)>0)*1 - (np.cos(theta)<0)*1) 
        section_points[:, 2, 0] = (abs((np.sin(theta)))**(2/n))*b * ((np.sin(theta)>0)*1 - (np.sin(theta)<0)*1)  
        
        x_rotation = np.zeros((tessellation, 3, 3))
        x_rotation[:,0,0] = 1
        x_rotation[:,1,1] = np.cos(segment.orientation_euler_angles[0])
        x_rotation[:,1,2] = -np.sin(segment.orientation_euler_angles[0])
        x_rotation[:,2,1] = np.sin(segment.orientation_euler_angles[0])
        x_rotation[:,2,2] = np.cos(segment.orientation_euler_angles[0])
        
        y_rotation = np.zeros((tessellation, 3, 3))
        y_rotation[:,0,0] = np.cos(segment.orientation_euler_angles[1])
        y_rotation[:,0,2] = np.sin(segment.orientation_euler_angles[1])
        y_rotation[:,1,1] = 1
        y_rotation[:,2,0] = -np.sin(segment.orientation_euler_angles[1])
        y_rotation[:,2,2] = np.cos(segment.orientation_euler_angles[1]) 

        z_rotation = np.zeros((tessellation, 3, 3))
        z_rotation[:,0,0] = np.cos(segment.orientation_euler_angles[2])
        z_rotation[:,0,1] = -np.sin(segment.orientation_euler_angles[2])
        z_rotation[:,1,0] = np.sin(segment.orientation_euler_angles[2])
        z_rotation[:,1,1] = np.cos(segment.orientation_euler_angles[2])
        z_rotation[:,2,2] = 1
        
        rotated_pts = np.matmul(z_rotation,np.matmul(y_rotation,np.matmul(x_rotation,section_points))) 

        nac_pts[i_seg] = rotated_pts[:,:,0]   

        nac_pts[i_seg,:,0] += segment.percent_x_location*nac.length     
        nac_pts[i_seg,:,1] += segment.percent_y_location*nac.length 
        nac_pts[i_seg,:,2] += segment.percent_z_location*nac.length          
            
    # rotation about y to orient propeller/rotor to thrust angle
    rot_trans =  nac.nac_vel_to_body()
    rot_trans =  np.repeat( np.repeat(rot_trans[ np.newaxis,:,: ],tessellation,axis=0)[ np.newaxis,:,:,: ],num_nac_segs,axis=0)    
    
    NAC_PTS  =  np.matmul(rot_trans,nac_pts[...,None]).squeeze()  
     
    # translate to body 
    NAC_PTS[:,:,0] = NAC_PTS[:,:,0] + nac.origin[0][0]
    NAC_PTS[:,:,1] = NAC_PTS[:,:,1] + nac.origin[0][1]
    NAC_PTS[:,:,2] = NAC_PTS[:,:,2] + nac.origin[0][2]
     
    G = Data()         
    G.PTS  = NAC_PTS 
    return G     


 
def generate_3d_BOR_nacelle_points(nac,tessellation = 24 ,number_of_airfoil_points = 21):
    """ This generates the coordinate points on the surface of the body of revolution nacelle

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
     
    theta        = np.linspace(0,2*np.pi,tessellation)  
    num_nac_segs = int(np.ceil(number_of_airfoil_points/2))
    nac_pts      = np.zeros((num_nac_segs,tessellation,3))
    af_tag       = list(nac.Airfoil.keys())[0]
    naf          =  nac.Airfoil[af_tag]
    
    if type(naf) == RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil: 
        a_geo        = compute_naca_4series(naf.NACA_4_Series_code,num_nac_segs)
        xpts         = np.repeat(np.atleast_2d(a_geo.x_coordinates).T,tessellation,axis = 1)*nac.length
        zpts         = np.repeat(np.atleast_2d(a_geo.y_coordinates).T,tessellation,axis = 1)*nac.length  
    
    elif naf.coordinate_file != None: 
        a_geo        = import_airfoil_geometry(naf.coordinate_file,num_nac_segs)
        xpts         = np.repeat(np.atleast_2d(np.take(a_geo.x_coordinates,axis=0)).T,tessellation,axis = 1)*nac.length
        zpts         = np.repeat(np.atleast_2d(np.take(a_geo.y_coordinates,axis=0)).T,tessellation,axis = 1)*nac.length 

    if nac.flow_through: 
        zpts = zpts + nac.diameter/2  
            
    # create geometry 
    theta_2d = np.repeat(np.atleast_2d(theta),num_nac_segs,axis =0) 
    nac_pts[:,:,0] =  xpts
    nac_pts[:,:,1] =  zpts*np.cos(theta_2d)
    nac_pts[:,:,2] =  zpts*np.sin(theta_2d)   
            
    # rotation about y to orient propeller/rotor to thrust angle
    rot_trans =  nac.nac_vel_to_body()
    rot_trans =  np.repeat( np.repeat(rot_trans[ np.newaxis,:,: ],tessellation,axis=0)[ np.newaxis,:,:,: ],num_nac_segs,axis=0)    
    
    NAC_PTS  =  np.matmul(rot_trans,nac_pts[...,None]).squeeze()  
     
    # translate to body 
    NAC_PTS[:,:,0] = NAC_PTS[:,:,0] + nac.origin[0][0]
    NAC_PTS[:,:,1] = NAC_PTS[:,:,1] + nac.origin[0][1]
    NAC_PTS[:,:,2] = NAC_PTS[:,:,2] + nac.origin[0][2]
    
    G = Data()         
    G.PTS  = NAC_PTS 
    return G     

def generate_3d_basic_nacelle_points(nac,tessellation,number_of_airfoil_points):
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
      

    num_nac_segs = 10
    nac_pts      = np.zeros((num_nac_segs,tessellation,3)) 
    theta        = np.linspace(0,2*np.pi,tessellation)  
          
    # if no airfoil defined, use super ellipse as default
    a    =  nac.length/2 
    b    =  nac.diameter/2  
    xpts =  np.repeat(np.atleast_2d(np.linspace(-a,a,num_nac_segs)).T,tessellation,axis = 1) 
    zpts = np.sqrt((b**2)*(1 - (xpts**2)/(a**2) ))  
    xpts = (xpts+a)  

    if nac.flow_through: 
        zpts = zpts + nac.inlet_diameter/2  
            
    # create geometry 
    theta_2d = np.repeat(np.atleast_2d(theta),num_nac_segs,axis =0) 
    nac_pts[:,:,0] =  xpts
    nac_pts[:,:,1] =  zpts*np.cos(theta_2d)
    nac_pts[:,:,2] =  zpts*np.sin(theta_2d)  
                 
    # rotation about y to orient propeller/rotor to thrust angle
    rot_trans =  nac.nac_vel_to_body()
    rot_trans =  np.repeat( np.repeat(rot_trans[ np.newaxis,:,: ],tessellation,axis=0)[ np.newaxis,:,:,: ],num_nac_segs,axis=0)    
    
    NAC_PTS  =  np.matmul(rot_trans,nac_pts[...,None]).squeeze()  
     
    # translate to body 
    NAC_PTS[:,:,0] = NAC_PTS[:,:,0] + nac.origin[0][0]
    NAC_PTS[:,:,1] = NAC_PTS[:,:,1] + nac.origin[0][1]
    NAC_PTS[:,:,2] = NAC_PTS[:,:,2] + nac.origin[0][2]
     
    G = Data()         
    G.PTS  = NAC_PTS 
    return G     