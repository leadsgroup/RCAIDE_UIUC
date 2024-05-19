## @ingroup Methods-Weights-Buildups-Common 
# RCAIDE/Methods/Weights/Buildups/Common/compute_boom_weight.py
# 
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Compute wiring weight
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Weights-Buildups-Common 
def compute_wiring_weight(wing, config, cablePower):
    """ Calculates mass of wiring required for a wing, including DC power
        cables and communication cables, assuming power cables run an average of
        half the fuselage length and height in addition to reaching the motor
        location on the wingspan, and that communication and sesor  wires run an
        additional length based on the fuselage and wing dimensions. 
        
        Sources:
        Project Vahana Conceptual Trade Study

        Inputs:

            config                      RCAIDE Config Data Structure 
            max_power_draw              Maximum DC Power Draw           [W]

        Outputs:

            weight:                     Wiring Mass                     [kg]

    """
    weight      = 0.0 
    cableLength = 0.0
    for network in config.networks:
        for bus in network.busses: 
            for propulsor in bus.propulsors:
                motor = propulsor.motor
                if motor.wing_mounted == True: 
                    if motor.wing_tag == wing.tag: 
                        MSL             = np.array(motor.origin)  
                        cableLength     += np.sum(abs(MSL)) 
                    else:
                        cableLength     += 0
                        
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