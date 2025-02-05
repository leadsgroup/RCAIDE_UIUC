# RCAIDE/Library/Methods/Weights/Correlation_Buildups/FLOPS/compute_fuselage_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE
import RCAIDE 
from RCAIDE.Framework.Core    import Units

# python imports 
import  numpy as  np
 
# ----------------------------------------------------------------------------------------------------------------------
# Fuselage Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_fuselage_weight(vehicle):
    """ Calculate the weight of the fuselage of a transport aircraft

        Assumptions:
            NFUSE = 1, only one fuselage (it's possible to modify this in future work)
            delta_isa = 0, for pressure calculations
            Fuselage is tagged as 'fuselage'

        Source:
            The Flight Optimization System Weight Estimation Method

        Inputs:
            vehicle - data dictionary with vehicle properties                    [dimensionless]
                -.networks: data dictionary containing all propulsion properties
                -.fuselages['fuselage'].lengths.total: fuselage total length      [meters]
                -.fuselages['fuselage'].width: fuselage width                    [meters]
                -.fuselages['fuselage'].heights.maximum: fuselage maximum height [meters]
                -.flight_envelope.ultimate_load: ultimate load factor (default: 3.75)
                -.systems.accessories: type of aircraft (short-range, commuter
                                                        medium-range, long-range,
                                                        sst, cargo)
                -.mass_properties.max_takeoff: MTOW                              [kilograms]
                -.design_mach_number: design mach number for cruise flight

        Outputs:
            WFUSE - weight of the fuselage                                      [kilograms]

        Properties Used:
            N/A
    """
    
    L =  0
    for fuselage in vehicle.fuselages:
        if L < fuselage.lengths.total: 
            total_length = fuselage.lengths.total
            width        = fuselage.width
            max_height   = fuselage.heights.maximum
    
    XL  = total_length / Units.ft  # Fuselage length, ft
    DAV = (width + max_height) / 2. * 1 / Units.ft
    
    DG       = vehicle.mass_properties.max_takeoff / Units.lbs  # Design gross weight in lb
    QCRUS    = vehicle.design_dynamic_pressure / Units.psf
    ULF      = vehicle.flight_envelope.ultimate_load  
    SWFUS    = 3.14159*(XL/DAV -1.7)*(DAV**2)

    WFUSE = 0.052 * SWFUS**1.086 * (ULF*DG)**0.177 * QCRUS**0.241 
    
    return WFUSE * Units.lbs