# RCAIDE/Library/Methods/Weights/Correlation_Buildups/FLOPS/compute_horizontal_tail_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core    import Units
 
# ----------------------------------------------------------------------------------------------------------------------
#  Horizontal Tail Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_horizontal_tail_weight(vehicle, wing): 
    """ Calculate the horizontal tail weight

            N/A
        """
    SHT     = wing.areas.reference / Units.ft **2
    DG      = vehicle.mass_properties.max_takeoff / Units.lbs
    QCRUS    = vehicle.design_dynamic_pressure / Units.psf
    ULF      = vehicle.flight_envelope.ultimate_load   
    WHT     = 0.016*SHT**0.873 * ( ULF * DG)**0.414 * QCRUS**0.122 
    return WHT * Units.lbs
