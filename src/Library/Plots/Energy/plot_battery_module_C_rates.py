# RCAIDE/Library/Plots/Energy/plot_battery_module_C_rates.py
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
def plot_battery_module_C_rates(results,
                        save_figure   = False,
                        show_legend   = True,
                        save_filename = "Battery_Module_C_Rates",
                        file_type     =".png",
                        width         = 8,
                        height        = 6):
    """Plots the module-level conditions of the battery throughout flight.

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
     

    fig = plt.figure(save_filename)
    fig.set_size_inches(width,height)
    # get line colors for plots 
    line_colors   = cm.inferno(np.linspace(0,0.9,len(results.segments)))      
    axis_1 = plt.subplot(1,2,1)
    axis_2 = plt.subplot(1,2,2)  
     
    for network in results.segments[0].analyses.energy.vehicle.networks: 
        busses  = network.busses 
        for bus in busses:
            for b_i, battery in enumerate(bus.battery_modules):
                if b_i == 0 or bus.identical_battery_modules == False:
                    for i in range(len(results.segments)):  
                        time                  = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min    
                        battery_conditions    = results.segments[i].conditions.energy[bus.tag].battery_modules[battery.tag]     
                        module_energy         = battery_conditions.energy[:,0]
                        module_volts          = battery_conditions.voltage_under_load[:,0] 
                        module_current        = battery_conditions.current[:,0]  
                        module_battery_amp_hr = (module_energy/ Units.Wh )/module_volts
                        module_C_instant      = module_current/module_battery_amp_hr
                        module_C_nominal      = module_current/np.max(module_battery_amp_hr)   
    
                        if i == 0 and i ==0:              
                            axis_1.plot(time, module_C_instant, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = battery.tag)
                        else: 
                            axis_1.plot(time, module_C_instant, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)                                
                        axis_1.set_ylabel(r'Inst. C-Rate (C)')
                        axis_1.set_xlabel('Time (mins)')
                        set_axes(axis_1)     
                         
                        axis_2.plot(time, module_C_nominal, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)
                        axis_2.set_ylabel(r'Nom. C-Rate (C)')
                        axis_2.set_xlabel('Time (mins)')
                        set_axes(axis_2)    
    if show_legend:      
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 4)  
    
    # Adjusting the sub-plots for legend 
    fig.tight_layout()
    fig.subplots_adjust(top=0.8) 
    
    # set title of plot 
    title_text   = 'Battery Cell Conditions'       
    fig.suptitle(title_text) 
    
    if save_figure:
        plt.savefig(save_filename + battery.tag + file_type)    
    return fig


    return  
 
                 