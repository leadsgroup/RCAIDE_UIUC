# RCAIDE/Library/Components/Propulsors/Turbofan.py 
#
#
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports  
from RCAIDE.Framework.Core      import Container
from .                          import Propulsor
from RCAIDE.Library.Methods.Propulsors.Turbofan_Propulsor.append_turbofan_conditions     import append_turbofan_conditions 
from RCAIDE.Library.Methods.Propulsors.Turbofan_Propulsor.compute_turbofan_performance   import compute_turbofan_performance, reuse_stored_turbofan_data
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Fan Component
# ---------------------------------------------------------------------------------------------------------------------- 
class Turbofan(Propulsor):
    """This is a turbofan propulsor.
    
    Assumptions:
    None

    Source:
    None
    """ 
    def __defaults__(self):    
        # setting the default values
        self.tag                                      = 'Turbofan'  
        self.nacelle                                  = None 
        self.fan                                      = None 
        self.ram                                      = None 
        self.inlet_nozzle                             = None 
        self.low_pressure_compressor                  = None 
        self.high_pressure_compressor                 = None 
        self.low_pressure_turbine                     = None 
        self.high_pressure_turbine                    = None 
        self.combustor                                = None 
        self.core_nozzle                              = None 
        self.fan_nozzle                               = None  
        self.active_fuel_tanks                        = None         
        self.engine_diameter                          = 0.0      
        self.engine_length                            = 0.0
        self.engine_height                            = 0.5     # Engine centerline heigh above the ground plane
        self.exa                                      = 1       # distance from fan face to fan exit/ fan diameter)
        self.plug_diameter                            = 0.1     # dimater of the engine plug
        self.geometry_xe                              = 1.      # Geometry information for the installation effects function
        self.geometry_ye                              = 1.      # Geometry information for the installation effects function
        self.geometry_Ce                              = 2.      # Geometry information for the installation effects function
        self.bypass_ratio                             = 0.0 
        self.design_isa_deviation                     = 0.0
        self.design_altitude                          = 0.0
        self.SFC_adjustment                           = 0.0 # Less than 1 is a reduction
        self.compressor_nondimensional_massflow       = 0.0
        self.reference_temperature                    = 288.15
        self.reference_pressure                       = 1.01325*10**5 
        self.design_thrust                            = 0.0
        self.mass_flow_rate_design                    = 0.0
        self.OpenVSP_flow_through                     = False
    
    def append_operating_conditions(self,segment):
        append_turbofan_conditions(self,segment)
        return

    def unpack_propulsor_unknowns(self,segment):   
        return 

    def pack_propulsor_residuals(self,segment): 
        return

    def append_propulsor_unknowns_and_residuals(self,segment): 
        return
    
    def compute_performance(self,state,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power,stored_results_flag,stored_propulsor_tag =  compute_turbofan_performance(self,state,center_of_gravity)
        return thrust,moment,power,stored_results_flag,stored_propulsor_tag
    
    def reuse_stored_data(turbofan,state,network,stored_propulsor_tag,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power  = reuse_stored_turbofan_data(turbofan,state,network,stored_propulsor_tag,center_of_gravity)
        return thrust,moment,power 