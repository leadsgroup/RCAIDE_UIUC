# RCAIDE/Library/Components/Propulsors/Converters/Compressor.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Feb 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from RCAIDE.Library.Components                      import Component  
from RCAIDE.Library.Methods.Propulsors.Converters.Supersonic_Nozzle.append_supersonic_nozzle_conditions import append_supersonic_nozzle_conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  Compressor 
# ----------------------------------------------------------------------------------------------------------------------  
class Supersonic_Nozzle(Component):
    """This is a nozzle component that allows for supersonic outflow.
    Calling this class calls the compute function.
    
    Assumptions:
    Pressure ratio and efficiency do not change with varying conditions.
    
    Source:
    https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/
    """
    
    def __defaults__(self):
        """ This sets the default values for the component to function.
        
        Assumptions:
        None
    
        Source:
        N/A
    
        Inputs:
        None
    
        Outputs:
        None
    
        Properties Used:
        None
        """        
        
        #set the defaults
        self.tag                             = 'Supersonic_Nozzle'
        self.polytropic_efficiency           = 1.0
        self.pressure_ratio                  = 1.0
        self.pressure_recovery               = 1.0 
        self.max_area_ratio                  = 1000.
        self.min_area_ratio                  = 0.

    def append_operating_conditions(self,segment,propulsor): 
        propulsor_conditions =  segment.state.conditions.energy[propulsor.tag]
        append_supersonic_nozzle_conditions(self,segment,propulsor_conditions)
        return 