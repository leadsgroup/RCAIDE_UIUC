# RCAIDE/Library/Plots/Energy/plot_electric_propulsor_efficiencies.py
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
def plot_electric_propulsor_efficiencies(results,
                                  save_figure = False,
                                  show_legend=True,
                                  save_filename = "Electric_Efficiencies",
                                  file_type = ".png",
                                  width = 11, height = 7):
    """This plots the electric driven network propeller efficiencies 

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.conditions.propulsion. 
         etap
         etam
         fom
        
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
    axis_1 = plt.subplot(2,2,1)
    axis_2 = plt.subplot(2,2,2) 
    axis_3 = plt.subplot(2,2,3)
    

    for network in results.segments[0].analyses.energy.vehicle.networks:  
        for p_i, propulsor in enumerate(network.propulsors):
            if (p_i == 0) or (network.identical_propulsors == False): 
                for i in range(len(results.segments)):  
                    if 'rotor' in propulsor: 
                        thrustor =  propulsor.rotor
                        axis_1.set_ylabel(r'$\eta_{rotor}$')
                    elif 'ducted_fan' in propulsor:
                        thrustor =  propulsor.ducted_fan
                        axis_1.set_ylabel(r'$\eta_{ducted fan}$')
                    motor =  propulsor.motor
                      
                    bus_results  = results.segments[i].conditions.energy 
                    time         = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min      
                    effp         = bus_results[propulsor.tag][thrustor.tag].efficiency[:,0]
                    fom          = bus_results[propulsor.tag][thrustor.tag].figure_of_merit[:,0]
                    effm         = bus_results[propulsor.tag][motor.tag].efficiency[:,0]  
                    
                    if p_i == 0 and i ==0:              
                        axis_1.plot(time, effp, color = line_colors[i], marker = ps.markers[p_i], markersize= ps.marker_size, linewidth = ps.line_width, label = thrustor.tag)
                    else:
                        axis_1.plot(time, effp, color = line_colors[i], marker = ps.markers[p_i], markersize= ps.marker_size, linewidth = ps.line_width) 
                    axis_1.set_ylim([0,1.1])
                    set_axes(axis_1)         
                     
                    axis_2.plot(time, fom, color = line_colors[i], marker = ps.markers[p_i], markersize= ps.marker_size , linewidth = ps.line_width)
                    axis_2.set_xlabel('Time (mins)')
                    axis_2.set_ylabel(r'FoM')
                    axis_2.set_ylim([0,1.1])
                    set_axes(axis_2) 
             
                    axis_3.plot(time, effm, color = line_colors[i], marker = ps.markers[p_i], markersize= ps.marker_size, linewidth = ps.line_width)
                    axis_3.set_xlabel('Time (mins)')
                    axis_3.set_ylabel(r'$\eta_{motor}$')
                    axis_3.set_ylim([0,1.1])
                    set_axes(axis_3)
           
    if show_legend:     
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 4)  
    
    # Adjusting the sub-plots for legend 
    fig.tight_layout()
    fig.subplots_adjust(top=0.8) 
    
    # set title of plot 
    title_text  =  'Electronic Network Efficiencies' 
    fig.suptitle(title_text)
    if save_figure:
        plt.savefig(save_filename + file_type) 
     
    return fig  