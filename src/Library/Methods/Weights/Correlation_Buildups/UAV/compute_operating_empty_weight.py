# RCAIDE/Library/Methods/Weights/Correlation_Buildups/UAV/compute_operating_empty_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE
import RCAIDE
from RCAIDE.Framework.Core    import  Data  
 
 # ----------------------------------------------------------------------------------------------------------------------
# Compute Operating Empty Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_operating_empty_weight(vehicle):
    """ This computes the weigt of a UAV   
    
    Assumptions:
        Assumes a 'main wing' is attached

    Source:
        Structural Weight correlation from all 415 samples of fixed-wing UAVs and sailplanes
        Equation 3.16 from 'Design of Solar Powered Airplanes for Continuous Flight' by Andre Noth
        Relatively valid for a wide variety of vehicles, may be optimistic 

    Inputs:
        S                [meters**2]
        AR               [dimensionless]
        
    Outputs:
        weight           [kilograms]

    Properties Used:
        N/A
    """    
    # ----------------------------------------------------------------------------------------------------------------------
    # Unpack
    # ----------------------------------------------------------------------------------------------------------------------
    S     = vehicle.reference_area
    
    # ----------------------------------------------------------------------------------------------------------------------
    #  find max wing area and aspect ratio 
    # ----------------------------------------------------------------------------------------------------------------------    
    S_max = 0
    for wing in vehicle.wings:
        if S_max < wing.areas.reference:
            AR    = wing.aspect_ratio 
            S_max = wing.areas.reference 
        if isinstance(wing,RCAIDE.Library.Components.Wings.Main_Wing):
            AR = wing.aspect_ratio
            break 
            
    Earth = RCAIDE.Library.Attributes.Planets.Earth()
    g     = Earth.sea_level_gravity 
    
    # ----------------------------------------------------------------------------------------------------------------------
    # Airframe weight
    # ----------------------------------------------------------------------------------------------------------------------
    W_airframe   = (5.58*(S**1.59)*(AR**0.71))/g  
    
    # Pack
    weight              = Data()
    weight.empty        = Data()
    weight.empty.total  = W_airframe
    
    return weight