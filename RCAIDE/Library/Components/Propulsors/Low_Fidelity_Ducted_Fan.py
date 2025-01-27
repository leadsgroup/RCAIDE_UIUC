# RCAIDE/Library/Components/Propulsors/Low_Fidelity_Ducted_Fan.py 
#
#
# Created:  Jan 2025, M. Guidotti

## ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
## RCAIDE imports   
from RCAIDE.Framework.Core      import Data
from .                          import Propulsor
from RCAIDE.Library.Methods.Propulsors.Low_Fidelity_Ducted_Fan.append_low_fidelity_ducted_fan_conditions     import append_low_fidelity_ducted_fan_conditions 
from RCAIDE.Library.Methods.Propulsors.Low_Fidelity_Ducted_Fan.compute_low_fidelity_ducted_fan_performance   import compute_low_fidelity_ducted_fan_performance, reuse_stored_low_fidelity_ducted_fan_data
 
 
# ----------------------------------------------------------------------
#  low_fidelity_ducted_fan Propulsor
# ---------------------------------------------------------------------- 
class Low_Fidelity_Ducted_Fan(Propulsor):
    """
    """ 
    def __defaults__(self):
        # setting the default values
        self.tag                                      = 'low_fidelity_ducted_fan' 
        self.nacelle                                  = None  
        self.ram                                      = None 
        self.inlet_nozzle                             = None 
        self.fan                                      = None 
        self.exit_nozzle                              = None      
        
        self.engine_length                            = 0.0
        self.engine_diameter                          = 0.0 
        self.engine_height                            = 0.5     # Engine centerline heigh above the ground plane 
        self.exa                                      = 1       # distance from fan face to fan exit/ fan diameter)
        self.design_isa_deviation                     = 0.0
        self.design_altitude                          = 0.0
        self.compressor_nondimensional_massflow       = 0.0
        self.reference_temperature                    = 288.15
        self.reference_pressure                       = 1.01325*10**5 
        self.design_thrust                            = 0.0
        self.mass_flow_rate_design                    = 0.0 
        self.OpenVSP_flow_through                     = False
        self.geometry_xe                              = 1.      # Geometry information for the installation effects function
        self.geometry_ye                              = 1.      # Geometry information for the installation effects function
        self.geometry_Ce                              = 2.      # Geometry information for the installation effects function

        #areas needed for drag; not in there yet
        self.areas                                    = Data()
        self.areas.wetted                             = 0.0
        self.areas.maximum                            = 0.0
        self.areas.exit                               = 0.0
        self.areas.inflow                             = 0.0 


    def append_operating_conditions(self,segment):
        append_low_fidelity_ducted_fan_conditions(self,segment)
        return

    def unpack_propulsor_unknowns(self,segment):   
        return 

    def pack_propulsor_residuals(self,segment): 
        return        

    def append_propulsor_unknowns_and_residuals(self,segment): 
        return
    
    def compute_performance(self,state,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power,stored_results_flag,stored_propulsor_tag =  compute_low_fidelity_ducted_fan_performance(self,state,center_of_gravity)
        return thrust,moment,power,stored_results_flag,stored_propulsor_tag
    
    def reuse_stored_data(low_fidelity_ducted_fan,state,network,stored_propulsor_tag,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power  = reuse_stored_low_fidelity_ducted_fan_data(low_fidelity_ducted_fan,state,network,stored_propulsor_tag,center_of_gravity)
        return thrust,moment,power 