## @ingroup Library-Methods-Energy-Thermal_Management-Common-Heat-Exchanger-Systems
# cross_flow_heat_exchanger_geometry_setup.py 
#
# Created: Jun 2023, M. Clarke

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------  
# RCAIDE Imports 
import RCAIDE     


## @ingroup Methods-Thermal_Management-Batteries-Sizing
def cross_flow_heat_exchanger_geometry_setup(HEX): 
    """ Modifies geometry of Cross Flow Heat Exchanger  
          
          Inputs:  
             nexus     - RCAIDE optmization framework with Wavy Channel geometry data structure [None]
              
          Outputs:   
             procedure - optimization methodology                                       
              
          Assumptions: 
             N/A 
        
          Source:
             None
    """            
    vehicle                                        = RCAIDE.Vehicle()  
    net                                            = RCAIDE.Framework.Networks.All_Electric_Network()  
    bus                                            = RCAIDE.Library.Components.Energy.Distribution.Electrical_Bus()
    bat                                            = RCAIDE.Library.Components.Energy.Batteries.Lithium_Ion_NMC()   
     
    HEX.coolant_temperature_of_hot_fluid                  = 313 # Temperature from reservior
    bat.thermal_management_system.heat_exchanger_system   = HEX 
    bus.batteries.append(bat)
    net.busses.append(bus) 
    vehicle.append_energy_network(net)
    
    configs                             = RCAIDE.Library.Components.Configs.Config.Container()
    base_config                         = RCAIDE.Library.Components.Configs.Config(vehicle)  
    config                              = RCAIDE.Library.Components.Configs.Config(base_config)
    config.tag                          = 'optimized'  
    configs.append(config)         
    return configs 