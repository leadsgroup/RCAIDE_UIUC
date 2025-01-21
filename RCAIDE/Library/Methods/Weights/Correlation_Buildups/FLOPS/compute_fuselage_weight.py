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
    """
    Computes the fuselage weight using NASA FLOPS weight estimation method. Accounts for 
    aircraft type.

    Parameters
    ----------
    vehicle : Vehicle
        The vehicle instance containing:
            - networks : list
                Propulsion system data for engine count and mounting
            - fuselages['fuselage'] : Fuselage
                Primary fuselage with:
                    - lengths.total : float
                        Total fuselage length [m]
                    - width : float
                        Maximum fuselage width [m]
                    - heights.maximum : float
                        Maximum fuselage height [m]
            - flight_envelope.ultimate_load : float
                Ultimate load factor (default: 3.75)
            - systems.accessories : str
                Aircraft type ('short-range', 'commuter', 'medium-range', 
                'long-range', 'sst', 'cargo')
            - mass_properties.max_takeoff : float
                Maximum takeoff weight [kg]
            - design_mach_number : float
                Design cruise Mach number

    Returns
    -------
    WFUSE : float
        Fuselage structural weight [kg]

    Notes
    -----
    Uses FLOPS correlations developed from transport aircraft database, with 
    adjustments for different aircraft types. For more details, please refer to the 
    FLOPS documentation: https://ntrs.nasa.gov/citations/20170005851  

    **Major Assumptions**
        * Single fuselage configuration (NFUSE = 1)
        * Fuselage is tagged as 'fuselage'
    
    **Theory**
    For short-range/commuter aircraft:
    .. math::
        W_{fuse} = 0.052 S_{wet}^{1.086}(ULF \\cdot TOGW)^{0.177}q_{c}^{0.241}

    For other aircraft types:
    .. math::
        W_{fuse} = 1.35(L_{f}D_{eq})^{1.28}(1 + 0.05N_{ef})(1 + 0.38F_{cargo})

    where:
        * S_wet = fuselage wetted area
        * ULF = ultimate load factor
        * TOGW = takeoff gross weight
        * q_c = cruise dynamic pressure
        * L_f = fuselage length
        * D_eq = equivalent diameter
        * N_ef = number of fuselage-mounted engines
        * F_cargo = cargo aircraft flag

    References
    ----------
    [1] NASA Flight Optimization System (FLOPS)

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.FLOPS.compute_operating_empty_weight
    """
    
    L =  0
    for fuselage in vehicle.fuselages:
        if L < fuselage.lengths.total: 
            total_length = fuselage.lengths.total
            width        = fuselage.width
            max_height   = fuselage.heights.maximum
    
    XL  = total_length / Units.ft  # Fuselage length, ft
    DAV = (width + max_height) / 2. * 1 / Units.ft
    if vehicle.systems.accessories == "short-range" or vehicle.systems.accessories == "commuter":
        SWFUS           = np.pi * (XL / DAV - 1.7) * DAV ** 2  # Fuselage wetted area, ft**2
        ULF             = vehicle.flight_envelope.ultimate_load  # Ultimate load factor
        atmosphere      = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
        atmo_data       = atmosphere.compute_values(vehicle.flight_envelope.design_cruise_altitude, 0)
        atmo_data_floor = atmosphere.compute_values(0, 0)
        DELTA           = atmo_data.pressure/atmo_data_floor.pressure
        QCRUS           = 1481.35 * DELTA * vehicle.flight_envelope.design_mach_number**2  # Cruise dynamic pressure, psf
        DG              = vehicle.mass_properties.max_takeoff / Units.lbs  # Design gross weight in lb
        WFUSE           = 0.052 * SWFUS ** 1.086 * (ULF * DG) ** 0.177 * QCRUS ** 0.241
    else: 
        NENG = 0
        FNEW = 0
        FNEF = 0 
        for network in  vehicle.networks:
            for propulsor in network.propulsors:
                if isinstance(propulsor, RCAIDE.Library.Components.Propulsors.Turbofan) or  isinstance(propulsor, RCAIDE.Library.Components.Propulsors.Turbojet):
                    NENG += 1 
                    FNEF += 1
                    if propulsor.wing_mounted: 
                        FNEW += 1  
        if vehicle.systems.accessories == 'cargo':
            CARGF = 1
        else:
            CARGF = 0  # Cargo aircraft floor factor [0 for passenger transport, 1 for cargo transport
        NFUSE = 1  # Number of fuselages
        WFUSE = 1.35 * (XL * DAV) ** 1.28 * (1 + 0.05 * FNEF) * (1 + 0.38 * CARGF) * NFUSE
    return WFUSE * Units.lbs
