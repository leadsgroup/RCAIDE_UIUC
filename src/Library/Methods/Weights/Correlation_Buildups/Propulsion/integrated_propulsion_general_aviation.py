# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Propulsion/integrated_propulsion_general_aviation.py
# 
# 
# Created:  Sep 2024, M. Clarke 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core import  Units

# ----------------------------------------------------------------------------------------------------------------------
#  Integrated Propulsion Weight 
# ----------------------------------------------------------------------------------------------------------------------
def integrated_propulsion_general_aviation(piston_engine_weight,num_eng, engine_W_factor = 2.575, engine_W_exp = .922):
    """ 
        Calculate the weight of the entire propulsion system        

        Source:
                Source: Raymer, Aircraft Design, a Conceptual Approach        
                
        Inputs:
                piston_engine_weight - dry weight of a single engine                                     [kilograms]
                num_eng - total number of engines on the aircraft                                 [dimensionless]
                engine_W_factor - weight increase factor for entire integrated propulsion system [dimensionless]
        
        Outputs:
                weight - weight of the full propulsion system [kilograms]

    """     
    engine_dry = piston_engine_weight/Units.lbs
    weight     = engine_W_factor * (engine_dry**engine_W_exp)*num_eng
    mass       = weight*Units.lbs #convert to kg

    return mass