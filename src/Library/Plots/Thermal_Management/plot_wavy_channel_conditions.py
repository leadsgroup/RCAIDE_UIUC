# RCAIDE/Library/Plots/Thermal_Management/plot_wavy_channel_conditions.py
# 
# 
# Created:  Sep 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  

from RCAIDE.Framework.Core import Units
from RCAIDE.Library.Plots.Common import set_axes, plot_style
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#   plot_wavy_channel_conditions
# ----------------------------------------------------------------------------------------------------------------------   
def plot_wavy_channel_conditions(wavy_channel, results, coolant_line, save_figure,show_legend ,save_filename,file_type , width, height):
    """Plots the Wavy Channel Heat Acqusition conditions throughout flight.
    
     Assumptions:
     None
    
     Source:
     None
    
     Inputs:
     results.segments.conditions.energy[coolant_line.tag][wavy_channel.tag].
                                                                       outlet_coolant_temperature
                                                                       coolant_mass_flow_rate
                                                                       power
                                                                
                                                                       
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
    
    fig = plt.figure('Identical_'+ save_filename)
    fig.set_size_inches(width,height) 
    axis_1 = plt.subplot(2,2,1)
    axis_2 = plt.subplot(2,2,2) 
    axis_3 = plt.subplot(2,2,3)

    for network in results.segments[0].analyses.energy.vehicle.networks: 
        busses  = network.busses 
        for bus in busses:
            for b_i, battery in enumerate(bus.battery_modules):
                if b_i == 0 or bus.identical_battery_modules == False:
                    for i in range(len(results.segments)): 
                        time                            = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min    
                        wavy_channel_conditions         = results.segments[i].conditions.energy[coolant_line.tag][wavy_channel.tag]   
                        outlet_coolant_temperature      = wavy_channel_conditions.outlet_coolant_temperature[:,0]
                        coolant_mass_flow_rate          = wavy_channel_conditions.coolant_mass_flow_rate[:,0]
                        power                           = wavy_channel_conditions.power[:,0]       
                
                        if i == 0:                
                            axis_1.plot(time, outlet_coolant_temperature, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width, label = wavy_channel.tag)
                        else:
                            axis_1.plot(time, outlet_coolant_temperature, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width)
                        axis_1.set_ylabel(r'Coolant Temp. (K)') 
                        set_axes(axis_1)     
                         
                        axis_2.plot(time, coolant_mass_flow_rate, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width)
                        axis_2.set_ylabel(r'Coolant $\dot{m}$ (kg/s)')
                        set_axes(axis_2) 
                 
                        axis_3.plot(time, power, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width)
                        axis_3.set_ylabel(r'HAS Power (W)')
                        axis_3.set_xlabel(r'Time (mins)')
                        set_axes(axis_3)
        
    if show_legend:          
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 4) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})     
    
    # Adjusting the sub-plots for legend 
    fig.tight_layout()
    fig.subplots_adjust(top=0.8) 
    
    # set title of plot 
    title_text   = 'Wavy_Channel_Properties'       
    fig.suptitle(title_text) 
    
    if save_figure:
        plt.savefig(wavy_channel.tag + file_type)    
    return fig 