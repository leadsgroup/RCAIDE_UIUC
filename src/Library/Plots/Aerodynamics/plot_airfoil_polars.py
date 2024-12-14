# RCAIDE/Library/Plots/Performance/Aerodynamics/plot_airfoil_polars.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Framework.Core import Units
from RCAIDE.Library.Plots.Common import set_axes, plot_style
import matplotlib.pyplot as plt 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------     

def plot_airfoil_polars(polar_data,
                        save_figure   = False,
                        save_filename = "Airfoil_Polars",
                        file_type = ".png",
                        width = 11, height = 7):
    """This plots all the airfoil polars of a specfic airfoil

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
 
    # Get raw data polars 
    CL           = polar_data.cl_invisc[0]
    CD           = polar_data.cd_invisc[0]
    CM           = polar_data.cm_invisc[0]
    alpha        = polar_data.AoA[0]/Units.degrees
    Re_raw       = polar_data.Re[0]  
       
    Re_val = str(round(Re_raw[0])/1e6)+'e6' 
    
    # get plotting style 
    ps      = plot_style()  

    parameters = {'axes.labelsize': ps.axis_font_size,
                  'xtick.labelsize': ps.axis_font_size,
                  'ytick.labelsize': ps.axis_font_size,
                  'axes.titlesize': ps.title_font_size}
    plt.rcParams.update(parameters)
      
    fig   = plt.figure(save_filename)
    fig.set_size_inches(width,height) 
               
    axis_1 = plt.subplot(2,2,1)
    axis_1.plot(alpha, CL, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width, label = 'Re = '+Re_val)
    axis_1.set_ylabel(r'$C_l$')
    set_axes(axis_1)    
    
    axis_2 = plt.subplot(2,2,2)
    axis_2.plot(alpha, CD, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width)
    axis_2.set_ylabel(r'$C_d$')
    set_axes(axis_2) 

    axis_3 = plt.subplot(2,2,3)
    axis_3.plot(alpha, CM, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width)
    axis_3.set_xlabel('AoA [deg]') 
    axis_3.set_ylabel(r'$C_m$')
    set_axes(axis_3) 
    
    axis_4 = plt.subplot(2,2,4)
    axis_4.plot(alpha, CL/CD, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width)
    axis_4.set_xlabel('AoA [deg]')
    axis_4.set_ylabel(r'Cl/Cd')
    axis_4.set_ylim([-20,20])
    set_axes(axis_4) 
            
    if save_figure:
        plt.savefig(save_filename + file_type)   
    return  fig
     
     
     
     