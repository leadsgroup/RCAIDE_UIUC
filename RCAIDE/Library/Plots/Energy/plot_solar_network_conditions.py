## @ingroup Library-Plots-Energy
# RCAIDE/Library/Plots/Energy/plot_solar_network_conditions.py
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
## @ingroup Library-Plots-Energy
def plot_solar_network_conditions(results,
                    save_figure   = False,
                    show_legend   = True,
                    save_filename = "Solar_Flux",
                    file_type     = ".png",
                    width = 12, height = 7):
    """This plots the solar flux and power train performance of an solar powered aircraft

    Assumptions:
    None
     
    Source:
    None
    
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
    
    for network in results.segments[0].analyses.energy.networks: 
        busses  = network.busses
        for bus in busses:     
            for battery in bus.batteries:  
                fig = plt.figure(save_filename + '_' + battery.tag)
                fig.set_size_inches(width,height)    
                for i in range(len(results.segments)):  
                    battery_conditions  = results.segments[i].conditions.energy[bus.tag][battery.tag]  
                    time                = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min 
                    flux                = results.segments[i].conditions.energy.solar_flux[:,0]
                    charge              = battery_conditions.pack.power[:,0]
                    current             = battery_conditions.pack.current[:,0]
                    energy              = battery_conditions.pack.energy[:,0] / Units.MJ 
                
                    segment_tag  =  results.segments[i].tag
                    segment_name = segment_tag.replace('_', ' ')
                    axis_1 = plt.subplot(2,2,1)
                    axis_1.plot(time, flux, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name)
                    axis_1.set_ylabel(r'Solar Flux (W/m^2)')
                    set_axes(axis_1)    
                
                    axis_2 = plt.subplot(2,2,2)
                    axis_2.plot(time, charge, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width) 
                    axis_2.set_ylabel(r'Charging Power (W)')
                    set_axes(axis_2) 
                
                    axis_3 = plt.subplot(2,2,3)
                    axis_3.plot(time, current, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)
                    axis_3.set_xlabel('Time (mins)')
                    axis_3.set_ylabel(r'Battery Current (A)')
                    set_axes(axis_3) 
                
                    axis_4 = plt.subplot(2,2,4)
                    axis_4.plot(time, energy, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)
                    axis_4.set_xlabel('Time (mins)')
                    axis_4.set_ylabel(r'Battery Energy (MJ)')
                    set_axes(axis_4)   
                            
                if show_legend:        
                    leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
                    leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
                
                # Adjusting the sub-plots for legend 
                fig.subplots_adjust(top=0.8)
                
                # set title of plot 
                title_text    = 'Solar Flux Conditions: ' + battery.tag  
                fig.suptitle(title_text)
                
                if save_figure:
                    plt.savefig(save_filename + file_type)    
           
    return fig 