# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Common/compute_landing_gear_weight.py
# 
# Created: Sep 2024, M. Clarke 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ----------------------------------------------------------------------------------------------------------------------
from RCAIDE.Framework.Core import Data 

# ---------------------------------------------------------------------------------------------------------------------- 
# Landing Gear 
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_landing_gear_weight(vehicle,landing_gear_W_factor=0.04):
    """ Calculate the weight of the landing gear assuming that the gear 
    weight is 4 percent of the takeoff weight        
    
    Assumptions:
        calculating the landing gear weight based on the takeoff weight
    
    Source: 
        N/A
        
    Inputs:
        TOW - takeoff weight of the aircraft                              [kilograms]
        landing_gear_W_factor - landing gear weight as percentage of TOW [dimensionless]
    
    Outputs:
        weight - weight of the landing gear                               [kilograms]
            
    Properties Used:
        N/A
    """

    # process
    weight          = landing_gear_W_factor * vehicle.mass_properties.max_takeoff
    output          = Data()
    output.main     = weight * 0.9
    output.nose     = weight * 0.1
    return output
