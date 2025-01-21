# RCAIDE/Library/Methods/Weights/Correlation_Buildups/FLOPS/ccompute_propulsion_system_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE
import  RCAIDE 
from RCAIDE.Framework.Core    import Units ,  Data

# python imports 
import  numpy as  np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Propulsion Systems Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_propulsion_system_weight(vehicle, ref_propulsor):
    """
    Computes the complete propulsion system weight using NASA FLOPS weight estimation 
    method. Includes engines, nacelles, thrust reversers, and associated systems.

    Parameters
    ----------
    vehicle : Vehicle
        The vehicle instance containing:
            - networks : list
                Propulsion systems with:
                    - propulsors : list
                        Engine data
                    - fuel_lines : list
                        Fuel system data with fuel tanks
            - design_mach_number : float
                Design cruise Mach number
            - mass_properties.max_zero_fuel : float
                Maximum zero fuel weight [kg]
            - systems.accessories : str
                Aircraft type ('short-range', 'commuter', 'medium-range', 
                'long-range', 'sst', 'cargo')
    ref_propulsor : Propulsor
        Reference engine containing:
            - sealevel_static_thrust : float
                Sea level static thrust [N]
            - nacelle : Nacelle
                Nacelle geometry with:
                    - diameter : float
                        Maximum diameter [m]
                    - length : float
                        Total length [m]

    Returns
    -------
    output : Data
        Container with propulsion weight breakdown:
            - W_prop : float
                Total propulsion system weight [kg]
            - W_engine : float
                Dry engine weight [kg]
            - W_thrust_reverser : float
                Thrust reverser weight [kg]
            - W_starter : float
                Starter system weight [kg]
            - W_engine_controls : float
                Engine controls weight [kg]
            - W_fuel_system : float
                Fuel system weight [kg]
            - W_nacelle : float
                Nacelle weight [kg]
            - number_of_engines : int
                Total engine count
            - number_of_fuel_tanks : int
                Total fuel tank count

    Notes
    -----
    Uses FLOPS correlations developed from transport aircraft database.

    **Major Assumptions**
        * Rated thrust per scaled engine equals baseline thrust
        * Engine weight scaling parameter is 1.15
        * Engine inlet weight scaling exponent is 1
        * Baseline inlet weight is 0 lbs
        * Baseline nozzle weight is 0 lbs
        * All nacelles are identical
        * Number of nacelles equals number of engines

    **Theory**
    Engine weight is computed using:
    .. math::
        W_{eng} = W_{base}(T/T_{base})^{1.15}

    Nacelle weight is computed using:
    .. math::
        W_{nac} = 0.25N_{nac}D_{nac}L_{nac}T^{0.36}

    Thrust reverser weight is computed using:
    .. math::
        W_{rev} = 0.034T N_{nac}

    where:
        * W_base = baseline engine weight
        * T = sea level static thrust
        * N_nac = number of nacelles
        * D_nac = nacelle diameter
        * L_nac = nacelle length

    References
    ----------
    [1] NASA Flight Optimization System (FLOPS)
    """
     
    NENG =  0 
    number_of_tanks =  0
    for network in  vehicle.networks:
        for propulsor in network.propulsors:
            if isinstance(propulsor, RCAIDE.Library.Components.Propulsors.Turbofan) or  isinstance(propulsor, RCAIDE.Library.Components.Propulsors.Turbojet):
                ref_propulsor = propulsor  
                NENG  += 1 
            if 'nacelle' in propulsor:
                ref_nacelle =  propulsor.nacelle   
        for fuel_line in network.fuel_lines:
            for fuel_tank in fuel_line.fuel_tanks:
                number_of_tanks +=  1
                  
     
    WNAC            = nacelle_FLOPS(ref_propulsor,ref_nacelle,NENG ) 
    WFSYS           = fuel_system_FLOPS(vehicle, NENG)
    WENG            = compute_engine_weight(vehicle,ref_propulsor)
    WEC, WSTART     = misc_engine_FLOPS(vehicle,ref_propulsor,ref_nacelle,NENG)
    WTHR            = thrust_reverser_FLOPS(ref_propulsor,NENG)
    WPRO            = NENG * WENG + WFSYS + WEC + WSTART + WTHR + WNAC

    output                      = Data()
    output.W_prop               = WPRO
    output.W_thrust_reverser    = WTHR
    output.W_starter            = WSTART
    output.W_engine_controls    = WEC
    output.W_fuel_system        = WFSYS
    output.W_nacelle            = WNAC
    output.W_engine             = WENG * NENG
    output.number_of_engines    = NENG 
    output.number_of_fuel_tanks = number_of_tanks  
    return output


def nacelle_FLOPS(ref_propulsor, ref_nacelle, NENG):
    """
    Calculates the nacelle weight based on the FLOPS method.

    Parameters
    ----------
    ref_propulsor : Propulsor
        Reference engine containing:
            - sealevel_static_thrust : float
                Sea level static thrust [N]
    ref_nacelle : Nacelle
        Nacelle geometry with:
            - diameter : float
                Maximum diameter [m]
            - length : float
                Total length [m]
    NENG : int
        Number of engines

    Returns
    -------
    WNAC : float
        Total nacelle weight [kg]

    Notes
    -----
    **Major Assumptions**
        * All nacelles are identical
        * Number of nacelles equals number of engines

    **Theory**
    Weight is computed using:
    .. math::
        W_{nac} = 0.25N_{nac}D_{nac}L_{nac}T^{0.36}

    where:
        * N_nac = number of nacelles
        * D_nac = nacelle diameter
        * L_nac = nacelle length
        * T = sea level static thrust

    References
    ----------
    [1] Raymer, D.P. Aircraft Design: A Conceptual Approach, AIAA Education Series, 2012
    """
    TNAC   = NENG + 1. / 2 * (NENG - 2 * np.floor(NENG / 2.))
    DNAC   = ref_nacelle.diameter / Units.ft
    XNAC   = ref_nacelle.length / Units.ft
    FTHRST = ref_propulsor.sealevel_static_thrust * 1 / Units.lbf
    WNAC   = 0.25 * TNAC * DNAC * XNAC * FTHRST ** 0.36
    return WNAC * Units.lbs


def thrust_reverser_FLOPS(ref_propulsor, NENG):
    """
    Calculates the weight of the thrust reversers.

    Parameters
    ----------
    ref_propulsor : Propulsor
        Reference engine containing:
            - sealevel_static_thrust : float
                Sea level static thrust [N]
    NENG : int
        Number of engines

    Returns
    -------
    WTHR : float
        Total thrust reverser weight [kg]

    Notes
    -----
    **Theory**
    Weight is computed using:
    .. math::
        W_{rev} = 0.034T N_{nac}

    where:
        * T = sea level static thrust
        * N_nac = number of nacelles

    References
    ----------
    [1] NASA Flight Optimization System (FLOPS)
    """
    TNAC = NENG + 1. / 2 * (NENG - 2 * np.floor(NENG / 2.))
    THRUST = ref_propulsor.sealevel_static_thrust * 1 / Units.lbf
    WTHR = 0.034 * THRUST * TNAC
    return WTHR * Units.lbs


def misc_engine_FLOPS(vehicle, ref_propulsor, ref_nacelle, NENG):
    """
    Calculates miscellaneous engine weights including electrical control system 
    and starter engine weights.

    Parameters
    ----------
    vehicle : Vehicle
        The vehicle instance containing:
            - design_mach_number : float
                Design cruise Mach number
    ref_propulsor : Propulsor
        Reference engine containing:
            - sealevel_static_thrust : float
                Sea level static thrust [N]
    ref_nacelle : Nacelle
        Nacelle geometry with:
            - diameter : float
                Maximum diameter [m]
    NENG : int
        Number of engines

    Returns
    -------
    WEC : float
        Electrical engine control system weight [kg]
    WSTART : float
        Starter engine weight [kg]

    Notes
    -----
    **Theory**
    Weights are computed using:
    .. math::
        W_{EC} = 0.26N_{eng}T^{0.5}
        W_{start} = 11.0N_{eng}V_{max}^{0.32}D_{nac}^{1.6}

    where:
        * N_eng = number of engines
        * T = sea level static thrust
        * V_max = design Mach number
        * D_nac = nacelle diameter
    
    References
    ----------
    [1] NASA Flight Optimization System (FLOPS)
    """
    THRUST  = ref_propulsor.sealevel_static_thrust * 1 / Units.lbf
    WEC     = 0.26 * NENG * THRUST ** 0.5
    FNAC    = ref_nacelle.diameter / Units.ft
    VMAX    = vehicle.flight_envelope.design_mach_number
    WSTART  = 11.0 * NENG * VMAX ** 0.32 * FNAC ** 1.6
    return WEC * Units.lbs, WSTART * Units.lbs


def fuel_system_FLOPS(vehicle, NENG):
    """
    Calculates the weight of the fuel system.

    Parameters
    ----------
    vehicle : Vehicle
        The vehicle instance containing:
            - design_mach_number : float
                Design cruise Mach number
            - mass_properties.max_zero_fuel : float
                Maximum zero fuel weight [kg]
    NENG : int
        Number of engines

    Returns
    -------
    WFSYS : float
        Fuel system weight [kg]

    Notes
    -----
    **Theory**
    Weight is computed using:
    .. math::
        W_{fsys} = 1.07W_{ZF}^{0.58}N_{eng}^{0.43}M^{0.34}

    where:
        * W_ZF = zero fuel weight
        * N_eng = number of engines
        * M = design Mach number
    
    References
    ----------
    [1] NASA Flight Optimization System (FLOPS)
    """
    VMAX = vehicle.flight_envelope.design_mach_number
    FMXTOT = vehicle.mass_properties.max_zero_fuel / Units.lbs
    WFSYS = 1.07 * FMXTOT ** 0.58 * NENG ** 0.43 * VMAX ** 0.34
    return WFSYS * Units.lbs


def compute_engine_weight(vehicle, ref_propulsor):
    """
    Calculates the dry engine weight based on the FLOPS method.

    Parameters
    ----------
    vehicle : Vehicle
        The vehicle instance containing:
            - systems.accessories : str
                Aircraft type ('short-range', 'commuter', etc.)
    ref_propulsor : Propulsor
        Reference engine containing:
            - sealevel_static_thrust : float
                Sea level static thrust [N]

    Returns
    -------
    WENG : float
        Dry engine weight [kg]

    Notes
    -----
    **Major Assumptions**
        * Rated thrust per scaled engine equals baseline thrust
        * Engine weight scaling parameter is 1.15
        * Engine inlet weight scaling exponent is 1
        * Baseline inlet weight is 0 lbs
        * Baseline nozzle weight is 0 lbs

    **Theory**
    Weight is computed using:
    .. math::
        W_{eng} = W_{base}(T/T_{base})^{1.15}

    where:
        * W_base = baseline engine weight
        * T = sea level static thrust
        * T_base = baseline thrust
    
    References
    ----------
    [1] NASA Flight Optimization System (FLOPS)
    """
    EEXP = 1.15
    EINL = 1
    ENOZ = 1
    THRSO = ref_propulsor.sealevel_static_thrust * 1 / Units.lbf
    THRUST = THRSO
    if vehicle.systems.accessories == "short-range" or vehicle.systems.accessories == "commuter":
        WENGB = THRSO / 10.5
    else:
        WENGB = THRSO / 5.5
    WINLB = 0 / Units.lbs
    WNOZB = 0 / Units.lbs
    WENGP = WENGB * (THRUST / THRSO) ** EEXP
    WINL = WINLB * (THRUST / THRSO) ** EINL
    WNOZ = WNOZB * (THRUST / THRSO) ** ENOZ
    WENG = WENGP + WINL + WNOZ
    return WENG * Units.lbs
