## @ingroup Library-Plots-Geometry
# RCAIDE/Library/Plots/Geometry/plot_3d_vehicle.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import RCAIDE
from RCAIDE.Library.Methods.Aerodynamics.Vortex_Lattice_Method  import generate_vortex_distribution  
from RCAIDE.Library.Plots.Geometry.plot_3d_fuselage             import plot_3d_fuselage
from RCAIDE.Library.Plots.Geometry.plot_3d_wing                 import plot_3d_wing 
from RCAIDE.Library.Plots.Geometry.plot_3d_nacelle              import plot_3d_nacelle
from RCAIDE.Library.Plots.Geometry.plot_3d_rotor                import plot_3d_rotor

# python imports 
import numpy as np 
import plotly.graph_objects as go  

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Plots-Geometry
def plot_3d_vehicle(vehicle,
                    show_axis                   = False,
                    save_figure                 = False,
                    alpha                       = 1.0,
                    show_wing_control_points    = True,
                    show_rotor_wake_vortex_core = False,
                    save_filename               = "Vehicle_Geometry",
                    min_x_axis_limit            = None,
                    max_x_axis_limit            = None,
                    min_y_axis_limit            = None,
                    max_y_axis_limit            = None,
                    min_z_axis_limit            = None,
                    max_z_axis_limit            = None,
                    camera_eye_x                = -1.5,
                    camera_eye_y                = -1.5,
                    camera_eye_z                = .8,
                    camera_center_x             = 0.,
                    camera_center_y             = 0.,
                    camera_center_z             = 0.,
                    show_figure                 = True):
    """This plots a 3D representation of the aircraft 

    Assumptions:
    None

    Source:
    None

    Inputs:
       vehicle                      - vehicle data structure 
       show_axis                    - plot axis flag          
       save_figure                  - safe figure flag              
       alpha                        - opacity                   
       show_wing_control_points     - show control point flag  
       show_rotor_wake_vortex_core  - show rotor wake flag 
       save_filename                - filename for saving  
       x_axis_limit                 - limits of axis  
       y_axis_limit                 - limits of axis  
       z_axis_limit                 - limits of axis  
       show_figure                  - show figure flag  

    Outputs:
    Plots

    Properties Used:
    N/A
    """

    print("\nPlotting vehicle") 
    camera        =  dict(eye=dict(x=camera_eye_x, y=camera_eye_y, z=camera_eye_z), center=dict(x= camera_center_x, y=camera_center_x, z= camera_center_z))   
    plot_data     = []
    
    plot_data,x_min,x_max,y_min,y_max,z_min,z_max  = generate_3d_vehicle_geometry_data(plot_data,
                                                                                       vehicle,
                                                                                       alpha,
                                                                                       show_wing_control_points,
                                                                                       show_rotor_wake_vortex_core,
                                                                                       min_x_axis_limit,
                                                                                       max_x_axis_limit,
                                                                                       min_y_axis_limit,
                                                                                       max_y_axis_limit,
                                                                                       min_z_axis_limit,
                                                                                       max_z_axis_limit)
    

    fig = go.Figure(data=plot_data)
    fig.update_scenes(aspectmode   = 'cube',
                      xaxis_visible=show_axis,
                      yaxis_visible=show_axis,
                      zaxis_visible=show_axis
                      )
    fig.update_layout( 
             width     = 1500,
             height    = 1500, 
             scene = dict(
                        xaxis = dict(backgroundcolor="grey", gridcolor="white", showbackground=show_axis,
                                     zerolinecolor="white", range=[x_min,x_max]),
                        yaxis = dict(backgroundcolor="grey", gridcolor="white", showbackground=show_axis, 
                                     zerolinecolor="white", range=[y_min,y_max]),
                        zaxis = dict(backgroundcolor="grey",gridcolor="white",showbackground=show_axis,
                                     zerolinecolor="white", range=[z_min,z_max])),             
             scene_camera=camera) 
    fig.update_coloraxes(showscale=False) 
    fig.update_traces(opacity = alpha)
    if save_figure:
        fig.write_image(save_filename + ".png")
        
    if show_figure:
        fig.write_html( save_filename + '.html', auto_open=True) 
    
    return     

## @ingroup Library-Plots-Geometry
def generate_3d_vehicle_geometry_data(plot_data,
                                      vehicle,
                                      alpha                       = 1.0,
                                      show_wing_control_points    = False,
                                      show_rotor_wake_vortex_core = False,
                                      min_x_axis_limit            = None,
                                      max_x_axis_limit            = None,
                                      min_y_axis_limit            = None,
                                      max_y_axis_limit            = None,
                                      min_z_axis_limit            = None,
                                      max_z_axis_limit            = None):
    """ This plots the 3D surface of the network

    Assumptions:
    None

    Source:
    None

    Inputs:
       vehicle                      - vehicle data structure          
       alpha                        - opacity                   
       show_wing_control_points     - show control point flag  
       show_rotor_wake_vortex_core  - show rotor wake flag 
       save_filename                - filename for saving  
       x_axis_limit                 - limits of axis  
       y_axis_limit                 - limits of axis  
       z_axis_limit                 - limits of axis   

    Properties Used:
    N/A
    """ 
    # unpack vortex distribution
    try:
        VD = vehicle.vortex_distribution
    except:
        VL = RCAIDE.Framework.Analyses.Aerodynamics.Subsonic_VLM()  
        VL.settings.number_of_spanwise_vortices  = 25
        VL.settings.number_of_chordwise_vortices = 5
        VL.settings.spanwise_cosine_spacing      = False
        VL.settings.model_fuselage               = False
        VL.settings.model_nacelle                = False
        VD = generate_vortex_distribution(vehicle,VL.settings)

    
    # -------------------------------------------------------------------------
    # DEFINE PLOT LIMITS 
    # -------------------------------------------------------------------------  
    if min_x_axis_limit == None: 
        min_x_axis_limit = np.minimum(-1,np.min(VD.XC)*1.2) 
    if max_x_axis_limit  == None: 
        max_x_axis_limit = np.maximum(np.max(VD.XC)*1.2,10)
    if min_y_axis_limit  == None: 
        min_y_axis_limit = np.min(VD.YC)*1.2
    if min_y_axis_limit  == None: 
        max_y_axis_limit = np.max(VD.YC)*1.2
    if min_z_axis_limit  == None:  
        min_z_axis_limit = -1*np.max(VD.ZC)
    if max_z_axis_limit == None:
        min_z_axis_limit = 2.5*np.max(VD.ZC) 
    
    # -------------------------------------------------------------------------
    # PLOT WING
    # ------------------------------------------------------------------------- 
    plot_data       = plot_3d_wing(plot_data,VD,color_map ='greys')
    if  show_wing_control_points: 
        ctrl_pts = go.Scatter3d(x=VD.XC, y=VD.YC, z=VD.ZC,
                                    mode  = 'markers',
                                    marker= dict(size=6,color='red',opacity=0.8),
                                    line  = dict(color='red',width=2))
        
        plot_data.append(ctrl_pts) 
 
    # -------------------------------------------------------------------------
    # PLOT FUSELAGE
    # ------------------------------------------------------------------------- 
    for fus in vehicle.fuselages:
        plot_data = plot_3d_fuselage(plot_data,fus,color_map = 'teal')

    
    # -------------------------------------------------------------------------
    # PLOT BOOMS
    # ------------------------------------------------------------------------- 
    for boom in vehicle.booms:
        plot_data = plot_3d_fuselage(plot_data,boom,color_map = 'gray')
            
    # -------------------------------------------------------------------------
    # PLOT NACELLE
    # ------------------------------------------------------------------------- 
    number_of_airfoil_points = 21
    tessellation             = 24
    for nacelle in vehicle.nacelles:    
        plot_data = plot_3d_nacelle(plot_data,nacelle,tessellation,number_of_airfoil_points,color_map = 'darkmint')  
        
    # -------------------------------------------------------------------------
    # PLOT ROTORS
    # ------------------------------------------------------------------------- 
    number_of_airfoil_points = 11
    for network in vehicle.networks:
        plot_data = plot_3d_energy_network(plot_data,network,number_of_airfoil_points,color_map = 'turbid' )
 
    return plot_data,min_x_axis_limit,max_x_axis_limit,min_y_axis_limit,max_y_axis_limit,min_z_axis_limit,max_z_axis_limit

## @ingroup Library-Plots-Geometry
def plot_3d_energy_network(plot_data,network,number_of_airfoil_points,color_map):
    """ This plots the 3D surface of the network

    Assumptions:
    None

    Source:
    None

    Inputs:
    network            - network data structure
    network_face_color - color of panel
    network_edge_color - color of panel edge 

    Properties Used:
    N/A
    """ 
    show_axis     = False 
    save_figure   = False 
    show_figure   = False
    save_filename = 'Rotor'
 
    if 'busses' in network:  
        for bus in network.busses:
            for propulsor in bus.propulsors:
                if 'rotor' in propulsor: 
                    plot_data = plot_3d_rotor(propulsor.rotor,save_filename,save_figure,plot_data,show_figure,show_axis,0,number_of_airfoil_points,color_map) 
                if 'propeller' in propulsor:
                    plot_data = plot_3d_rotor(propulsor.propeller,save_filename,save_figure,plot_data,show_figure,show_axis,0,number_of_airfoil_points,color_map) 
 
    if 'fuel_lines' in network:  
        for fuel_line in network.fuel_lines:
            for propulsor in fuel_line.propulsors: 
                if 'rotor' in propulsor: 
                    plot_data = plot_3d_rotor(propulsor.rotor,save_filename,save_figure,plot_data,show_figure,show_axis,0,number_of_airfoil_points,color_map) 
                if 'propeller' in propulsor:
                    plot_data = plot_3d_rotor(propulsor.propeller,save_filename,save_figure,plot_data,show_figure,show_axis,0,number_of_airfoil_points,color_map) 
 
    return plot_data