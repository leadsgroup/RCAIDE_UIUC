# RCAIDE/Library/Components/Propulsors/Electric_Rotor.py
#  
# 
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports 
from .   import Propulsor 
from RCAIDE.Library.Methods.Propulsors.Electric_Rotor_Propulsor.unpack_electric_rotor_unknowns             import unpack_electric_rotor_unknowns
from RCAIDE.Library.Methods.Propulsors.Electric_Rotor_Propulsor.pack_electric_rotor_residuals              import pack_electric_rotor_residuals
from RCAIDE.Library.Methods.Propulsors.Electric_Rotor_Propulsor.append_electric_rotor_conditions           import append_electric_rotor_conditions
from RCAIDE.Library.Methods.Propulsors.Electric_Rotor_Propulsor.compute_electric_rotor_performance         import compute_electric_rotor_performance, reuse_stored_electric_rotor_data
from RCAIDE.Library.Methods.Propulsors.Electric_Rotor_Propulsor.append_electric_rotor_residual_and_unknown import append_electric_rotor_residual_and_unknown

# ---------------------------------------------------------------------------------------------------------------------- 
#  Electric_Rotor
# ----------------------------------------------------------------------------------------------------------------------  
class Electric_Rotor(Propulsor):
    """This is a electric motor-rotor propulsor 
    
    Assumptions:
    None

    Source:
    None
    """ 
    def __defaults__(self):    
        # setting the default values
        self.tag                          = 'electric_rotor'    
        self.motor                        = None
        self.rotor                        = None 
        self.electronic_speed_controller  = None 

    def append_operating_conditions(self,segment):
        append_electric_rotor_conditions(self,segment)
        return
    
    def append_propulsor_unknowns_and_residuals(self,segment):
        append_electric_rotor_residual_and_unknown(self,segment)
        return

    def unpack_propulsor_unknowns(self,segment):  
        unpack_electric_rotor_unknowns(self,segment)
        return 

    def pack_propulsor_residuals(self,segment): 
        pack_electric_rotor_residuals(self,segment)
        return    
    
    def compute_performance(self,state,voltage,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power,stored_results_flag,stored_propulsor_tag =  compute_electric_rotor_performance(self,state,voltage,center_of_gravity)
        return thrust,moment,power,stored_results_flag,stored_propulsor_tag
    
    def reuse_stored_data(electric_rotor,state,network,stored_propulsor_tag,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power = reuse_stored_electric_rotor_data(electric_rotor,state,network,stored_propulsor_tag,center_of_gravity)
        return thrust,moment,power
