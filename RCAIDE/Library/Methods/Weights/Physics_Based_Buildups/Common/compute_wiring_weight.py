# RCAIDE/Library/Methods/Weights/Buildups/Common/compute_boom_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Compute wiring weight
# ----------------------------------------------------------------------------------------------------------------------
def compute_wiring_weight(wing, config, cablePower):
    """
    Calculates the mass of electrical wiring in an aircraft, including power cables and communication/sensor wiring.

    Parameters
    ----------
    wing : RCAIDE.Components.Wings.Wing()
        Wing data structure containing
            - spans.projected : float
                Wing span [m]
    config : RCAIDE.Vehicle()
        Vehicle configuration containing
            - networks : list
                List of propulsion networks
                    - propulsors : list
                        List of propulsors
                            - motor : Motor()
                                Motor data structure
                                    - origin : array
                                        Motor location [x,y,z]
                            - wing_mounted : bool
                                Indicates if propulsor is wing-mounted
            - fuselages : list
                List of fuselage components
                    - lengths.total : float
                        Fuselage length [m]
    cablePower : float
        Maximum power carried by cables [W]

    Returns
    -------
    weight : float
        Total wiring mass [kg]

    Notes
    -----
    The function calculates wiring mass based on cable length, power requirements,
    and additional sensor/communication wiring needs.

    **Major Assumptions**
        * Power cables run from motor locations to a central point
        * Cable density is 5.7e-6 kg/(W*m)
        * Communication wires have 6 wires per bundle
        * Communication wire density is 460e-5 kg/m
        * Communication wiring length includes:
            - Power cable routing paths
            - 10x fuselage length
            - 4x wing span

    **Theory**
    Mass calculations:
    .. math::
        m_{cables} = \\rho_{cable} * P * L_{cable}

        m_{comm} = \\rho_{wire} * N_{wires} * L_{wire}

    where:
        - :math:`\\rho_{cable}` = power cable density
        - :math:`P` = cable power
        - :math:`L_{cable}` = cable length
        - :math:`\\rho_{wire}` = communication wire density
        - :math:`N_{wires}` = number of wires per bundle
        - :math:`L_{wire}` = total wire length

    References
    ----------
    [1] Project Vahana Conceptual Trade Study
    """
    weight      = 0.0 
    cableLength = 0.0
    for network in config.networks:
        for propulsor in network.propulsors:
            motor = propulsor.motor
            if propulsor.wing_mounted == True:  
                MSL             = np.array(motor.origin) #- np.array(bus.origin)  WHAT DO WE DO HERE SINCE WE DONT HAVE A BUS DEFINED YET AT THIS STAGE
                cableLength     += np.sum(abs(MSL))  
                    
    cableDensity    = 5.7e-6
    massCables      = cableDensity * cablePower * cableLength
     
    # Determine mass of sensor/communication wires
    
    fLength = 0
    for fus in config.fuselages:
        fLength  += fus.lengths.total 
    
    wiresPerBundle  = 6
    wireDensity     = 460e-5
    wireLength      = cableLength + (10 * fLength) +  4*wing.spans.projected
    massWires       = wireDensity * wiresPerBundle * wireLength
     
    # Sum Total 
    weight += massCables + massWires
    
    return weight