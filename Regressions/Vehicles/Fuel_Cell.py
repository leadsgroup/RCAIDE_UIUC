# Regressions/Vehicles/Isolated_Battery_Cell.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE  
from RCAIDE.Framework.Core                                    import Units 
 
# ----------------------------------------------------------------------------------------------------------------------
#  Build the Vehicle
# ----------------------------------------------------------------------------------------------------------------------   

def vehicle_setup(fuel_cell_model): 

    vehicle                       = RCAIDE.Vehicle() 
    vehicle.tag                   = 'battery'   
    vehicle.reference_area        = 1
 
    # ################################################# Vehicle-level Properties #####################################################   
    # mass properties
    vehicle.mass_properties.takeoff         = 1 * Units.kg 
    vehicle.mass_properties.max_takeoff     = 1 * Units.kg 
         
    net                              = RCAIDE.Framework.Networks.Electric() 
    #------------------------------------------------------------------------------------------------------------------------------------  
    # Bus
    #------------------------------------------------------------------------------------------------------------------------------------  
    bus                                  = RCAIDE.Library.Components.Energy.Distributors.Electrical_Bus() 
    if fuel_cell_model == 'PEM': 
        fuel_cell_stack = RCAIDE.Library.Components.Energy.Sources.Fuel_Cell_Stacks.Proton_Exchange_Membrane_Fuel_Cell()
    if fuel_cell_model == 'Simple':  
        fuel_cell_stack   = RCAIDE.Library.Components.Energy.Sources.Fuel_Cell_Stacks.Generic_Fuel_Cell_Stack()
    if fuel_cell_model == 'Larminie':  
        fuel_cell_stack   = RCAIDE.Library.Components.Energy.Sources.Fuel_Cell_Stacks.Generic_Fuel_Cell_Stack()
        fuel_cell_stack.discharge_model =  'Larminie'
        
    bus.fuel_cell_stacks.append(fuel_cell_stack)  
    bus.initialize_bus_properties()

    #------------------------------------------------------------------------------------------------------------------------------------           
    # Payload 
    #------------------------------------------------------------------------------------------------------------------------------------  
    payload                      = RCAIDE.Library.Components.Payloads.Payload()
    payload.power_draw           = 1
    payload.mass_properties.mass = 1.0 * Units.kg
    bus.payload                  = payload      
    # append bus   
    net.busses.append(bus) 
    
    # append network 
    vehicle.append_energy_network(net) 
 
    # ##################################   Determine Vehicle Mass Properties Using Physic Based Methods  ################################       
    vehicle.mass_properties.takeoff = fuel_cell_stack.mass_properties.mass 
    return vehicle


def configs_setup(vehicle): 
    configs  = RCAIDE.Library.Components.Configs.Config.Container()  
    base     = RCAIDE.Library.Components.Configs.Config(vehicle)
    base.tag = 'base' 
    configs.append(base)
     
    return configs 