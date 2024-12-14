# RCAIDE/Library/Plots/Noise/plot_noise_level.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Framework.Core import Units
from RCAIDE.Library.Plots.Common import set_axes, plot_style 

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ---------------------------------------------------------------------------------------------------------------------- 
def plot_noise_level(noise_data,
                     noise_level = False,
                     save_figure = False,
                     save_filename="Sideline_Noise_Levels",
                     file_type=".png",
                     width = 11, height = 7): 
    """This plots the A-weighted Sound Pressure Level as a function of time at various aximuthal angles
    on the ground

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.conditions.
        frames.inertial.position_vector   - position vector of aircraft
        noise.
            total_SPL_dBA                 - total SPL (dbA)
            relative_microphone_locations - microphone locations

    Outputs:
    Plots

    Properties Used:
    N/A
    """      
    N_gm_y       = noise_data.microphone_y_resolution 
    gm           = noise_data.microphone_locations    
    gm_x         = gm[:,:,0]
    gm_y         = gm[:,:,1]    
    

    # get plotting style 
    ps      = plot_style()  

    parameters = {'axes.labelsize': ps.axis_font_size,
                  'xtick.labelsize': ps.axis_font_size,
                  'ytick.labelsize': ps.axis_font_size,
                  'axes.titlesize': ps.title_font_size}
    plt.rcParams.update(parameters) 
      
    fig         = plt.figure(save_filename)
    fig.set_size_inches(width,height)
    axes        = fig.add_subplot(1,1,1) 
    
    # get line colors for plots 
    line_colors   = cm.inferno(np.linspace(0,0.9,N_gm_y))  
      
    for k in range(N_gm_y):    
        axes.plot(gm_x[:,0]/Units.nmi, noise_level[:,k], marker = 'o', color = line_colors[k], label= r'mic at y = ' + str(round(gm_y[0,k],1)) + r' m' ) 
    axes.set_ylabel('SPL [dBA]')
    axes.set_xlabel('Range [nmi]')  
    set_axes(axes)
    axes.legend(loc='upper right')         
    if save_figure:
        plt.savefig(save_filename + ".png")    
        
    return fig