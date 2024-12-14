# RCAIDE/Library/Components/Propulsors/Turboprop.py 
#
#
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from .                          import Propulsor
from RCAIDE.Library.Methods.Propulsors.Turboprop_Propulsor.append_turboprop_conditions     import append_turboprop_conditions 
from RCAIDE.Library.Methods.Propulsors.Turboprop_Propulsor.compute_turboprop_performance   import compute_turboprop_performance, reuse_stored_turboprop_data
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Fan Component
# ---------------------------------------------------------------------------------------------------------------------- 
class Turboprop(Propulsor):
    """This is a turboprop propulsor
    
    Assumptions:
    None

    Source:
    None
    """ 
    def __defaults__(self):    
        # setting the default values
        self.tag                                      = 'turboprop'   
        self.nacelle                                  = None 
        self.compressor                               = None  
        self.turbine                                  = None  
        self.combustor                                = None  
        self.active_fuel_tanks                        = None         
        self.engine_diameter                          = 0.0      
        self.engine_length                            = 0.0
        self.engine_height                            = 0.5      
        self.design_isa_deviation                     = 0.0
        self.design_altitude                          = 0.0
        self.design_propeller_efficiency              = 0.0
        self.design_gearbox_efficiency                = 0.0 
        self.design_mach_number                       = 0.0
        self.compressor_nondimensional_massflow       = 0.0
        self.reference_temperature                    = 288.15
        self.reference_pressure                       = 1.01325*10**5  
    
    def append_operating_conditions(self,segment):
        append_turboprop_conditions(self,segment)
        return

    def unpack_propulsor_unknowns(self,segment):   
        return 

    def pack_propulsor_residuals(self,segment): 
        return

    def append_propulsor_unknowns_and_residuals(self,segment): 
        return    
    
    def compute_performance(self,state,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power,stored_results_flag,stored_propulsor_tag =  compute_turboprop_performance(self,state,center_of_gravity)
        return thrust,moment,power,stored_results_flag,stored_propulsor_tag
    
    def reuse_stored_data(turboprop,state,network,stored_propulsor_tag,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power  = reuse_stored_turboprop_data(turboprop,state,network,stored_propulsor_tag,center_of_gravity)
        return thrust,moment,power 