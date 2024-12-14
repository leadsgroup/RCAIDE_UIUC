# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Common/operating_empty_weight.py
# 
# Created: Sep 2024, M. Clarke 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ----------------------------------------------------------------------------------------------------------------------  
import RCAIDE.Library.Methods.Weights.Correlation_Buildups.Transport.compute_operating_empty_weight as compute_operating_empty_weight_transport

# ---------------------------------------------------------------------------------------------------------------------- 
# Operating Empty Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_operating_empty_weight(vehicle, settings=None,  method_type='RCAIDE'):
    """Computes the operating empty weight of a general aircraft 
    
    Assumptions:
    None
    
    Source:
    N/A
    
    Inputs:
    None
    
    Outputs:
    results 
    """
    output =  compute_operating_empty_weight_transport(vehicle,settings,method_type) 

    return output
