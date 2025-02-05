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
def compute_propulsion_system_weight(vehicle,ref_propulsor):
    """ Calculate the weight of propulsion system, including:
        - dry engine weight
        - fuel system weight
        - thurst reversers weight
        - electrical system weight
        - starter engine weight
        - nacelle weight
        - cargo containers

        Assumptions:
            1) Rated thrust per scaled engine and rated thurst for baseline are the same
            2) Engine weight scaling parameter is 1.15
            3) Enginge inlet weight scaling exponent is 1
            4) Baseline inlet weight is 0 lbs as in example files FLOPS
            5) Baseline nozzle weight is 0 lbs as in example files FLOPS

        Source:
            The Flight Optimization System Weight Estimation Method

        Inputs:
            vehicle - data dictionary with vehicle properties                   [dimensionless]
                -.design_mach_number: design mach number for cruise flight
                -.mass_properties.max_zero_fuel: zero fuel weight               [kg]
                -.systems.accessories: type of aircraft (short-range, commuter
                                                        medium-range, long-range,
                                                        sst, cargo)
            nacelle - data dictionary with propulsion system properties 
                -.diameter: diameter of nacelle                                 [meters]
                -.length: length of complete engine assembly                    [meters]
            ref_propulsor.
                -.sealevel_static_thrust: thrust at sea level                   [N]


        Outputs:
            output - data dictionary with weights                               [kilograms]
                    - output.W_prop: total propulsive system weight
                    - output.W_thrust_reverser: thurst reverser weight
                    - output.starter: starter engine weight
                    - output.W_engine_controls: engine controls weight
                    - output.fuel_system: fuel system weight
                    - output.nacelle: nacelle weight
                    - output.W_engine: dry engine weight

        Properties Used:
            N/A
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
            for _ in fuel_line.fuel_tanks:
                number_of_tanks +=  1
                  
     

    WFSYS           = compute_fuel_system_weight(vehicle, NENG)
    WENG            = compute_engine_weight(vehicle,ref_propulsor)
    WEC, WSTART     = compute_misc_propulsion_system_weight(vehicle,ref_propulsor,ref_nacelle,NENG)
    WPRO            = NENG * WENG + WFSYS + WEC + WSTART

    output                      = Data()
    output.W_prop               = WPRO
    output.W_starter            = WSTART
    output.W_engine_controls    = WEC
    output.W_fuel_system        = WFSYS
    output.W_engine             = WENG * NENG
    output.number_of_engines    = NENG 
    output.number_of_fuel_tanks = number_of_tanks  
    return output



def compute_misc_propulsion_system_weight(vehicle,ref_propulsor,ref_nacelle,NENG ):
    """ Calculates the miscellaneous engine weight based on the FLOPS method, electrical control system weight
        and starter engine weight
        
        Assumptions:
            1) All nacelles are identical
            2) The number of nacelles is the same as the number of engines 

        Source:
            The Flight Optimization System Weight Estimation Method

        Inputs:
            vehicle - data dictionary with vehicle properties                            [dimensionless]
                 -.design_mach_number: design mach number
            ref_propulsor    - data dictionary for the specific network that is being estimated [dimensionless]
                -.number_of_engines: number of engines
                -.sealevel_static_thrust: sealevel static thrust of engine               [N]
            nacelle              
                -.diameter: diameter of nacelle                                          [m]
              
        Outputs:              
            WEC: electrical engine control system weight                                 [kg]
            WSTART: starter engine weight                                                [kg]

        Properties Used:
            N/A
    """ 
    THRUST  = ref_propulsor.sealevel_static_thrust * 1 / Units.lbf
    WEC     = 0.26 * NENG * THRUST ** 0.5
    FNAC    = ref_nacelle.diameter / Units.ft
    VMAX    = vehicle.flight_envelope.design_mach_number
    WSTART  = 11.0 * NENG * VMAX ** 0.32 * FNAC ** 1.6
    return WEC * Units.lbs, WSTART * Units.lbs

 
def compute_fuel_system_weight(vehicle, NENG):
    """ Calculates the weight of the fuel system based on the FLOPS method
        Assumptions:

        Source:
            The Flight Optimization System Weight Estimation Method

        Inputs:
            vehicle - data dictionary with vehicle properties                   [dimensionless]

        Outputs:
            WFSYS: Fuel system weight                                       [kg]

        Properties Used:
            N/A
    """
    FMXTOT = vehicle.mass_properties.max_fuel / Units.lbs
    WFSYS = 1.07 * FMXTOT ** 0.58 * NENG ** 0.43 
    return WFSYS * Units.lbs


def compute_engine_weight(vehicle, ref_propulsor):
    """ Calculates the dry engine weight based on the FLOPS method
        Assumptions:
            Rated thrust per scaled engine and rated thurst for baseline are the same
            Engine weight scaling parameter is 1.15
            Enginge inlet weight scaling exponent is 1
            Baseline inlet weight is 0 lbs as in example files FLOPS
            Baseline nozzle weight is 0 lbs as in example files FLOPS

        Source:
            The Flight Optimization System Weight Estimation Method

        Inputs:
            vehicle - data dictionary with vehicle properties                   [dimensionless]
                -.systems.accessories: type of aircraft (short-range, commuter
                                                        medium-range, long-range,
                                                        sst, cargo)
            ref_propulsor    - data dictionary for the specific network that is being estimated [dimensionless]
                -.sealevel_static_thrust: sealevel static thrust of engine  [N]

        Outputs:
            WENG: dry engine weight                                         [kg]

        Properties Used:
            N/A
    """
    EEXP = 1.15
    EINL = 1
    ENOZ = 1
    THRSO = ref_propulsor.sealevel_static_thrust * 1 / Units.lbf
    THRUST = THRSO
    WENGB = THRSO / 10.5
    WINLB = 0 / Units.lbs
    WNOZB = 0 / Units.lbs
    WENGP = WENGB * (THRUST / THRSO) ** EEXP
    WINL = WINLB * (THRUST / THRSO) ** EINL
    WNOZ = WNOZB * (THRUST / THRSO) ** ENOZ
    WENG = WENGP + WINL + WNOZ
    return WENG * Units.lbs