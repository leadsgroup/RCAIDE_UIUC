## @ingroup Library-Plots-Energy
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
## @ingroup Library-Plots-Performance-Energy-Fuel
def plot_altitude_sfc_weight(results,
                             save_figure = False,
                             show_legend = True,
                             save_filename = "Altitude_SFC_Weight" ,
                             file_type = ".png",
                             width = 12, height = 7):
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
    axis_1 = plt.subplot(2,2,1)
    axis_2 = plt.subplot(2,2,2)
    axis_3 = plt.subplot(2,2,3)
    axis_4 = plt.subplot(2,2,4)
    
    for i in range(len(results.segments)): 
        time     = results.segments[i].conditions.frames.inertial.time[:, 0] / Units.min
        Weight   = results.segments[i].conditions.weights.total_mass[:, 0] * 9.81   
        mdot     = results.segments[i].conditions.weights.vehicle_mass_rate[:, 0]
        thrust   = results.segments[i].conditions.frames.body.thrust_force_vector[:, 0]
        sfc      = (mdot / Units.lb) / (thrust / Units.lbf) * Units.hr       
            
        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ') 
        
        axis_1.set_ylabel(r'Throttle')
        set_axes(axis_1)               
        for network in results.segments[i].analyses.energy.networks: 
            busses      = network.busses
            fuel_lines  = network.fuel_lines
            for bus in busses:
                for propulsor in bus.propulsors: 
                    eta = results.segments[i].conditions.energy[bus.tag][propulsor.tag].throttle[:,0]  
                    axis_1.plot(time, eta, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)               
            for fuel_line in fuel_lines:  
                for propulsor in fuel_line.propulsors: 
                    eta = results.segments[i].conditions.energy[fuel_line.tag][propulsor.tag].throttle[:,0]  
                    axis_1.plot(time, eta, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)     
        
        if i == 0:
            axis_2.plot(time, Weight/1000 , color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name) 
        else:
            axis_2.plot(time, Weight/1000 , color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width) 
        axis_2.set_ylabel(r'Weight (kN)')  
        set_axes(axis_2) 

        axis_3.plot(time, sfc, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)
        axis_3.set_xlabel('Time (mins)')
        axis_3.set_ylabel(r'SFC (lb/lbf-hr)')
        set_axes(axis_3) 

        axis_4.plot(time, mdot, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)
        axis_4.set_xlabel('Time (mins)')
        axis_4.set_ylabel(r'Fuel Rate (kg/s)')
        set_axes(axis_4)         
        
    
    if show_legend:
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend 
    fig.subplots_adjust(top=0.8)
    
    # set title of plot 
    title_text    = 'Throttle, Fuel Consumption  and Weight'      
    fig.suptitle(title_text)
    
    if save_figure:
        plt.savefig(save_filename + file_type)   
    return fig 