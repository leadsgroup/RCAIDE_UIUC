# RCAIDE/Library/Plots/Performance/Aerodynamics/plot_airfoil_polar_files.py
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
def plot_airfoil_polar_files(polar_data,
                             save_figure = False,
                             save_filename = "Airfoil_Polars",
                             file_type = ".png",
                             width = 11, height = 7):
    """This plots all airfoil polars in the list "airfoil_polar_paths" 

    Assumptions:
    None

    Source:
    None

    Inputs:
    airfoil_polar_paths   [list of strings]

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
    
    
    # Get raw data polars
    CL           = polar_data.lift_coefficients
    CD           = polar_data.drag_coefficients
    alpha        = polar_data.angle_of_attacks/Units.degrees
    Re_raw       = polar_data.reynolds_numbers
    n_Re         = len(polar_data.re_from_polar) 
        
     
    # get line colors for plots 
    line_colors   = cm.inferno(np.linspace(0,0.9,n_Re))     
     
    fig   = plt.figure(save_filename)
    fig.set_size_inches(width,height) 
      
    for j in range(n_Re):
        
        Re_val = str(round(Re_raw[j])/1e6)+'e6'  
        
        axis_1 = plt.subplot(2,2,1)
        axis_1.plot(alpha, CL[j,:], color = line_colors[j], marker = ps.markers[0], linewidth = ps.line_width, label ='Re='+Re_val)
        axis_1.set_ylabel(r'$C_l$')
        axis_1.set_xlabel(r'$\alpha$')
        set_axes(axis_1)    
        
        axis_2 = plt.subplot(2,2,2)
        axis_2.plot(alpha,CD[j,:], color = line_colors[j], marker = ps.markers[0], linewidth = ps.line_width, label ='Re='+Re_val) 
        axis_2.set_ylabel(r'$C_d$')
        axis_2.set_xlabel(r'$\alpha$')
        set_axes(axis_2)  
        
        axis_3 = plt.subplot(2,2,3)
        axis_3.plot(CL[j,:],CD[j,:], color = line_colors[j], marker = ps.markers[0], linewidth = ps.line_width, label ='Re='+Re_val)
        axis_3.set_xlabel('$C_l$')
        axis_3.set_ylabel(r'$C_d$')
        set_axes(axis_3) 
    
        axis_4 = plt.subplot(2,2,4)
        axis_4.plot(alpha, CL[j,:]/CD[j,:], color = line_colors[j], marker = ps.markers[0], linewidth = ps.line_width, label ='Re='+Re_val) 
        axis_4.set_ylabel(r'$Cl/Cd$')
        axis_4.set_xlabel(r'$\alpha$')
        set_axes(axis_4)   
     
    # set title of plot 
    title_text    = 'Airfoil Polars'      
    fig.suptitle(title_text)
    
    if save_figure:
        plt.savefig(save_filename + file_type)   
    return fig