# RCAIDE/Library/Components/Propulsors/Converters/Compression_Nozzle.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Feb 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from RCAIDE.Library.Components                      import Component  
from RCAIDE.Library.Methods.Propulsors.Converters.Compression_Nozzle.append_compression_nozzle_conditions import append_compression_nozzle_conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  Compression Nozzle 
# ---------------------------------------------------------------------------------------------------------------------- 
class Compression_Nozzle(Component):
    """This is a nozzle component intended for use in compression. 
    """

    def __defaults__(self): 
        """This sets the default values for the component to function.

        Assumptions:
            1. Pressure ratio and efficiency do not change with varying conditions.
            2. Subsonic or choked output.

        Source:
            https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/
        """    
        self.tag                             = 'Nozzle'
        self.polytropic_efficiency           = 1.0
        self.pressure_ratio                  = 1.0
        self.pressure_recovery               = 1.0
        self.compressibility_effects         = False 
        self.compression_levels              = 0.0
        self.theta                           = 0.0

    def append_operating_conditions(self,segment,propulsor): 
        propulsor_conditions =  segment.state.conditions.energy[propulsor.tag]
        append_compression_nozzle_conditions(self,segment,propulsor_conditions)
        return