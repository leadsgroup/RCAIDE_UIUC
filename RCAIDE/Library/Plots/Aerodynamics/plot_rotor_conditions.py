## @ingroup Library-Plots-Performance-Aerodynamics
# RCAIDE/Library/Plots/Performance/Aerodynamics/plot_rotor_conditions.py
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
## @ingroup Library-Plots-Performance-Aerodynamics
def plot_rotor_conditions(results,
                        save_figure = False,
                        show_legend=True,
                        save_filename = "Rotor_Conditions",
                        file_type = ".png",
                        width = 12, height = 7):
    """This plots the electric driven network propeller efficiencies 

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.conditions.propulsion.  
        
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
    axis_1 = plt.subplot(2,2,1)
    axis_2 = plt.subplot(2,2,1)
    axis_3 = plt.subplot(2,2,2) 
    axis_4 = plt.subplot(2,2,3)  
    pi     = 0 
    for network in results.segments[0].analyses.energy.networks:  
        if 'busses' in network: 
            for bus in network.busses:    
                for p_i, propulsor in enumerate(bus.propulsors):
                    if p_i == 0:
                        axis_0.plot(np.zeros(2),np.zeros(2), color = line_colors[0], marker = ps.markers[pi], linewidth = ps.line_width,label= propulsor.tag) 
                        axis_0.grid(False)
                        axis_0.axis('off')
                        plot_propulsor_data(results,bus,propulsor,axis_1,axis_2,axis_3,axis_4,line_colors,ps,pi)
                    elif (bus.identical_propulsors == False) and p_i !=0: 
                        axis_0.plot(np.zeros(2),np.zeros(2), color = line_colors[0], marker = ps.markers[pi], linewidth = ps.line_width,label= propulsor.tag) 
                        axis_0.grid(False)
                        axis_0.axis('off')
                        plot_propulsor_data(results,bus,propulsor,axis_1,axis_2,axis_3,axis_4,line_colors,ps,pi)  
                    pi += 1
             
        if 'fuel_lines' in network: 
            for fuel_line in network.fuel_lines:    
                for p_i, propulsor in enumerate(fuel_line.propulsors):  
                    if p_i == 0: 
                        axis_0.plot(np.zeros(2),np.zeros(2), color = line_colors[0], marker = ps.markers[pi], linewidth = ps.line_width,label= propulsor.tag) 
                        axis_0.grid(False)
                        axis_0.axis('off')
                        plot_propulsor_data(results,fuel_line,propulsor,axis_1,axis_2,axis_3,axis_4,line_colors,ps,pi)
                    elif (fuel_line.identical_propulsors == False) and p_i !=0: 
                        axis_0.plot(np.zeros(2),np.zeros(2), color = line_colors[0], marker = ps.markers[pi], linewidth = ps.line_width,label= propulsor.tag) 
                        axis_0.grid(False)
                        axis_0.axis('off')
                        plot_propulsor_data(results,fuel_line,propulsor,axis_1,axis_2,axis_3,axis_4,line_colors,ps,pi)  
                    pi += 1
    if show_legend:    
        h, l = axis_0.get_legend_handles_labels()
        axis_1.legend(h, l)            
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend 
    fig.subplots_adjust(top=0.8) 
    
    # set title of plot 
    title_text  =  'Rotor Performance' 
    fig.suptitle(title_text)
    if save_figure:
        plt.savefig(save_filename + file_type) 
                 
    return fig 

def plot_propulsor_data(results,distributor,propulsor,axis_1,axis_2,axis_3,axis_4,line_colors,ps,pi):
    
    for i in range(len(results.segments)): 
        bus_results  =  results.segments[i].conditions.energy[distributor.tag] 
        time         =  results.segments[i].conditions.frames.inertial.time[:,0] / Units.min   
        rpm          =  bus_results[propulsor.tag].rotor.rpm[:,0]
        thrust       =  bus_results[propulsor.tag].rotor.thrust[:,0]
        torque       =  bus_results[propulsor.tag].rotor.torque[:,0]
        tm           =  bus_results[propulsor.tag].rotor.tip_mach[:,0]  
        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ') 
        if pi == 0: 
            axis_1.plot(time,rpm, color = line_colors[i], marker = ps.markers[pi]  , linewidth = ps.line_width, label = segment_name)
        else:
            axis_1.plot(time,rpm, color = line_colors[i], marker = ps.markers[pi]  , linewidth = ps.line_width)
        axis_1.set_ylabel(r'RPM')
        set_axes(axis_1)    
         
        axis_2.plot(time, tm, color = line_colors[i], marker = ps.markers[pi]  , linewidth = ps.line_width) 
        axis_2.set_ylabel(r'Tip Mach')
        set_axes(axis_2) 
 
        axis_3.plot(time,thrust, color = line_colors[i], marker = ps.markers[pi] , linewidth = ps.line_width)
        axis_3.set_ylabel(r'Thrust (N)')
        set_axes(axis_3) 
         
        axis_4.plot(time,torque, color = line_colors[i], marker = ps.markers[pi] , linewidth = ps.line_width)
        axis_4.set_ylabel(r'Torque (N-m)')
        set_axes(axis_4)     
    return 