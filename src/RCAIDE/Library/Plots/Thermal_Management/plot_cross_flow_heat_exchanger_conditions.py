# RCAIDE/Library/Plots/Thermal_Management/plot_cross_flow_heat_exchanger_conditions.py
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
#   plot_heat_exchanger_system_conditions
# ----------------------------------------------------------------------------------------------------------------------   
def plot_cross_flow_heat_exchanger_conditions(cross_flow_hex, results, coolant_line, save_figure,show_legend ,save_filename,file_type , width, height):
    """Plots the Cross Flow Heat Exchanger conditions throughout flight.
    
     Assumptions:
     None
    
     Source:
     None
    
     Inputs:
     results.segments.conditions.energy[coolant_line.tag][cross_flow_hex.tag].
                                                                             coolant_mass_flow_rate
                                                                             effectiveness_HEX   
                                                                             power          
                                                                             air_inlet_pressure
                                                                             inlet_air_temperature 
                                                                             air_mass_flow_rate    
                                                                       
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
    axis_1 = plt.subplot(3,2,1)
    axis_2 = plt.subplot(3,2,2) 
    axis_3 = plt.subplot(3,2,3) 
    axis_4 = plt.subplot(3,2,4)
    axis_5 = plt.subplot(3,2,5) 
    axis_6 = plt.subplot(3,2,6) 
 
    for network in results.segments[0].analyses.energy.vehicle.networks: 
        busses  = network.busses 
        for bus in busses:
            for b_i, battery in enumerate(bus.battery_modules):
                if b_i == 0 or bus.identical_battery_modules == False:
                    for i in range(len(results.segments)): 
                        time    = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min    
                        cross_flow_hex_conditions  = results.segments[i].conditions.energy[coolant_line.tag][cross_flow_hex.tag]  
                
                        coolant_mass_flow_rate     = cross_flow_hex_conditions.coolant_mass_flow_rate[:,0]        
                        effectiveness_HEX          = cross_flow_hex_conditions.effectiveness_HEX[:,0]   
                        power                      = cross_flow_hex_conditions.power[:,0]                       
                        inlet_air_pressure         = cross_flow_hex_conditions.air_inlet_pressure[:,0]          
                        inlet_air_temperature      = cross_flow_hex_conditions.inlet_air_temperature[:,0]          
                        air_mass_flow_rate         = cross_flow_hex_conditions.air_mass_flow_rate[:,0]     
                                             
                        if i == 0: 
                            axis_1.plot(time, effectiveness_HEX, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width, label = cross_flow_hex.tag)
                        else:
                            axis_1.plot(time, effectiveness_HEX, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width) 
                        axis_1.set_ylabel(r'Effectiveness') 
                        set_axes(axis_1)      
                
                        axis_2.plot(time,  inlet_air_temperature, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width)
                        axis_2.set_ylabel(r'Air Temp. (K)') 
                        set_axes(axis_2)    
                        
                        axis_3.plot(time, coolant_mass_flow_rate, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width)
                        axis_3.set_ylabel(r'Coolant $\dot{m}$ (kg/s)')
                        set_axes(axis_3) 
                
                        axis_4.plot(time, air_mass_flow_rate, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width)
                        axis_4.set_ylabel(r'Air $\dot{m}$ (kg/s)')
                        set_axes(axis_4)                               
                 
                        axis_5.plot(time, power/1000, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width)
                        axis_5.set_ylabel(r'HEX Power (KW)')
                        axis_5.set_xlabel(r'Time (mins)')
                        set_axes(axis_5)    
                
                        axis_6.plot(time, inlet_air_pressure/10e6 , color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width)
                        axis_6.set_ylabel(r'Air Pres. (MPa)')
                        axis_6.set_xlabel(r'Time (mins)')
                        set_axes(axis_6)  
            
    if show_legend:     
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 4) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})  
    
    # Adjusting the sub-plots for legend 
    fig.tight_layout()
    fig.subplots_adjust(top=0.8) 
    
    # set title of plot 
    title_text   = 'Heat_Exchanger_System'       
    fig.suptitle(title_text) 
    
    if save_figure:
        plt.savefig(save_filename + cross_flow_hex.tag + file_type)    
    return fig 