# RCAIDE/Library/Components/Propulsors/Converters/Compressor.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Feb 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from RCAIDE.Library.Components                      import Component  
from RCAIDE.Library.Methods.Propulsors.Converters.Compressor.append_compressor_conditions import append_compressor_conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  Compressor 
# ---------------------------------------------------------------------------------------------------------------------- 
class Compressor(Component):
    """This is a compressor component typically used in a turbofan or turbojet.
    """
    
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
            None

        Source:
            None 
        """          
        #set the default values
        self.tag                             = 'Compressor'
        self.polytropic_efficiency           = 1.0
        self.pressure_ratio                  = 1.0

    def append_operating_conditions(self,segment,propulsor): 
        propulsor_conditions =  segment.state.conditions.energy[propulsor.tag]
        append_compressor_conditions(self,segment,propulsor_conditions)
        return        