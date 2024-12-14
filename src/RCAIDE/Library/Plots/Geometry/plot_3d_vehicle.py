# RCAIDE/Library/Plots/Geometry/plot_3d_vehicle.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
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
def plot_3d_vehicle(vehicle,
                    show_axis                   = False,
                    save_figure                 = False,
                    save_filename               = "Vehicle_Geometry",
                    alpha                       = 1.0,  
                    min_x_axis_limit            =  -5,
                    max_x_axis_limit            =  40,
                    min_y_axis_limit            =  -20,
                    max_y_axis_limit            =  20,
                    min_z_axis_limit            =  -20,
                    max_z_axis_limit            =  20, 
                    camera_eye_x                = -1.5,
                    camera_eye_y                = -1.5,
                    camera_eye_z                = .8,
                    camera_center_x             = 0.,
                    camera_center_y             = 0.,
                    camera_center_z             = -0.5,
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

def generate_3d_vehicle_geometry_data(plot_data,
                                      vehicle, 
                                      alpha                       = 1.0,  
                                      min_x_axis_limit            =  -5,
                                      max_x_axis_limit            =  40,
                                      min_y_axis_limit            =  -20,
                                      max_y_axis_limit            =  20,
                                      min_z_axis_limit            =  -20,
                                      max_z_axis_limit            =  20, ):
    """ This plots the 3D surface of the network

    Assumptions:
    None

    Source:
    None

    Inputs:
       vehicle                      - vehicle data structure          
       alpha                        - opacity  
       save_filename                - filename for saving  
       x_axis_limit                 - limits of axis  
       y_axis_limit                 - limits of axis  
       z_axis_limit                 - limits of axis   

    Properties Used:
    N/A
    """ 
    
    # -------------------------------------------------------------------------
    # PLOT WING
    # ------------------------------------------------------------------------- 
    number_of_airfoil_points = 21
    for wing in vehicle.wings:
        plot_data       = plot_3d_wing(plot_data,wing,number_of_airfoil_points , color_map='greys',alpha=1) 
        
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
    # PLOT ROTORS
    # ------------------------------------------------------------------------- 
    number_of_airfoil_points = 11
    for network in vehicle.networks:
        plot_data = plot_3d_energy_network(plot_data,network,number_of_airfoil_points,color_map = 'turbid' )
 
    return plot_data,min_x_axis_limit,max_x_axis_limit,min_y_axis_limit,max_y_axis_limit,min_z_axis_limit,max_z_axis_limit

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
    save_filename = 'propulsor'
 
    for propulsor in network.propulsors:   
        number_of_airfoil_points = 21
        tessellation             = 24
        if 'nacelle' in propulsor: 
            if propulsor.nacelle !=  None: 
                plot_data = plot_3d_nacelle(plot_data,propulsor.nacelle,tessellation,number_of_airfoil_points,color_map = 'darkmint') 
        if 'rotor' in propulsor: 
            plot_data = plot_3d_rotor(propulsor.rotor,save_filename,save_figure,plot_data,show_figure,show_axis,0,number_of_airfoil_points,color_map) 
        if 'propeller' in propulsor:
            plot_data = plot_3d_rotor(propulsor.propeller,save_filename,save_figure,plot_data,show_figure,show_axis,0,number_of_airfoil_points,color_map)  
        if 'rotor' in propulsor: 
            plot_data = plot_3d_rotor(propulsor.rotor,save_filename,save_figure,plot_data,show_figure,show_axis,0,number_of_airfoil_points,color_map) 
        if 'propeller' in propulsor:
            plot_data = plot_3d_rotor(propulsor.propeller,save_filename,save_figure,plot_data,show_figure,show_axis,0,number_of_airfoil_points,color_map) 
 
    return plot_data