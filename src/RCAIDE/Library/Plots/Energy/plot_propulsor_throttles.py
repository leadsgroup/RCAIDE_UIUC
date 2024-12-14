# RCAIDE/Library/Plots/Energy/plot_altitude_sfc_weight.py
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
def plot_propulsor_throttles(results,
                             save_figure = False,
                             show_legend = True,
                             save_filename = "Propulsor_Throttles" ,
                             file_type = ".png",
                             width = 11, height = 7):
    """This plots the altitude, specific fuel consumption and vehicle weight.

    Assumptions:
    None

    Source:

    Inputs:
    results.segments.conditions.
        freestream.altitude
        weights.total_mass
        weights.vehicle_mass_rate
        frames.body.thrust_force_vector

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
        time     = results.segments[i].conditions.frames.inertial.time[:, 0] / Units.min  
        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ') 
        
        # power 
        axis_1 = plt.subplot(1,1,1)
        axis_1.set_ylabel(r'Throttle')
        set_axes(axis_1)               
        for network in results.segments[i].analyses.energy.vehicle.networks: 
            for j ,  propulsor in enumerate(network.propulsors):
                eta = results.segments[i].conditions.energy[propulsor.tag].throttle[:,0]  
                if j == 0 and i ==0:               
                    axis_1.plot(time, eta, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name + ': '+ propulsor.tag )
                else:
                    axis_1.plot(time, eta, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width) 
                        
          
    if show_legend:
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 4) 
        leg.set_title('Propulsor', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend 
    fig.tight_layout()
    fig.subplots_adjust(top=0.8)
    
    # set title of plot 
    title_text    = 'Throttle'      
    fig.suptitle(title_text)
    
    if save_figure:
        plt.savefig(save_filename + file_type)   
    return fig 