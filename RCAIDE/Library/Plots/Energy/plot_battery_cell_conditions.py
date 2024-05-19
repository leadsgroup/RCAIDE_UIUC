## @ingroup Library-Plots-Energy
# RCAIDE/Library/Plots/Energy/plot_battery_cell_conditions.py
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
def plot_battery_cell_conditions(results,
                                  save_figure = False,
                                  show_legend = True,
                                  save_filename = "Battery_Cell_Conditions_",
                                  file_type = ".png",
                                  width = 12, height = 7):
    """Plots the cell-level conditions of the battery throughout flight.

    Assumptions:
    None

    Source:
    None

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

    fig = plt.figure(save_filename)
    fig.set_size_inches(width,height) 
    axis_0 = plt.subplot(1,1,1)
    axis_1 = plt.subplot(3,2,1)
    axis_2 = plt.subplot(3,2,2) 
    axis_3 = plt.subplot(3,2,3) 
    axis_4 = plt.subplot(3,2,4)
    axis_5 = plt.subplot(3,2,5) 
    axis_6 = plt.subplot(3,2,6)      
    b_i = 0 
    for network in results.segments[0].analyses.energy.networks: 
        busses  = network.busses
        for bus in busses: 
            for battery in bus.batteries:   
                axis_0.plot(np.zeros(2),np.zeros(2), color = line_colors[0], marker = ps.markers[b_i], linewidth = ps.line_width,label= battery.tag) 
                axis_0.grid(False)
                axis_0.axis('off')  
               
                for i in range(len(results.segments)):  
                    time    = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min    
                    battery_conditions  = results.segments[i].conditions.energy[bus.tag][battery.tag]    
                    cell_power          = battery_conditions.cell.power[:,0]
                    cell_energy         = battery_conditions.cell.energy[:,0]
                    cell_volts          = battery_conditions.cell.voltage_under_load[:,0]
                    cell_volts_oc       = battery_conditions.cell.voltage_open_circuit[:,0]
                    cell_current        = battery_conditions.cell.current[:,0]
                    cell_SOC            = battery_conditions.cell.state_of_charge[:,0]   
                    cell_temperature    = battery_conditions.cell.temperature[:,0]  
            
                    segment_tag  = results.segments[i].tag
                    segment_name = segment_tag.replace('_', ' ') 

                    if b_i == 0:                     
                        axis_1.plot(time, cell_SOC, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width, label = segment_name)
                    else:
                        axis_1.plot(time, cell_SOC, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width)
                    axis_1.set_ylabel(r'SOC')
                    axis_1.set_ylim([0,1.1])
                    set_axes(axis_1)     
                     
                    axis_2.plot(time, cell_energy/Units.Wh, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width)
                    axis_2.set_ylabel(r'Energy (W-hr)')
                    set_axes(axis_2) 
             
                    axis_3.plot(time, cell_current, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width)
                    axis_3.set_ylabel(r'Current (A)')
                    set_axes(axis_3)  
             
                    axis_4.plot(time, cell_power, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width)
                    axis_4.set_ylabel(r'Power (W)')
                    set_axes(axis_4)     
                     
                    axis_5.plot(time, cell_volts, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width) 
                    axis_5.set_ylabel(r'Voltage (V)')
                    set_axes(axis_5) 
             
                    axis_6.plot(time, cell_temperature, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width)
                    axis_6.set_ylabel(r'Temperature, $\degree$C')
                    set_axes(axis_6)  
                b_i += 1 
            
    if show_legend:      
        h, l = axis_0.get_legend_handles_labels()
        axis_2.legend(h, l)    
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})      
    
    # Adjusting the sub-plots for legend 
    fig.subplots_adjust(top=0.8) 
    
    # set title of plot 
    title_text   = 'Battery Cell Conditions'       
    fig.suptitle(title_text) 
    
    if save_figure:
        plt.savefig(save_filename + battery.tag + file_type)    
    return fig 