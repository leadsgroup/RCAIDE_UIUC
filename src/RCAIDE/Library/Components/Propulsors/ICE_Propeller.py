# RCAIDE/Library/Components/Propulsors/ICE_Propeller.py
# 
#  
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from .                import Propulsor  
from RCAIDE.Library.Methods.Propulsors.ICE_Propulsor.unpack_ice_propeller_unknowns   import unpack_ice_propeller_unknowns
from RCAIDE.Library.Methods.Propulsors.ICE_Propulsor.pack_ice_propeller_residuals    import pack_ice_propeller_residuals
from RCAIDE.Library.Methods.Propulsors.ICE_Propulsor.append_ice_propeller_conditions import append_ice_propeller_conditions
from RCAIDE.Library.Methods.Propulsors.ICE_Propulsor.compute_ice_performance         import compute_ice_performance, reuse_stored_ice_data
from RCAIDE.Library.Methods.Propulsors.ICE_Propulsor.append_ice_residual_and_unknown import  append_ice_residual_and_unknown
 

# ---------------------------------------------------------------------------------------------------------------------- 
# ICE_Propeller
# ---------------------------------------------------------------------------------------------------------------------- 
class ICE_Propeller(Propulsor):
    """This is an internal engine-propeller propulsor
    
    Assumptions:
    None

    Source:
    None
    """ 
    def __defaults__(self):    
        # setting the default values
        self.tag                          = 'ice_propeller'   
        self.active_fuel_tanks            = None
        self.engine                       = None
        self.propeller                    = None
        self.engine_diameter              = 0.0      
        self.engine_length                = 0.0
        self.engine_mass                  = 0.0

    def append_operating_conditions(self,segment):
        append_ice_propeller_conditions(self,segment)
        return

    def unpack_propulsor_unknowns(self,segment):  
        unpack_ice_propeller_unknowns(self,segment)
        return 

    def pack_propulsor_residuals(self,segment): 
        pack_ice_propeller_residuals(self,segment)
        return

    def append_propulsor_unknowns_and_residuals(self,segment):
        append_ice_residual_and_unknown(self,segment)
        return    
    
    def compute_performance(self,state,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power,stored_results_flag,stored_propulsor_tag =  compute_ice_performance(self,state,center_of_gravity)
        return thrust,moment,power,stored_results_flag,stored_propulsor_tag
    
    def reuse_stored_data(ICE_prop,state,network,stored_propulsor_tag,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power  = reuse_stored_ice_data(ICE_prop,state,network,stored_propulsor_tag,center_of_gravity)
        return thrust,moment,power 