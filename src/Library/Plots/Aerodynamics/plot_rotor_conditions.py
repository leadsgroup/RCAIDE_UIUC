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
def plot_rotor_conditions(results,
                        save_figure = False,
                        show_legend=True,
                        save_filename = "Rotor_Conditions",
                        file_type = ".png",
                        width = 11, height = 7):
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
    axis_1 = plt.subplot(2,2,1)
    axis_2 = plt.subplot(2,2,2)
    axis_3 = plt.subplot(2,2,3) 
    axis_4 = plt.subplot(2,2,4)   
 
    for network in results.segments[0].analyses.energy.vehicle.networks: 
        for p_i, propulsor in enumerate(network.propulsors): 
            if (p_i == 0) or (network.identical_propulsors == False):            
                plot_propulsor_data(results,propulsor,axis_1,axis_2,axis_3,axis_4,line_colors,ps,p_i)                  
              
    if show_legend:                
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 4) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend
    fig.tight_layout() 
    fig.subplots_adjust(top=0.8) 
    
    # set title of plot 
    title_text  =  'Rotor Performance' 
    fig.suptitle(title_text)
    if save_figure:
        plt.savefig(save_filename + file_type) 
                 
    return fig 

def plot_propulsor_data(results,propulsor,axis_1,axis_2,axis_3,axis_4,line_colors,ps,p_i):
    if 'rotor' in  propulsor:
        thrustor = propulsor.rotor
    elif 'propeller' in  propulsor:
        thrustor = propulsor.propeller
        
    for i in range(len(results.segments)): 
        bus_results  =  results.segments[i].conditions.energy
        time         =  results.segments[i].conditions.frames.inertial.time[:,0] / Units.min   
        rpm          =  bus_results[propulsor.tag][thrustor.tag].rpm[:,0]
        thrust       =  np.linalg.norm(bus_results[propulsor.tag][thrustor.tag].thrust , axis =1)
        torque       =  bus_results[propulsor.tag][thrustor.tag].torque[:,0]
        angle        =  bus_results[propulsor.tag].commanded_thrust_vector_angle[:,0]   
        if  i == 0 :
            axis_1.plot(time,rpm, color = line_colors[i], marker = ps.markers[p_i]  , linewidth = ps.line_width, label = thrustor.tag)
        else:
            axis_1.plot(time,rpm, color = line_colors[i], marker = ps.markers[p_i]  , linewidth = ps.line_width)
        axis_1.set_ylabel(r'RPM')
        set_axes(axis_1)    
         
        axis_2.plot(time, angle/Units.degrees, color = line_colors[i], marker = ps.markers[p_i]  , linewidth = ps.line_width) 
        axis_2.set_ylabel(r'Rotor Angle')
        set_axes(axis_2) 
 
        axis_3.plot(time,thrust, color = line_colors[i], marker = ps.markers[p_i] , linewidth = ps.line_width)
        axis_3.set_ylabel(r'Thrust (N)')
        set_axes(axis_3) 
         
        axis_4.plot(time,torque, color = line_colors[i], marker = ps.markers[p_i] , linewidth = ps.line_width)
        axis_4.set_ylabel(r'Torque (N-m)')
        set_axes(axis_4)     
    return 