# RCAIDE/Library/Methods/Weights/Correlation_Buildups/General_Aviation/compute_payload_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core import  Units ,  Data 

# ----------------------------------------------------------------------------------------------------------------------
# Payload Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_payload_weight(TOW, empty, num_pax, W_cargo, W_passenger = 225.*Units.lbs,W_baggage = 0.):
    """ 
        Calculate the weight of the payload and the resulting fuel mass
 
        Inputs:
            TOW -                                                    [kilograms]
            W_empty - Operating empty weight of the aircraft        [kilograms]
            num_pax - number of passengers on the aircraft           [dimensionless]
            W_cargo - weight of cargo being carried on the aircraft [kilogram]
            W_passenger - weight of each passenger on the aircraft  [kilograms]
            W_baggage - weight of the baggage for each passenger    [kilograms]
            
            
        Outputs:
            output - a data dictionary with fields:
                payload - weight of the passengers plus baggage and paid cargo [kilograms]
                pax - weight of all the passengers                             [kilograms]
                bag - weight of all the baggage                                [kilograms]
                fuel - weight of the fuel carried                              [kilograms]
                empty - operating empty weight of the aircraft                 [kilograms]

    """     

    # process
    W_pax     = W_passenger * num_pax 
    W_bag     = W_baggage * num_pax
    W_payload = W_pax + W_bag + W_cargo

    # packup outputs
    output = Data()
    output.total        = W_payload
    output.passengers   = W_pax
    output.baggage      = W_bag
    output.cargo        = W_cargo

    return output