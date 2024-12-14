# RCAIDE/Library/Components/Propulsors/Turboshaft.py
# 
#  
# Created:  Mar 2024, M. Clarke
# Modified: Jun 2024, M. Guidotti & D.J. Lee

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
## RCAIDE imports
import RCAIDE
from RCAIDE.Framework.Core                  import Data
from .                                      import Propulsor  
from RCAIDE.Library.Methods.Propulsors.Turboshaft_Propulsor.append_turboshaft_conditions     import append_turboshaft_conditions 
from RCAIDE.Library.Methods.Propulsors.Turboshaft_Propulsor.compute_turboshaft_performance   import compute_turboshaft_performance, reuse_stored_turboshaft_data
 
# ----------------------------------------------------------------------
#  Turboshaft
# ----------------------------------------------------------------------
class Turboshaft(Propulsor):
    """This is a turboshaft propulsor

    Assumptions:
    None

    Source:
    None
    """ 
    def __defaults__(self):
        # setting the default values
        self.tag                                              = 'Turboshaft'
        self.fuel_type                                        = RCAIDE.Library.Attributes.Propellants.Jet_A1()
        self.active_fuel_tanks                                = None
        self.nacelle                                          = None  
        self.ram                                              = None 
        self.inlet_nozzle                                     = None 
        self.compressor                                       = None 
        self.low_pressure_turbine                             = None 
        self.high_pressure_turbine                            = None 
        self.combustor                                        = None 
        self.afterburner                                      = None
        self.core_nozzle                                      = None      
                                                              
        self.engine_length                                    = 0.0
        self.bypass_ratio                                     = 0.0 
        self.design_isa_deviation                             = 0.0
        self.design_altitude                                  = 0.0
        self.afterburner_active                               = False
        self.SFC_adjustment                                   = 0.0  
        self.reference_temperature                            = 288.15
        self.reference_pressure                               = 1.01325*10**5 
        self.design_thrust                                    = 0.0
        self.design_power                                     = 0.0
        self.mass_flow_rate_design                            = 0.0 
        self.conversion_efficiency                            = 0.5
        self.compressor_nondimensional_massflow               = 0.0
        self.OpenVSP_flow_through                             = False
                                                              
        #areas needed for drag; not in there yet              
        self.areas                                            = Data()
        self.areas.wetted                                     = 0.0
        self.areas.maximum                                    = 0.0
        self.areas.exit                                       = 0.0
        self.areas.inflow                                     = 0.0 

    def append_operating_conditions(self,segment):
        append_turboshaft_conditions(self,segment)
        return

    def unpack_propulsor_unknowns(self,segment):   
        return 

    def pack_propulsor_residuals(self,segment): 
        return    

    def append_propulsor_unknowns_and_residuals(self,segment): 
        return
    
    def compute_performance(self,state,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power,stored_results_flag,stored_propulsor_tag =  compute_turboshaft_performance(self,state,center_of_gravity)
        return thrust,moment,power,stored_results_flag,stored_propulsor_tag
    
    def reuse_stored_data(turboshaft,state,network,stored_propulsor_tag,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power  = reuse_stored_turboshaft_data(turboshaft,state,network,stored_propulsor_tag,center_of_gravity)
        return thrust,moment,power 
