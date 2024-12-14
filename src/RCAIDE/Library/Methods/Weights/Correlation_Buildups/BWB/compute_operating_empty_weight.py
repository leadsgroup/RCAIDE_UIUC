# RCAIDE/Library/Methods/Weights/Correlation_Buildups/BWB/operating_empty_weight.py
# 
# Created: Sep 2024, M. Clarke  

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ----------------------------------------------------------------------------------------------------------------------
import  RCAIDE
from RCAIDE.Framework.Core import Data 
from .compute_cabin_weight          import compute_cabin_weight
from .compute_aft_centerbody_weight import compute_aft_centerbody_weight
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Common     as Common
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Propulsion as Propulsion
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Transport  as Transport
from RCAIDE.Library.Attributes.Materials.Aluminum import Aluminum

# ---------------------------------------------------------------------------------------------------------------------- 
# Operating Empty Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_operating_empty_weight(vehicle,settings=None):
    """ This is for a BWB aircraft configuration.

    Assumptions:
         Calculated aircraft weight from correlations created per component of historical aircraft
         The wings are made out of aluminum.
         A wing with the tag 'main_wing' exists.

    Source:
        N/A

    Inputs:
        engine - a data dictionary with the fields:
            thrust_sls - sea level static thrust of a single engine                                        [Newtons]

        wing - a data dictionary with the fields:
            gross_area - wing gross area                                                                   [meters**2]
            span - span of the wing                                                                        [meters]
            taper - taper ratio of the wing                                                                [dimensionless]
            t_c - thickness-to-chord ratio of the wing                                                     [dimensionless]
            sweep - sweep angle of the wing                                                                [radians]
            mac - mean aerodynamic chord of the wing                                                       [meters]
            r_c - wing root chord                                                                          [meters]

        aircraft - a data dictionary with the fields:
            Nult - ultimate load of the aircraft                                                           [dimensionless]
            Nlim - limit load factor at zero fuel weight of the aircraft                                   [dimensionless]
            TOW - maximum takeoff weight of the aircraft                                                   [kilograms]
            zfw - maximum zero fuel weight of the aircraft                                                 [kilograms]
            num_eng - number of engines on the aircraft                                                    [dimensionless]
            num_pax - number of passengers on the aircraft                                                 [dimensionless]
            W_cargo - weight of the bulk cargo being carried on the aircraft                              [kilograms]
            num_seats - number of seats installed on the aircraft                                          [dimensionless]
            ctrl - specifies if the control system is "fully powered", "partially powered", or not powered [dimensionless]
            ac - determines type of instruments, electronics, and operating items based on types:
                "short-range", "medium-range", "long-range", "business", "cargo", "commuter", "sst"        [dimensionless]

         fuselage - a data dictionary with the fields:
            area - fuselage wetted area                                                                    [meters**2]
            diff_p - Maximum fuselage pressure differential                                                [Pascal]
            width - width of the fuselage                                                                  [meters]
            height - height of the fuselage                                                                [meters]
            length - length of the fuselage                                                                [meters]

    Outputs:
        output - a data dictionary with fields:
            W_payload - weight of the passengers plus baggage and paid cargo                              [kilograms]
            W_pax - weight of all the passengers                                                          [kilogram]
            W_bag - weight of all the baggage                                                             [kilogram]
            W_fuel - weight of the fuel carried                                                           [kilogram]
            W_empty - operating empty weight of the aircraft                                              [kilograms]

    Properties Used:
    N/A
    """

    # Unpack inputs
    if settings == None: 
        use_max_fuel_weight = True 
    else:
        use_max_fuel_weight = settings.use_max_fuel_weight
        
    TOW         = vehicle.mass_properties.max_takeoff
    
    for fuselage in vehicle.fuselages:
        if type(fuselage) ==  RCAIDE.Library.Components.Fuselages.Blended_Wing_Body_Fuselage: 
            bwb_aft_centerbody_area       = fuselage.aft_centerbody_area
            bwb_aft_centerbody_taper      = fuselage.aft_centerbody_taper 
            W_cabin                       = compute_cabin_weight(fuselage.cabin_area, TOW)
            fuselage.mass_properties.mass = W_cabin
        else:
            print('No BWB Fuselage is defined!') 
            bwb_aft_centerbody_area       = 0
            bwb_aft_centerbody_taper      = 0
            W_cabin                       = 0
            fuselage.mass_properties.mass = 0      
    
    
    # Compute Propulsor Weight
    number_of_tanks =  0
    for network in vehicle.networks:
        W_propulsion = 0
        no_of_engines = 0
        for propulsor in network.propulsors:
                if type(propulsor) == RCAIDE.Library.Components.Propulsors.Turbofan:
                    no_of_engines  += 1
                    thrust_sls            = propulsor.sealevel_static_thrust
                    W_engine_jet          = Propulsion.compute_jet_engine_weight(thrust_sls)
                    total_propulsor_mass  = Propulsion.integrated_propulsion(W_engine_jet)
                    propulsor.mass_properties.mass = total_propulsor_mass
                    W_propulsion   += total_propulsor_mass
        for fuel_line in network.fuel_lines: 
            for fuel_tank in fuel_line.fuel_tanks:
                number_of_tanks +=  1

        
    # Compute Wing Weight 
    for wing in vehicle.wings:
        if isinstance(wing,RCAIDE.Library.Components.Wings.Main_Wing):
            rho      = Aluminum().density
            sigma    = Aluminum().yield_tensile_strength           
            W_wing   = Common.compute_main_wing_weight(vehicle,wing, rho, sigma)
            wing.mass_properties.mass = W_wing

    # Calculating Landing Gear Weight 
    landing_gear        = Common.compute_landing_gear_weight(vehicle)
    
    # Compute Aft Center Body Weight 
    W_aft_centerbody   = compute_aft_centerbody_weight(no_of_engines,bwb_aft_centerbody_area, bwb_aft_centerbody_taper, TOW)
    
    # Compute Systems Weight     
    systems_weights     = Common.compute_systems_weight(vehicle) 

    # Compute Payload Weight     
    payload = Common.compute_payload_weight(vehicle) 
    vehicle.payload.passengers = RCAIDE.Library.Components.Component()
    vehicle.payload.baggage    = RCAIDE.Library.Components.Component()
    vehicle.payload.cargo      = RCAIDE.Library.Components.Component()
    
    vehicle.payload.passengers.mass_properties.mass = payload.passengers
    vehicle.payload.baggage.mass_properties.mass    = payload.baggage
    vehicle.payload.cargo.mass_properties.mass      = payload.cargo 
    payload.total =  payload.passengers +  payload.baggage +  payload.cargo 

    # Compute Peripheral Operating Items Weights 
    W_oper = Transport.compute_operating_items_weight(vehicle)
    
    # Store Weights Results 
    output                                     = Data()
    output.empty                               = Data()
    output.empty.structural                    = Data()
    output.empty.structural.wings              = W_wing
    output.empty.structural.afterbody          = W_aft_centerbody
    output.empty.structural.fuselage           = W_cabin
    output.empty.structural.landing_gear       = landing_gear.main +  landing_gear.nose 
    output.empty.structural.nacelle            = 0
    output.empty.structural.paint              = 0   
    output.empty.structural.total              = output.empty.structural.wings + output.empty.structural.afterbody \
                                                      + output.empty.structural.fuselage + output.empty.structural.landing_gear \
                                                      + output.empty.structural.paint + output.empty.structural.nacelle

    output.empty.propulsion                     = Data()
    output.empty.propulsion.total               = W_propulsion
    output.empty.propulsion.engines             = 0
    output.empty.propulsion.thrust_reversers    = 0
    output.empty.propulsion.miscellaneous       = 0
    output.empty.propulsion.fuel_system         = 0

    output.empty.systems                        = Data()
    output.empty.systems.control_systems        = systems_weights.W_flight_control
    output.empty.systems.apu                    = systems_weights.W_apu
    output.empty.systems.electrical             = systems_weights.W_electrical
    output.empty.systems.avionics               = systems_weights.W_avionics
    output.empty.systems.hydraulics             = systems_weights.W_hyd_pnu
    output.empty.systems.furnishings            = systems_weights.W_furnish
    output.empty.systems.air_conditioner        = systems_weights.W_ac
    output.empty.systems.instruments            = systems_weights.W_instruments
    output.empty.systems.anti_ice               = 0
    output.empty.systems.total                  = output.empty.systems.control_systems + output.empty.systems.apu \
                                                            + output.empty.systems.electrical + output.empty.systems.avionics \
                                                             + output.empty.systems.hydraulics + output.empty.systems.furnishings \
                                                             + output.empty.systems.air_conditioner + output.empty.systems.instruments \
                                                             + output.empty.systems.anti_ice
          
                        
    output.operational_items                   = Data()
    output.operational_items                   = W_oper 
    output.empty.total                         = output.empty.structural.total + output.empty.propulsion.total + output.empty.systems.total  + output.operational_items.total  
    output.payload                             = payload
    output.zero_fuel_weight                    = output.empty.total + output.payload.total   
   
    if use_max_fuel_weight:  # assume fuel is equally distributed in fuel tanks
        total_fuel_weight  = vehicle.mass_properties.max_takeoff -  output.zero_fuel_weight
        for network in vehicle.networks: 
            for fuel_line in network.fuel_lines:  
                for fuel_tank in fuel_line.fuel_tanks:
                    fuel_weight =  total_fuel_weight/number_of_tanks  
                    fuel_tank.fuel.mass_properties.mass = fuel_weight
        output.fuel = total_fuel_weight 
        output.total = output.zero_fuel_weight + output.fuel
    else:
        total_fuel_weight =  0
        for network in vehicle.networks: 
            for fuel_line in network.fuel_lines:  
                for fuel_tank in fuel_line.fuel_tanks:
                    fuel_mass =  fuel_tank.fuel.density * fuel_tank.volume
                    fuel_tank.fuel.mass_properties.mass = fuel_mass * 9.81
                    total_fuel_weight = fuel_mass * 9.81 
        output.fuel = total_fuel_weight
        output.total = output.zero_fuel_weight + output.fuel
     
    control_systems                                  = RCAIDE.Library.Components.Component()
    control_systems.tag                              = 'control_systems'  
    electrical_systems                               = RCAIDE.Library.Components.Component()
    electrical_systems.tag                           = 'electrical_systems'
    furnishings                                      = RCAIDE.Library.Components.Component()
    furnishings.tag                                  = 'furnishings'
    air_conditioner                                  = RCAIDE.Library.Components.Component() 
    air_conditioner.tag                              = 'air_conditioner'
    apu                                              = RCAIDE.Library.Components.Component()
    apu.tag                                          = 'apu'
    hydraulics                                       = RCAIDE.Library.Components.Component()
    hydraulics.tag                                   = 'hydraulics'
    avionics                                         = RCAIDE.Library.Components.Systems.Avionics()
    optionals                                        = RCAIDE.Library.Components.Component()
    optionals.tag                                    = 'optionals'
          
    nose_landing_gear = False
    main_landing_gear = False
    for LG in vehicle.landing_gears:
        if isinstance(LG, RCAIDE.Library.Components.Landing_Gear.Main_Landing_Gear):
            LG.mass_properties.mass = landing_gear.main
            main_landing_gear = True
        elif isinstance(LG, RCAIDE.Library.Components.Landing_Gear.Nose_Landing_Gear):
            LG.mass_properties.mass = landing_gear.nose
            nose_landing_gear = True 
    if nose_landing_gear == False:
        nose_gear = RCAIDE.Library.Components.Landing_Gear.Nose_Landing_Gear()  
        nose_gear.mass_properties.mass = landing_gear.nose    
        vehicle.append_component(nose_gear) 
    if main_landing_gear == False:
        main_gear = RCAIDE.Library.Components.Landing_Gear.Main_Landing_Gear()  
        main_gear.mass_properties.mass = landing_gear.main  
        vehicle.append_component(main_gear) 
         
    control_systems.mass_properties.mass             = output.empty.systems.control_systems
    electrical_systems.mass_properties.mass          = output.empty.systems.electrical
    furnishings.mass_properties.mass                 = output.empty.systems.furnishings
    avionics.mass_properties.mass                    = output.empty.systems.avionics \
                                                     + output.empty.systems.instruments
    air_conditioner.mass_properties.mass             = output.empty.systems.air_conditioner 
    apu.mass_properties.mass                         = output.empty.systems.apu
    hydraulics.mass_properties.mass                  = output.empty.systems.hydraulics
    optionals.mass_properties.mass                   = output.operational_items.misc

    # assign components to vehicle
    vehicle.control_systems    = control_systems
    vehicle.electrical_systems = electrical_systems
    vehicle.avionics           = avionics
    vehicle.furnishings        = furnishings
    vehicle.air_conditioner    = air_conditioner 
    vehicle.apu                = apu
    vehicle.hydraulics         = hydraulics
    vehicle.optionals          = optionals

    return output
