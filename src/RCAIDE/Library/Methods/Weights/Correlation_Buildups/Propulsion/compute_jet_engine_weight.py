# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Propulsion/compute_jet_engine_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core import  Units 
 
# ----------------------------------------------------------------------------------------------------------------------
#  Jet Engine Weight 
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_jet_engine_weight(thrust_sls):
    """ Calculate the weight of the dry engine  
    
    Assumptions:
            calculated engine weight from a correlation of engines
    
    Source: 
            N/A
            
    Inputs:
            thrust_sls - sea level static thrust of a single engine [Newtons]
    
    Outputs:
            weight - weight of the dry engine                       [kilograms]
        
    Properties Used:
            N/A
    """     
    # setup
    thrust_sls_en = thrust_sls / Units.force_pound # Convert N to lbs force  
    
    # process
    weight = (0.4054*thrust_sls_en ** 0.9255) * Units.lb # Convert lbs to kg
    
    return weight