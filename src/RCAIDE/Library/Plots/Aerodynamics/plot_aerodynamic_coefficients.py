# RCAIDE/Library/Plots/Performance/Aerodynamics/plot_aerodynamic_coefficients.py
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
def plot_aerodynamic_coefficients(results,
                             save_figure = False,  
                             show_legend = True,
                             save_filename = "Aerodynamic_Coefficents",
                             file_type = ".png",
                             width = 11, height = 7):
    """This plots the aerodynamic coefficients
    
    Assumptions:
    None
    
    Source:
    None
    
    Inputs:
    results.segments.condtions.aerodynamics.
        lift_coefficient
        drag_coefficient
        angle_of_attack
        
    Outputs:
    Plots
    
    Properties Used:
    N/A
    """ 

    # get plotting style 
    ps      = plot_style()  

    parameters = {'axes.labelsize': ps.axis_font_size,
                  'xtick.labelsize': ps.axis_font_size,
                  'ytick.labelsize': ps.axis_font_size,
                  'axes.titlesize': ps.title_font_size}
    plt.rcParams.update(parameters)
     
    # get line colors for plots 
    line_colors   = cm.inferno(np.linspace(0,0.9,len(results.segments)))     
     
    fig   = plt.figure(save_filename)
    fig.set_size_inches(width,height)
     
    for i in range(len(results.segments)): 
        time = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        cl   = results.segments[i].conditions.aerodynamics.coefficients.lift.total[:,0,None]
        cd   = results.segments[i].conditions.aerodynamics.coefficients.drag.total[:,0,None]
        aoa  = results.segments[i].conditions.aerodynamics.angles.alpha[:,0] / Units.deg
        l_d  = cl/cd    
                       
        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ')
        axis_1 = plt.subplot(2,2,1) 
        axis_1.plot(time, aoa, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name) 
        axis_1.set_ylabel(r'AoA (deg)') 
        axis_1.set_xlabel('Time (mins)')        
        axis_1.set_ylim([-5,15])
        set_axes(axis_1)    

        axis_2 = plt.subplot(2,2,2)        
        axis_2.plot(time, l_d, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width) 
        axis_2.set_ylabel(r'L/D')
        axis_2.set_xlabel('Time (mins)')
        set_axes(axis_2) 

        axis_3 = plt.subplot(2,2,3) 
        axis_3.plot(time, cl, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width)
        axis_3.set_xlabel('Time (mins)')
        axis_3.set_ylabel(r'$C_L$')
        set_axes(axis_3) 

        axis_4 = plt.subplot(2,2,4)        
        axis_4.plot(time, cd, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width)
        axis_4.set_xlabel('Time (mins)')
        axis_4.set_ylabel(r'$C_D$')
        axis_4.set_ylim([0,0.1])
        set_axes(axis_4) 
        
    if show_legend:
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 4)  
    
    # Adjusting the sub-plots for legend
    fig.tight_layout() 
    fig.subplots_adjust(top=0.8)  
    
    if save_figure:
        fig.savefig(save_filename   + file_type)  
    return fig 