# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Propulsion/integrated_propulsion.py
# 
# 
# Created:  Sep 2024, M. Clarke 
 
# ----------------------------------------------------------------------------------------------------------------------
#  Integrated Propulsion Weight 
# ----------------------------------------------------------------------------------------------------------------------
def integrated_propulsion(jet_engine_weight, engine_W_factor = 1.6):
    """ Calculate the weight of the entire propulsion system 
    
    Assumptions:
            The propulsion system is a fixed 60% greater than the dry engine alone. 
            The propulsion system includes the engines, engine exhaust, reverser, starting,
            controls, lubricating, and fuel systems. The nacelle and pylon weight are also
            part of this calculation.           
            
    Source: 
            N/A
            
    Inputs:
            compute_jet_engine_weight - dry weight of the engine                                             [kilograms]
            num_eng - total number of engines on the aircraft                                 [dimensionless]
            engine_W_factor - weight increase factor for entire integrated propulsion system [dimensionless]
    
    Outputs:
            weight - weight of the full propulsion system                                     [kilograms]
        
    Properties Used:
            N/A
    """   
    
    weight = jet_engine_weight * engine_W_factor
    
    return weight
    