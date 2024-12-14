# RCAIDE/Library/Plots/Thermal_Management/plot_thermal_management_components.py
# 
# 
# Created:  Sep 2024, S. Shekar
# ----------------------------------------------------------------------------------------------------------------------
#   plot_thermal_management_component
# ----------------------------------------------------------------------------------------------------------------------   
def plot_thermal_management_component(results,
                        save_figure   = False,
                        show_legend   = True,
                        file_type     =".png",
                        width         = 12,
                        height        = 7):
    """Checks and plots all componenents of a thermal management system.
    
     Assumptions:
     None
    
     Source:
     None
    
     Inputs:
     results
     Outputs:
     Plots
    
     Properties Used:
     N/A	
     """     
    
    for network in  results.segments[0].analyses.energy.vehicle.networks:
        for coolant_line in  network.coolant_lines:
            for tag, item in  coolant_line.items():
                if coolant_line.identical_battery_modules:
                    if tag == 'battery_modules':
                            for i, battery in enumerate(item):
                                for btms in  (battery):
                                    if i ==  0:
                                        btms.plot_operating_conditions(results,coolant_line,save_figure,show_legend,btms.tag,file_type,width, height)
                else:
                    for _, battery in enumerate(item):
                            for btms in  (battery):
                                btms.plot_operating_conditions(results,coolant_line,save_figure,show_legend,btms.tag,file_type,width, height)
                if tag == 'heat_exchangers':
                    for heat_exchanger in  item:
                        heat_exchanger.plot_operating_conditions(results,coolant_line,save_figure,show_legend,heat_exchanger.tag,file_type,width, height)
                if tag == 'reservoirs':
                    for reservoir in  item:
                        reservoir.plot_operating_conditions(results,coolant_line,save_figure,show_legend,reservoir.tag,file_type,width, height)             
    return