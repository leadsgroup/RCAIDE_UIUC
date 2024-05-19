## @ingroup Library-Plots-Performance-Aerodynamics
# RCAIDE/Library/Plots/Performance/Aerodynamics/plot_drag_components.py
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
def plot_drag_components(results,
                         save_figure=False,
                         show_legend= True,
                         save_filename="Drag_Components",
                         file_type=".png",
                        width = 12, height = 7):
    """This plots the drag components of the aircraft
    
    Assumptions:
    None
    
    Source:
    None
    
    Inputs:
    results.segments.condtions.aerodynamics.drag_breakdown
          parasite.total
          induced.total
          compressible.total
          miscellaneous.total
          
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
    fig.set_size_inches(12,height)
    
    for i in range(len(results.segments)): 
        time   = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min 
        drag_breakdown = results.segments[i].conditions.aerodynamics.drag_breakdown
        cdp = drag_breakdown.parasite.total[:,0]
        cdi = drag_breakdown.induced.total[:,0]
        cdc = drag_breakdown.compressible.total[:,0]
        cdm = drag_breakdown.miscellaneous.total[:,0]
        cde = np.ones_like(cdm)*drag_breakdown.drag_coefficient_increment
        cd  = drag_breakdown.total[:,0]
         
            
        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ')
        
        axis_1 = plt.subplot(3,2,1)
        axis_1.plot(time, cdp, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name)
        axis_1.set_ylabel(r'$C_{Dp}$')
        set_axes(axis_1)    
        
        axis_2 = plt.subplot(3,2,2)
        axis_2.plot(time,cdi, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width) 
        axis_2.set_ylabel(r'$C_{Di}$')
        set_axes(axis_2) 

        axis_3 = plt.subplot(3,2,3)
        axis_3.plot(time, cdc, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width) 
        axis_3.set_ylabel(r'$C_{Dc}$')
        set_axes(axis_3) 
        
        axis_4 = plt.subplot(3,2,4)
        axis_4.plot(time, cdm, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)
        axis_4.set_ylabel(r'$C_{Dm}$')
        set_axes(axis_4)    
        
        axis_5 = plt.subplot(3,2,5)
        axis_5.plot(time, cde, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)
        axis_5.set_xlabel('Time (mins)')
        axis_5.set_ylabel(r'$C_{De}$')
        set_axes(axis_5) 

        axis_6 = plt.subplot(3,2,6)
        axis_6.plot(time, cd, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)
        axis_6.set_xlabel('Time (mins)')
        axis_6.set_ylabel(r'$C_D$')
        set_axes(axis_6) 
        
    
    if show_legend:                    
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend 
    fig.subplots_adjust(top=0.8)
    
    # set title of plot 
    title_text    = 'Drag Components'      
    fig.suptitle(title_text)
    
    if save_figure:
        plt.savefig(save_filename + file_type)   
    return fig 