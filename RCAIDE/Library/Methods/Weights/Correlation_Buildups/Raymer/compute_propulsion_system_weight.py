# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Raymer/compute_propulsion_system_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
import  RCAIDE 
from RCAIDE.Framework.Core    import Units, Data
from RCAIDE.Library.Methods.Weights.Correlation_Buildups.FLOPS.compute_propulsion_system_weight import compute_engine_weight

# python imports 
import  numpy as  np
 
# ----------------------------------------------------------------------------------------------------------------------
# Propulsion System Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_propulsion_system_weight(vehicle, network):
    """
    Calculates the total propulsion system weight using Raymer's method, including subsystems.

    Parameters
    ----------
    vehicle : RCAIDE.Vehicle()
        Vehicle data structure containing:
            - networks : list
                List of propulsion networks
            - fuselages : list
                List of fuselage components
            - flight_envelope : Data()
                Contains design_mach_number
            - mass_properties : Data()
                Contains max_zero_fuel
    network : RCAIDE.Network()
        Network component containing:
            - fuel_lines : list
                List of fuel line components with fuel tanks
            - propulsors : list
                List of propulsion components

    Returns
    -------
    output : Data()
        Propulsion system weight breakdown:
            - W_prop : float
                Total propulsion system weight [kg]
            - W_thrust_reverser : float
                Thrust reverser weight [kg]
            - W_starter : float
                Starter engine weight [kg]
            - W_engine_controls : float
                Engine controls weight [kg]
            - W_fuel_system : float
                Fuel system weight [kg]
            - W_nacelle : float
                Nacelle weight [kg]
            - W_engine : float
                Total dry engine weight [kg]
            - number_of_engines : int
                Number of engines
            - number_of_fuel_tanks : int
                Number of fuel tanks

    Notes
    -----
    This method calculates the complete propulsion system weight including engines,
    nacelles, fuel system, and all supporting systems using Raymer's correlations.

    **Major Assumptions**
        * Correlations based on conventional turbofan/turbojet installations
        * Engine controls scale with number of engines and fuselage length
        * Nacelle weight includes thrust reversers if applicable
        * Fuel system weight scales with fuel capacity and number of tanks
        * Starter weight scales with total engine weight

    **Theory**
    Key component weights are calculated using:
    .. math::
        W_{nacelle} = 0.6724K_{ng}L_n^{0.1}W_n^{0.294}N_{ult}^{0.119}W_{ec}^{0.611}N_{eng}S_n^{0.224}

    .. math::
        W_{fuel\_sys} = 1.07W_{fuel}^{0.58}N_{eng}^{0.43}M_{max}^{0.34}

    References
    ----------
    [1] Raymer, D., "Aircraft Design: A Conceptual Approach", AIAA 
        Education Series, 2018. 

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.FLOPS.compute_jet_engine_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.FLOPS.compute_piston_engine_weight
    """

    NENG    =  0 
    number_of_tanks =  0
    for network in  vehicle.networks:
        for fuel_line in network.fuel_lines:
            for fuel_tank in fuel_line.fuel_tanks:
                number_of_tanks +=  1
            for propulsor in network.propulsors:
                if isinstance(propulsor, RCAIDE.Library.Components.Propulsors.Turbofan) or  isinstance(propulsor, RCAIDE.Library.Components.Propulsors.Turbojet):
                    ref_propulsor = propulsor  
                    NENG  += 1 
                if 'nacelle' in propulsor:
                    ref_nacelle =  propulsor.nacelle 
                    
    WFSYS           = compute_fuel_system_weight(vehicle, NENG)
    WENG            = compute_engine_weight(vehicle,ref_propulsor)
    WNAC            = compute_nacelle_weight(vehicle,ref_nacelle, NENG, WENG)
    WEC, WSTART     = compute_misc_engine_weight(vehicle,NENG, WENG)
    WTHR            = 0
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

def compute_nacelle_weight(vehicle, ref_nacelle, NENG, WENG):
    """
    Calculates the nacelle weight based on Raymer's empirical method.

    Parameters
    ----------
    vehicle : RCAIDE.Vehicle()
        Vehicle data structure containing:
            - flight_envelope.ultimate_load : float
                Ultimate load factor
    ref_nacelle : RCAIDE.Component()
        Nacelle component containing:
            - length : float
                Total length of nacelle [m]
            - diameter : float
                Maximum diameter of nacelle [m]
    NENG : int
        Number of engines
    WENG : float
        Dry engine weight [kg]

    Returns
    -------
    WNAC : float
        Total nacelle weight [kg]

    Notes
    -----
    **Major Assumptions**
        * All nacelles are identical
        * Number of nacelles equals number of engines
        * Engine not pylon mounted (Kng = 1)
        * Conventional nacelle construction

    **Theory**
    The nacelle weight is calculated using:
    .. math::
        W_{nac} = 0.6724K_{ng}L_n^{0.1}W_n^{0.294}N_{ult}^{0.119}W_{ec}^{0.611}N_{eng}S_n^{0.224}

    References
    ----------
    [1] Raymer, D., "Aircraft Design: A Conceptual Approach", AIAA 
        Education Series, 2018. 
    """
    Kng             = 1 # assuming the engine is not pylon mounted
    Nlt             = ref_nacelle.length / Units.ft
    Nw              = ref_nacelle.diameter / Units.ft
    Wec             = 2.331 * WENG ** 0.901 * 1.18
    Sn              = 2 * np.pi * Nw/2 * Nlt + np.pi * Nw**2/4 * 2
    WNAC            = 0.6724 * Kng * Nlt ** 0.1 * Nw ** 0.294 * vehicle.flight_envelope.ultimate_load ** 0.119 \
                      * Wec ** 0.611 * NENG * 0.984 * Sn ** 0.224
    return WNAC * Units.lbs

def compute_misc_engine_weight(vehicle, NENG, WENG):
    """
    Calculates miscellaneous engine weights including electrical controls and starter.

    Parameters
    ----------
    vehicle : RCAIDE.Vehicle()
        Vehicle data structure containing:
            - fuselages : list
                List of fuselage components with lengths.total
    NENG : int
        Number of engines
    WENG : float
        Dry engine weight [kg]

    Returns
    -------
    WEC : float
        Engine control system weight [kg]
    WSTART : float
        Starter system weight [kg]

    Notes
    -----
    **Theory**
    The weights are calculated using:
    .. math::
        W_{ec} = 5N_{eng} + 0.8L_{ec}

    .. math::
        W_{start} = 49.19(N_{eng}W_{eng}/1000)^{0.541}

    References
    ----------
    [1] Raymer, D., "Aircraft Design: A Conceptual Approach", AIAA 
        Education Series, 2018. 
    """

    L =  0 
    for fuselage in vehicle.fuselages:
        if L < fuselage.lengths.total: 
            total_length = fuselage.lengths.total             
    Lec     = NENG * total_length / Units.ft
    WEC     = 5 * NENG + 0.8 * Lec
    WSTART  = 49.19*(NENG*WENG/1000)**0.541
    return WEC * Units.lbs, WSTART * Units.lbs
 
def compute_fuel_system_weight(vehicle, NENG):
    """
    Calculates the weight of the fuel system based on Raymer's method.

    Parameters
    ----------
    vehicle : RCAIDE.Vehicle()
        Vehicle data structure containing:
            - flight_envelope.design_mach_number : float
                Design mach number
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
    The fuel system weight is calculated using:
    .. math::
        W_{fs} = 1.07W_{fuel}^{0.58}N_{eng}^{0.43}M_{max}^{0.34}

    References
    ----------
    [1] Raymer, D., "Aircraft Design: A Conceptual Approach", AIAA 
        Education Series, 2018. 
    """
    VMAX    = vehicle.flight_envelope.design_mach_number
    FMXTOT  = vehicle.mass_properties.max_zero_fuel / Units.lbs
    WFSYS = 1.07 * FMXTOT ** 0.58 * NENG ** 0.43 * VMAX ** 0.34
    return WFSYS * Units.lbs