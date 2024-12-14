# RCAIDE/Library/Plots/Performance/Aerodynamics/plot_aerodynamic_forces.py
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
def plot_aerodynamic_forces(results,
                             save_figure = False,
                             show_legend = True,
                             save_filename = "Aerodynamic_Forces",
                             file_type = ".png",
                             width = 11, height = 7):
    """This plots the aerodynamic forces
    
    Assumptions:
    None
    
    Source:
    None
    
    Inputs:
    results.segments.condtions.frames
         body.thrust_force_vector
         wind.force_vector
         wind.force_vector
         
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
        time   = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        Power  = results.segments[i].conditions.energy.power[:,0] 
        Thrust = results.segments[i].conditions.frames.body.thrust_force_vector[:,0]
        Lift   = -results.segments[i].conditions.frames.wind.force_vector[:,2]
        Drag   = -results.segments[i].conditions.frames.wind.force_vector[:,0]
         
        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ')
        
        # power 
        axis_1 = plt.subplot(2,2,1)
        axis_1.set_ylabel(r'Power (MW)')
        axis_1.plot(time,Power/1E6, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name) 
        set_axes(axis_1)                
        
        axis_2 = plt.subplot(2,2,2)
        axis_2.plot(time, Thrust/1000, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width) 
        axis_2.set_ylabel(r'Thrust (kN)')
        set_axes(axis_2) 

        axis_3 = plt.subplot(2,2,3)
        axis_3.plot(time, Lift/1000, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)
        axis_3.set_xlabel('Time (mins)')
        axis_3.set_ylabel(r'Lift (kN)')
        set_axes(axis_3) 
        
        axis_4 = plt.subplot(2,2,4)
        axis_4.plot(time,Drag/1000 , color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)
        axis_4.set_xlabel('Time (mins)')
        axis_4.set_ylabel(r'Drag (kN)')
        set_axes(axis_4)  
        
 
    if show_legend:    
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 4) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend 
    fig.tight_layout()
    fig.subplots_adjust(top=0.8)
    
    # set title of plot 
    title_text    = 'Aerodynamic Forces'      
    fig.suptitle(title_text)
    
    if save_figure:
        plt.savefig(save_filename + file_type)   
    return fig 
