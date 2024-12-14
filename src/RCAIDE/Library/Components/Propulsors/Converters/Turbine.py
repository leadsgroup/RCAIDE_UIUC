# RCAIDE/Library/Components/Propulsors/Converters/Turbine.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports  
from RCAIDE.Library.Components                      import Component   
from RCAIDE.Library.Methods.Propulsors.Converters.Turbine.append_turbine_conditions import append_turbine_conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  Turbine
# ----------------------------------------------------------------------------------------------------------------------  
class Turbine(Component):
    """This is a turbine component typically used in a turbofan or turbojet
    
    Assumptions:
        Efficiencies do not change with varying conditions.

    Source:
         https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/
    """
    
    def __defaults__(self):
        """ This sets the default values for the component to function.

        Assumptions:
            None

        Source:
            None 
        """         
        #set the default values
        self.tag                               ='Turbine'
        self.mechanical_efficiency             = 1.0
        self.polytropic_efficiency             = 1.0

    def append_operating_conditions(self,segment,propulsor): 
        propulsor_conditions =  segment.state.conditions.energy[propulsor.tag]
        append_turbine_conditions(self,segment,propulsor_conditions)
        return                            
    