# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Propulsion/compute_piston_engine_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core import  Units 
 
# ----------------------------------------------------------------------------------------------------------------------
#  Piston Engine Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_piston_engine_weight(max_power, kwt2=5.22, xwt=.780):
    """ Calculate the weight of an piston engine  
        weight correlation; weight=kwt2*(max_power**xwt)
        Inputs:
                max_power- maximum power the motor can deliver safely [Watts]
                kwt2
                xwt
                
        Outputs:
                weight- weight of the motor [kilograms]
        
        Source: Raymer, Aircraft Design, a Conceptual Approach
        

                
               
    """    
    bhp    = max_power/Units.horsepower
    weight = kwt2*((bhp)**xwt)  # weight in lbs.
    mass   = weight*Units.lbs
    return mass