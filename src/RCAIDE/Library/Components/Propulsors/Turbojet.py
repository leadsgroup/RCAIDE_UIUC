# RCAIDE/Library/Components/Propulsors/Turbojet.py  
#
#
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
## RCAIDE imports   
from RCAIDE.Framework.Core      import Data
from .                          import Propulsor
from RCAIDE.Library.Methods.Propulsors.Turbojet_Propulsor.append_turbojet_conditions     import append_turbojet_conditions 
from RCAIDE.Library.Methods.Propulsors.Turbojet_Propulsor.compute_turbojet_performance   import compute_turbojet_performance, reuse_stored_turbojet_data
 
 
# ----------------------------------------------------------------------
#  Turbojet Propulsor
# ---------------------------------------------------------------------- 
class Turbojet(Propulsor):
    """This is a  turbojet propulsor

    Assumptions:
    None

    Source:
    None
    """ 
    def __defaults__(self):
        # setting the default values
        self.tag                                      = 'Turbojet' 
        self.active_fuel_tanks                        = None
        self.nacelle                                  = None  
        self.ram                                      = None 
        self.inlet_nozzle                             = None 
        self.low_pressure_compressor                  = None 
        self.high_pressure_compressor                 = None 
        self.low_pressure_turbine                     = None 
        self.high_pressure_turbine                    = None 
        self.combustor                                = None 
        self.afterburner                              = None
        self.core_nozzle                              = None      
        
        self.engine_length                            = 0.0
        self.bypass_ratio                             = 0.0 
        self.design_isa_deviation                     = 0.0
        self.design_altitude                          = 0.0
        self.afterburner_active                       = False
        self.SFC_adjustment                           = 0.0  
        self.compressor_nondimensional_massflow       = 0.0
        self.reference_temperature                    = 288.15
        self.reference_pressure                       = 1.01325*10**5 
        self.design_thrust                            = 0.0
        self.mass_flow_rate_design                    = 0.0 
        self.OpenVSP_flow_through                     = False

        #areas needed for drag; not in there yet
        self.areas                                    = Data()
        self.areas.wetted                             = 0.0
        self.areas.maximum                            = 0.0
        self.areas.exit                               = 0.0
        self.areas.inflow                             = 0.0 


    def append_operating_conditions(self,segment):
        append_turbojet_conditions(self,segment)
        return

    def unpack_propulsor_unknowns(self,segment):   
        return 

    def pack_propulsor_residuals(self,segment): 
        return        

    def append_propulsor_unknowns_and_residuals(self,segment): 
        return
    
    def compute_performance(self,state,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power,stored_results_flag,stored_propulsor_tag =  compute_turbojet_performance(self,state,center_of_gravity)
        return thrust,moment,power,stored_results_flag,stored_propulsor_tag
    
    def reuse_stored_data(turbojet,state,network,stored_propulsor_tag,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power  = reuse_stored_turbojet_data(turbojet,state,network,stored_propulsor_tag,center_of_gravity)
        return thrust,moment,power 