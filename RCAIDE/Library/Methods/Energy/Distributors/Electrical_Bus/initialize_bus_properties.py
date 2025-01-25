#  RCAIDE/Methods/Energy/Distributors/Electrical_Bus/initialize_bus_properties.py
# 
# Created: Sep 2024, S. Shekar
#
from RCAIDE.Library.Methods.Energy.Sources.Batteries.Common                    import compute_module_properties 

# ----------------------------------------------------------------------------------------------------------------------
#  METHODS
# ---------------------------------------------------------------------------------------------------------------------- 
def initialize_bus_properties(bus): 
    """ Initializes the bus electrical properties based what is appended onto the bus
        
        Assumptions:
        N/A
    
        Source:
        N/A
    
        Inputs:  
       
        Outputs:
           
        Properties Used:
        None
        """
    if bus.battery_module_electric_configuration == 'Series':
        bus.nominal_capacity = 0
        bus.maximum_energy   = 0
        for battery_module in  bus.battery_modules: 
            compute_module_properties(battery_module) 
            bus.voltage         +=  battery_module.voltage
            bus.maximum_energy  +=  battery_module.maximum_energy
            bus.nominal_capacity =  max(battery_module.nominal_capacity, bus.nominal_capacity)  
    elif bus.battery_module_electric_configuration == 'Parallel':
        bus.voltage = 0
        bus.maximum_energy   = 0
        for battery_module in  bus.battery_modules: 
            compute_module_properties(battery_module)        
            bus.voltage           =  max(battery_module.voltage, bus.voltage)
            bus.nominal_capacity +=  battery_module.nominal_capacity        
            bus.maximum_energy  +=  battery_module.initial_maximum_energy 
    return