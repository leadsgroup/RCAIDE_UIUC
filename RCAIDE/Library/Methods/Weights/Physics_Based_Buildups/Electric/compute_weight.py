## @ingroup Methods-Weights-Buildups-eVTOL 
# RCAIDE/Methods/Weights/Buildups/eVTOL/compute_weight.py
# 
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE
import RCAIDE
from RCAIDE.Framework.Core                                            import Units, Data 
from RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Common   import compute_fuselage_weight
from RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Common   import compute_boom_weight
from RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Common   import compute_rotor_weight
from RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Common   import compute_wiring_weight
from RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Common   import compute_wing_weight

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Compute evtol weight
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Weights-Buildups-eVTOL 
def compute_weight(config, 
          contingency_factor            = 1.1,
          speed_of_sound                = 340.294,
          max_tip_mach                  = 0.65,
          disk_area_factor              = 1.15,
          safety_factor                 = 1.5,
          max_thrust_to_weight_ratio    = 1.1,
          max_g_load                    = 3.8,
          motor_efficiency              = 0.85 * 0.98):

    """ Calculates the empty vehicle mass for an EVTOL-type aircraft including seats,
        avionics, servomotors, ballistic recovery system, rotor and hub assembly,
        transmission, and landing gear. 
        
        Sources:
        Project Vahana Conceptual Trade Study
        https://github.com/VahanaOpenSource


        Inputs: 
            config:                     RCAIDE Config Data Stucture
            contingency_factor          Factor capturing uncertainty in vehicle weight [Unitless]
            speed_of_sound:             Local Speed of Sound                           [m/s]
            max_tip_mach:               Allowable Tip Mach Number                      [Unitless]
            disk_area_factor:           Inverse of Disk Area Efficiency                [Unitless]
            max_thrust_to_weight_ratio: Allowable Thrust to Weight Ratio               [Unitless]
            safety_factor               Safety Factor in vehicle design                [Unitless]
            max_g_load                  Maximum g-forces load for certification        [UNitless]
            motor_efficiency:           Motor Efficiency                               [Unitless]

        Outputs: 
            outputs:                    Data Dictionary of Component Masses [kg]

        Output data dictionary has the following book-keeping hierarchical structure:

            Output
                Total.
                    Empty.
                        Structural.
                            Fuselage
                            Wings
                            Landing Gear
                            Rotors
                            Hubs
                        Seats
                        Battery
                        Motors
                        Servo
                    Systems.
                        Avionics
                        ECS               - Environmental Control System
                        BRS               - Ballistic Recovery System
                        Wiring            - Aircraft Electronic Wiring
                    Payload

    """

    # Set up data structures for RCAIDE weight methods
    weight                   = Data()  
    weight.battery           = 0.0
    weight.payload           = 0.0
    weight.servos            = 0.0
    weight.hubs              = 0.0
    weight.booms             = 0.0
    weight.BRS               = 0.0  
    weight.motors            = 0.0
    weight.rotors            = 0.0
    weight.rotors            = 0.0
    weight.fuselage          = 0.0
    weight.wiring            = 0.0
    weight.wings             = Data()
    weight.wings_total       = 0.0

    config.payload.passengers                      = RCAIDE.Library.Components.Component()
    config.payload.baggage                         = RCAIDE.Library.Components.Component()
    config.payload.cargo                           = RCAIDE.Library.Components.Component()
    control_systems                                = RCAIDE.Library.Components.Component()
    electrical_systems                             = RCAIDE.Library.Components.Component()
    furnishings                                    = RCAIDE.Library.Components.Component()
    air_conditioner                                = RCAIDE.Library.Components.Component()
    fuel                                           = RCAIDE.Library.Components.Component()
    apu                                            = RCAIDE.Library.Components.Component()
    hydraulics                                     = RCAIDE.Library.Components.Component()
    avionics                                       = RCAIDE.Library.Components.Systems.Avionics()
    optionals                                      = RCAIDE.Library.Components.Component()

    # assign components to vehicle
    config.systems.control_systems                 = control_systems
    config.systems.electrical_systems              = electrical_systems
    config.systems.avionics                        = avionics
    config.systems.furnishings                     = furnishings
    config.systems.air_conditioner                 = air_conditioner
    config.systems.fuel                            = fuel
    config.systems.apu                             = apu
    config.systems.hydraulics                      = hydraulics
    config.systems.optionals                       = optionals


    #-------------------------------------------------------------------------------
    # Fixed Weights
    #-------------------------------------------------------------------------------
    MTOW                = config.mass_properties.max_takeoff
    maxSpan             = config.wings["main_wing"].spans.projected  
    weight.seats        = config.passengers * 15.   * Units.kg
    weight.passengers   = config.passengers * 70.   * Units.kg
    weight.avionics     = 15.                       * Units.kg
    weight.landing_gear = MTOW * 0.02               * Units.kg
    weight.ECS          = config.passengers * 7.    * Units.kg

    # Inputs and other constants
    tipMach        = max_tip_mach
    k              = disk_area_factor
    ToverW         = max_thrust_to_weight_ratio
    eta            = motor_efficiency
    rho_ref        = 1.225
    maxVTip        = speed_of_sound * tipMach         # Prop Tip Velocity
    maxLift        = MTOW * ToverW * 9.81             # Maximum Thrust
    AvgBladeCD     = 0.012                            # Average Blade CD

    
    # Determine length scale 
    length_scale = 1. 
 
    if len(config.fuselages) == 0.:
        for w  in config.wings:
            if isinstance(w ,RCAIDE.Library.Components.Wings.Main_Wing):
                b = w.chords.root
                if b>length_scale:
                    length_scale = b
                    nose_length  = 0.25*b
    else:
        for fuse in config.fuselages:
            nose   = fuse.lengths.nose
            length = fuse.lengths.total
            if length > length_scale:
                length_scale = length
                nose_length  = nose
     
                            
    #-------------------------------------------------------------------------------
    # Environmental Control System
    #-------------------------------------------------------------------------------
    config.systems.air_conditioner.origin[0][0]          = 0.51 * length_scale
    config.systems.air_conditioner.mass_properties.mass  = weight.ECS

    #-------------------------------------------------------------------------------
    # Network Weight
    #-------------------------------------------------------------------------------
    for network in config.networks:

        if not isinstance(network, RCAIDE.Framework.Networks.All_Electric_Network):
            raise NotImplementedError("""eVTOL weight buildup only supports the Battery Electric Rotor energy network.\n
            Weight buildup will not return information on propulsion system.""",RuntimeWarning)
                
        for bus in network.busses: 
    
            
            #------------------------------------------------------------------------------- 
            # Payload Weight
            #-------------------------------------------------------------------------------
            if bus.payload.origin[0][0] == 0:
                bus.payload.origin[0][0]                              = 0.5 * length_scale
            weight.payload                                            += bus.payload.mass_properties.mass * Units.kg
     
            #-------------------------------------------------------------------------------
            # Avionics Weight
            #-------------------------------------------------------------------------------
            if bus.avionics.origin[0][0] == 0:
                bus.avionics.origin[0][0]                          = 0.4 * nose_length
            bus.avionics.mass_properties.center_of_gravity[0][0]   = 0.0
            weight.avionics                                        += bus.avionics.mass_properties.mass      
 
                        
            for battery in bus.batteries: 
                weight.battery                                            += battery.mass_properties.mass * Units.kg 
        
            # Servo, Hub and BRS Weights
            lift_rotor_hub_weight   = 4.   * Units.kg
            prop_hub_weight         = MTOW * 0.04  * Units.kg
            lift_rotor_BRS_weight   = 16.  * Units.kg
    
            # Rotor Weight
            number_of_propellers    = 0.0  
            number_of_lift_rotors   = 0.0   
            total_number_of_rotors  = 0.0      
            lift_rotor_servo_weight = 0.0  
            
            for propulsor in bus.propulsors: 
                # Rotor 
                rotor = propulsor.rotor   
                if type(rotor) == RCAIDE.Library.Components.Propulsors.Converters.Propeller:
                    ''' Propeller Weight '''  
                    number_of_propellers       += 1   
                    rTip_ref                   = rotor.tip_radius
                    bladeSol_ref               = rotor.blade_solidity 
                    prop_servo_weight          = 5.2 * Units.kg  
                    propeller_mass             = compute_rotor_weight(rotor, maxLift/5.) * Units.kg
                    weight.rotors              += propeller_mass 
                    rotor.mass_properties.mass =  propeller_mass + prop_hub_weight + prop_servo_weight
                    weight.servos              += prop_servo_weight
                    weight.hubs                += prop_hub_weight
                    
                if (type(rotor) == RCAIDE.Library.Components.Propulsors.Converters.Lift_Rotor or type(rotor) == RCAIDE.Library.Components.Propulsors.Converters.Prop_Rotor) or type(rotor) == RCAIDE.Library.Components.Propulsors.Converters.Rotor:
                    ''' Lift Rotor, Prop-Rotor or Rotor Weight '''  
                    number_of_lift_rotors       += 1  
                    rTip_ref                    = rotor.tip_radius
                    bladeSol_ref                = rotor.blade_solidity 
                    lift_rotor_servo_weight     = 0.65 * Units.kg 
                    if rotor.oei.design_thrust == None:
                        design_thrust = rotor.hover.design_thrust
                    else:
                        design_thrust =rotor.oei.design_thrust
                    lift_rotor_mass             = compute_rotor_weight(rotor,design_thrust)
                    weight.rotors               += lift_rotor_mass 
                    rotor.mass_properties.mass  =  lift_rotor_mass + lift_rotor_hub_weight + lift_rotor_servo_weight
                    weight.servos               += lift_rotor_servo_weight
                    weight.hubs                 += lift_rotor_hub_weight 
                
                # Motor 
                motor = propulsor.rotor                            
                weight.motors              += motor.mass_properties.mass  
               
        total_number_of_rotors  = int(number_of_lift_rotors + number_of_propellers)  
        if total_number_of_rotors > 1:
            prop_BRS_weight     = 16.   * Units.kg
        else:
            prop_BRS_weight     = 0.   * Units.kg
 
        # Add associated weights  
        weight.BRS    += (prop_BRS_weight + lift_rotor_BRS_weight)  
        maxLiftPower   = 1.15*maxLift*(k*np.sqrt(maxLift/(2*rho_ref*np.pi*rTip_ref**2)) +
                                           bladeSol_ref*AvgBladeCD/8*maxVTip**3/(maxLift/(rho_ref*np.pi*rTip_ref**2)))
        # Tail Rotor
        if number_of_lift_rotors == 1: # this assumes that the vehicle is an electric helicopter with a tail rotor
            
            maxLiftOmega   = maxVTip/rTip_ref
            maxLiftTorque  = maxLiftPower / maxLiftOmega 
    
            for bus in network.busses: 
                tailrotor = next(iter(bus.lift_rotors))
                weight.tail_rotor  = compute_rotor_weight(tailrotor, 1.5*maxLiftTorque/(1.25*rTip_ref))*0.2 * Units.kg
                weight.rotors     += weight.tail_rotor 

    #-------------------------------------------------------------------------------
    # Wing and Motor Wiring Weight
    #-------------------------------------------------------------------------------  
    for w in config.wings:
        if w.symbolic:
            wing_weight = 0
        else:
            wing_weight            = compute_wing_weight(w, config, maxLift/5, safety_factor= safety_factor, max_g_load =  max_g_load )
            wing_tag               = w.tag
            weight.wings[wing_tag] = wing_weight
            w.mass_properties.mass = wing_weight 
        weight.wings_total         += wing_weight

        # compute_wiring_weight weight
        weight.wiring  += compute_wiring_weight(w, config, maxLiftPower/(eta*total_number_of_rotors)) * Units.kg 

    #-------------------------------------------------------------------------------
    # Landing Gear Weight
    #-------------------------------------------------------------------------------
    if not hasattr(config.landing_gear, 'nose'):
        config.landing_gear.nose       = RCAIDE.Library.Components.Landing_Gear.Nose_Landing_Gear()
    config.landing_gear.nose.mass      = 0.0
    if not hasattr(config.landing_gear, 'main'):
        config.landing_gear.main       = RCAIDE.Library.Components.Landing_Gear.Main_Landing_Gear()
    config.landing_gear.main.mass      = weight.landing_gear

    #-------------------------------------------------------------------------------
    # Fuselage  Weight  
    #-------------------------------------------------------------------------------
    for fuse in  config.fuselages: 
        fuselage_weight = compute_fuselage_weight(fuse, maxSpan, MTOW )  
        fuse.mass_properties.center_of_gravity[0][0] = .45*fuse.lengths.total
        fuse.mass_properties.mass                    =  fuselage_weight + weight.passengers + weight.seats +\
                                                                             weight.wiring + weight.BRS
        weight.fuselage += fuselage_weight  

    #-------------------------------------------------------------------------------
    # Boom Weight
    #-------------------------------------------------------------------------------
    for b in config.booms:
        boom_weight                                = compute_boom_weight(b) * Units.kg
        weight.booms                               += boom_weight 
        b.mass_properties.mass                     =  boom_weight 
    
    #-------------------------------------------------------------------------------
    # Pack Up Outputs
    #-------------------------------------------------------------------------------
    weight.structural = (weight.rotors + weight.hubs + weight.booms + weight.fuselage + weight.landing_gear +weight.wings_total)*Units.kg

    weight.empty      = (contingency_factor * (weight.structural + weight.seats + weight.avionics +weight.ECS +\
                        weight.motors + weight.servos + weight.wiring + weight.BRS) + weight.battery) *Units.kg

    weight.total      = weight.empty + weight.payload + weight.passengers

    return weight
