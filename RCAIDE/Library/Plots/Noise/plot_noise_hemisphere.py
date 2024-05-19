## @ingroup Library-Plots-Noise
# RCAIDE/Library/Plots/Noise/plot_noise_hemisphere.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from RCAIDE.Library.Plots  import *
import plotly.graph_objects as go 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Plots-Noise
def plot_noise_hemisphere(noise_data,
                          noise_level              = False,
                          min_noise_level          = 35,  
                          max_noise_level          = 90, 
                          noise_scale_label        = None,
                          save_figure              = False,
                          show_figure              = True,
                          vehicle                  = None,
                          save_filename            = "Noise_Hemisphere", 
                          colormap                 = 'jet',
                          file_type                = ".png",
                          background_color         = 'white',
                          grid_color               = 'white',
                          width                    = 1400, 
                          height                   = 800,
                          *args, **kwargs):
    
    """This plots a noise hemisphere of an aircraft 

    Assumptions:
    None

    Source:
    None

    Inputs: 
       noise_data        - noise data structure 
       noise_level       - noise level  
       min_noise_level   - minimal noise level 
       max_noise_level   - maximum noise level  
       save_figure       - save figure 
       show_figure       - show figure 
       save_filename     - save file flag 

    Outputs:
       Plots

    Properties Used:
    N/A
    """         
 
    plot_data   = []     
    if vehicle != None:
        plot_data,_,_,_,_,_,_, = generate_3d_vehicle_geometry_data(plot_data,vehicle)
        
    X               = noise_data.ground_microphone_locations[:,:,0]   
    Y               = noise_data.ground_microphone_locations[:,:,1]  
    Z               = noise_data.ground_microphone_locations[:,:,2]  
  
    # ---------------------------------------------------------------------------
    # TRHEE DIMENSIONAL NOISE CONTOUR
    # --------------------------------------------------------------------------- 
    # TERRAIN CONTOUR 
    ground_contour   = contour_surface_slice(-X,Y,Z,noise_level,color_scale=colormap, showscale= True, colorbar_title = noise_scale_label, colorbar_location = 'right', colorbar_orientation = 'v' )
    plot_data.append(ground_contour) 

    # Define Colorbar Bounds 
    fig_3d = go.Figure(data=plot_data)  
        
                         
    fig_3d.update_layout(
             title_text                             = save_filename, 
             title_x                                = 0.5,
             width                                  = width,
             height                                 = height, 
             font_size                              = 12,
             scene_aspectmode                       = 'auto', 
             scene                                  = dict(xaxis = dict(visible=False),
                                                        yaxis = dict(visible=False),
                                                        zaxis =dict(visible=False)), 
             scene_camera=dict(up    = dict(x=0, y=0, z=1),
                               center= dict(x=-0.05, y=0, z=-0.0),
                               eye   = dict(x=-1.0, y=-1.0, z=.4))   
    )  
    
    if save_figure:
        fig_3d.write_image(save_filename + ".png")
        
    if show_figure:
        fig_3d.write_html( save_filename + '.html', auto_open=True)         

    return fig_3d     

def colorax(vmin, vmax):
    return dict(cmin=vmin,  cmax=vmax)
