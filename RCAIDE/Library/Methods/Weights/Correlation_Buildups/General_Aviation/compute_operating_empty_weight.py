# RCAIDE/Library/Methods/Weights/Correlation_Buildups/General_Aviation/compute_landing_gear_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE
import RCAIDE
from RCAIDE.Framework.Core import  Units , Data 
from .compute_fuselage_weight import compute_fuselage_weight
from .compute_landing_gear_weight import compute_landing_gear_weight
from .compute_payload_weight import compute_payload_weight
from .compute_systems_weight import compute_systems_weight
from .compute_horizontal_tail_weight import compute_horizontal_tail_weight
from .compute_vertical_tail_weight import compute_vertical_tail_weight
from .compute_main_wing_weight import compute_main_wing_weight
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Propulsion as Propulsion 


# ----------------------------------------------------------------------------------------------------------------------
# Main Wing Weight 
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_operating_empty_weight(vehicle, settings=None):
    """ output = RCAIDE.Methods.Weights.Correlations.Tube_Wing.empty(engine,wing,aircraft,fuselage,horizontal,vertical)
        Computes the empty weight breakdown of a General Aviation type aircraft  
        
        Inputs:
            engine - a data dictionary with the fields:                    
                thrust_sls - sea level static thrust of a single engine [Newtons]

            vehicle - a data dictionary with the fields:                    
                reference_area                                                            [meters**2]
                envelope - a data dictionary with the fields:
                    ultimate_load - ultimate load of the aircraft                         [dimensionless]
                    limit_load    - limit load factor at zero fuel weight of the aircraft [dimensionless]
                
                mass_properties - a data dictionary with the fields:
                    max_takeoff   - max takeoff weight of the vehicle           [kilograms]
                    max_zero_fuel - maximum zero fuel weight of the aircraft    [kilograms]
                    cargo         - cargo weight                                [kilograms]
                
                passengers - number of passengers on the aircraft               [dimensionless]
                        
                design_dynamic_pressure - dynamic pressure at cruise conditions [Pascal]
                design_mach_number      - mach number at cruise conditions      [dimensionless]
                
                networks - a data dictionary with the fields: 
                    keys           - identifier for the type of network; different types have different fields
                        turbofan
                            thrust_sls - sealevel standard thrust                               [Newtons]             
                        internal_combustion
                            rated_power - maximum rated power of the internal combustion engine [Watts]
                        
                    number_of_engines - integer indicating the number of engines on the aircraft

                W_cargo - weight of the bulk cargo being carried on the aircraft [kilograms]
                num_seats - number of seats installed on the aircraft [dimensionless]
                ctrl - specifies if the control system is "fully powered", "partially powered", or not powered [dimensionless]
                ac - determines type of instruments, electronics, and operating items based on types: 
                    "short-range", "medium-range", "long-range", "business", "cargo", "commuter", "sst" [dimensionless]
                w2h - tail length (distance from the airplane c.g. to the horizontal tail aerodynamic center) [meters]
                
                fuel - a data dictionary with the fields: 
                    mass_properties  - a data dictionary with the fields:
                        mass -mass of fuel [kilograms]
                    density          - gravimetric density of fuel                             [kilograms/meter**3]    
                    number_of_tanks  - number of external fuel tanks                           [dimensionless]
                    internal_volume  - internal fuel volume contained in the wing              [meters**3]
                wings - a data dictionary with the fields:    
                    wing - a data dictionary with the fields:
                        span                      - span of the wing                           [meters]
                        taper                     - taper ratio of the wing                    [dimensionless]
                        thickness_to_chord        - thickness-to-chord ratio of the wing       [dimensionless]
                        chords - a data dictionary with the fields:
                            mean_aerodynamic - mean aerodynamic chord of the wing              [meters]
                            root             - root chord of the wing                          [meters]
                            
                            
                        sweeps - a data dictionary with the fields:
                            quarter_chord - quarter chord sweep angle of the wing              [radians]
                        mac                       - mean aerodynamic chord of the wing         [meters]
                        r_c                       - wing root chord                            [meters]
                        origin  - location of the leading edge of the wing relative to the front of the fuselage                                      [meters,meters,meters]
                        aerodynamic_center - location of the aerodynamic center of the horizontal_stabilizer relative to the leading edge of the wing [meters,meters,meters]
        
                    
                    
                    
                    horizontal_stabilizer - a data dictionary with the fields:
                        areas -  a data dictionary with the fields:
                            reference - reference area of the horizontal stabilizer                                    [meters**2]
                            exposed  - exposed area for the horizontal tail                                            [meters**2]
                        taper   - taper ratio of the horizontal stabilizer                                             [dimensionless]
                        span    - span of the horizontal tail                                                          [meters]
                        sweeps - a data dictionary with the fields:
                            quarter_chord - quarter chord sweep angle of the horizontal stabilizer                     [radians]
                        chords - a data dictionary with the fields:
                            mean_aerodynamic - mean aerodynamic chord of the horizontal stabilizer                     [meters]         
                            root             - root chord of the horizontal stabilizer             
                        thickness_to_chord - thickness-to-chord ratio of the horizontal tail                           [dimensionless]
                        mac     - mean aerodynamic chord of the horizontal tail                                        [meters]
                        origin  - location of the leading of the horizontal tail relative to the front of the fuselage                                                 [meters,meters,meters]
                        aerodynamic_center - location of the aerodynamic center of the horizontal_stabilizer relative to the leading edge of the horizontal stabilizer [meters,meters,meters]
        
                    vertical - a data dictionary with the fields:
                        areas -  a data dictionary with the fields:
                            reference - reference area of the vertical stabilizer         [meters**2]
                        span    - span of the vertical tail                               [meters]
                        taper   - taper ratio of the horizontal stabilizer                [dimensionless]
                        t_c     - thickness-to-chord ratio of the vertical tail           [dimensionless]
                        sweeps   - a data dictionary with the fields:
                            quarter_chord - quarter chord sweep angle of the vertical stabilizer [radians]
                        t_tail - flag to determine if aircraft has a t-tail, "yes"               [dimensionless]


                
                fuselages - a data dictionary with the fields:  
                    fuselage - a data dictionary with the fields:
                        areas             - a data dictionary with the fields:
                            wetted - wetted area of the fuselage [meters**2]
                        differential_pressure  - Maximum fuselage pressure differential   [Pascal]
                        width             - width of the fuselage                         [meters]
                        heights - a data dictionary with the fields:
                            maximum - height of the fuselage                              [meters]
                        lengths-  a data dictionary with the fields:
                            structure - structural length of the fuselage                 [meters]                     
                        mass_properties - a data dictionary with the fields:
                            volume - total volume of the fuselage                         [meters**3]
                            internal_volume - internal volume of the fuselage             [meters**3]
                        number_coach_sets - number of seats on the aircraft               [dimensionless]    
                landing_gear - a data dictionary with the fields:
                    main - a data dictionary with the fields:
                        strut_length - strut length of the main gear                      [meters]
                    nose - a data dictionary with the fields:
                        strut_length - strut length of the nose gear                      [meters]
                avionics - a data dictionary, used to determine if avionics weight is calculated, don't include if vehicle has none
                air_conditioner - a data dictionary, used to determine if air conditioner weight is calculated, don't include if vehicle has none
        
        
        Outputs:
            output - a data dictionary with fields:
                wing - wing weight                            [kilograms]
                fuselage - fuselage weight                    [kilograms]
                propulsion - propulsion                       [kilograms]
                landing_gear_main - main gear weight          [kilograms]
                landing_gear_nose - nose gear weight          [kilograms]
                horizonal_tail - horizontal stabilizer weight [kilograms]
                vertical_tail - vertical stabilizer weight    [kilograms]
                systems - total systems weight                [kilograms]
                systems - a data dictionary with fields:
                    control_systems - control systems weight  [kilograms]
                    hydraulics - hydraulics weight            [kilograms]
                    avionics - avionics weight                [kilograms]
                    electric - electrical systems weight      [kilograms]
                    air_conditioner - air conditioner weight  [kilograms]
                    furnish - furnishing weight               [kilograms]
                    fuel_system - fuel system weight          [ kilograms]
           Wing, empannage, fuselage, propulsion and individual systems masses updated with their calculated values
       Assumptions:
            calculated aircraft weight from correlations created per component of historical aircraft
        
    """     

    if settings == None: 
        use_max_fuel_weight = True 
    else:
        use_max_fuel_weight = settings.use_max_fuel_weight
        
    # Unpack inputs
    S_gross_w   = vehicle.reference_area
    Nult        = vehicle.flight_envelope.ultimate_load 
    TOW         = vehicle.mass_properties.max_takeoff 
    num_pax     = vehicle.passengers
    W_cargo     = vehicle.mass_properties.cargo 
    q_c         = vehicle.design_dynamic_pressure
    mach_number = vehicle.flight_envelope.design_mach_number
 
    landing_weight              = TOW
    m_fuel                      =  0
    number_of_tanks             =  0
    V_fuel                      =  0
    V_fuel_int                  =  0
    W_energy_network_cumulative =  0
    number_of_engines           =  0
 
    for network in vehicle.networks:
        W_energy_network_total   = 0
        number_of_jet_engines    = 0
        number_of_piston_engines = 0  

        for fuel_line in  network.fuel_lines: 
            for fuel_tank in fuel_line.fuel_tanks: 
                m_fuel_tank     = fuel_tank.fuel.mass_properties.mass
                m_fuel          += m_fuel_tank   
                landing_weight  -= m_fuel_tank   
                number_of_tanks += 1
                V_fuel_int      += m_fuel_tank/fuel_tank.fuel.density  #assume all fuel is in integral tanks 
                V_fuel          += m_fuel_tank/fuel_tank.fuel.density #total fuel  
         
        # Electric-Powered Propulsors  
        for bus in network.busses: 
            # electrical payload 
            W_energy_network_total  += bus.payload.mass_properties.mass * Units.kg
     
            # Avionics Weight 
            W_energy_network_total  += bus.avionics.mass_properties.mass      
    
            for battery in bus.battery_modules: 
                W_energy_network_total  += battery.mass_properties.mass * Units.kg
                  
            for propulsor in bus.propulsors:
                if 'motor' in propulsor: 
                    motor_mass = propulsor.motor.mass_properties.mass       
                    W_energy_network_cumulative  += motor_mass                
        
        for propulsor in  network.propulsors: 
            if type(propulsor) ==  RCAIDE.Library.Components.Propulsors.Turbofan:
                number_of_jet_engines += 1
                thrust_sls    =  propulsor.sealevel_static_thrust 
                W_engine_jet            = Propulsion.compute_jet_engine_weight(thrust_sls)
                W_propulsion            = Propulsion.integrated_propulsion(W_engine_jet,number_of_jet_engines) 
                propulsor.mass_properties.mass = W_propulsion
                W_energy_network_total  += W_propulsion                
            elif type(propulsor) ==  RCAIDE.Library.Components.Propulsors.ICE_Propeller:      
                number_of_piston_engines += 1
                rated_power              = propulsor.engine.sea_level_power 
                W_engine_piston          = Propulsion.compute_piston_engine_weight(rated_power)
                W_propulsion             = Propulsion.integrated_propulsion_general_aviation(W_engine_piston,number_of_piston_engines) 
                propulsor.mass_properties.mass = W_propulsion
                W_energy_network_total  += W_propulsion
            elif type(propulsor) ==  RCAIDE.Library.Components.Propulsors.Turboprop:      
                number_of_piston_engines += 1
                rated_power   = propulsor.design_power 
                W_engine_piston          = Propulsion.compute_piston_engine_weight(rated_power)
                W_propulsion             = Propulsion.integrated_propulsion_general_aviation(W_engine_piston,number_of_piston_engines) 
                propulsor.mass_properties.mass = W_propulsion
                W_energy_network_total  += W_propulsion        
                
        W_energy_network_cumulative += W_energy_network_total
        number_of_engines           +=  number_of_jet_engines +  number_of_piston_engines
    
    for wing in vehicle.wings:
        if isinstance(wing,RCAIDE.Library.Components.Wings.Main_Wing):
            b          = wing.spans.projected
            AR_w       = (b**2.)/S_gross_w
            taper_w    = wing.taper
            t_c_w      = wing.thickness_to_chord
            sweep_w    = wing.sweeps.quarter_chord  
            W_wing    = compute_main_wing_weight(S_gross_w, m_fuel, AR_w, sweep_w, q_c, taper_w, t_c_w,Nult,TOW)
            wing.mass_properties.mass = W_wing
            
            # set main wing to be used in future horizontal tail calculations 
            main_wing  =  wing
        
    l_w2h = 0
    W_tail_horizontal =  0
    W_tail_vertical   =  0
    for wing in vehicle.wings:            
        if isinstance(wing,RCAIDE.Library.Components.Wings.Horizontal_Tail):
            S_h                = wing.areas.reference
            b_h                = wing.spans.projected
            AR_h               = (b_h**2.)/S_h
            taper_h            = wing.spans.projected
            sweep_h            = wing.sweeps.quarter_chord 
            t_c_h              = wing.thickness_to_chord
            l_w2h              = wing.origin[0][0] + wing.aerodynamic_center[0] - main_wing.origin[0][0] - main_wing.aerodynamic_center[0] 
            W_tail_horizontal  = compute_horizontal_tail_weight(S_h, AR_h, sweep_h, q_c, taper_h, t_c_h,Nult,TOW)                 
            wing.mass_properties.mass = W_tail_horizontal     
        if isinstance(wing,RCAIDE.Library.Components.Wings.Vertical_Tail):     
            S_v               = wing.areas.reference
            b_v               = wing.spans.projected
            AR_v              = (b_v**2.)/S_v
            taper_v           = wing.taper
            t_c_v             = wing.thickness_to_chord
            sweep_v           = wing.sweeps.quarter_chord
            t_tail            = wing.t_tail  
            W_tail_vertical   = compute_vertical_tail_weight(S_v, AR_v, sweep_v, q_c, taper_v, t_c_v, Nult,TOW,t_tail) 
            wing.mass_properties.mass = W_tail_vertical
    
    for fuselage in  vehicle.fuselages: 
        S_fus       = fuselage.areas.wetted
        diff_p_fus  = fuselage.differential_pressure
        w_fus       = fuselage.width
        h_fus       = fuselage.heights.maximum 
        l_fus       = fuselage.lengths.total-fuselage.lengths.tail  
        V_fuse      = fuselage.mass_properties.volume 
        num_seats   = fuselage.number_coach_seats  
        W_fuselage  = compute_fuselage_weight(S_fus, Nult, TOW, w_fus, h_fus, l_fus, l_w2h, q_c, V_fuse, diff_p_fus)
        fuselage.mass_properties.mass = W_fuselage
        
    # landing gear 
    strut_length_main = 0
    strut_length_nose = 0 
    nose_landing_gear = False
    main_landing_gear = False
    for LG in vehicle.landing_gears:
        if isinstance(LG, RCAIDE.Library.Components.Landing_Gear.Main_Landing_Gear):
            strut_length_main = LG.strut_length
            main_landing_gear = True
        elif isinstance(LG, RCAIDE.Library.Components.Landing_Gear.Nose_Landing_Gear):
            strut_length_nose = LG.strut_length 
            nose_landing_gear = True
    W_landing_gear         = compute_landing_gear_weight(landing_weight, Nult, strut_length_main, strut_length_nose) 
    for landing_gear in vehicle.landing_gears:
        if isinstance(landing_gear, RCAIDE.Library.Components.Landing_Gear.Main_Landing_Gear):
            landing_gear.mass_properties.mass = W_landing_gear.main
            main_landing_gear = True
        elif isinstance(landing_gear, RCAIDE.Library.Components.Landing_Gear.Nose_Landing_Gear):
            landing_gear.mass_properties.mass = W_landing_gear.nose
            nose_landing_gear = True 
    if nose_landing_gear == False:
        nose_gear = RCAIDE.Library.Components.Landing_Gear.Nose_Landing_Gear()  
        nose_gear.mass_properties.mass = W_landing_gear.nose
        vehicle.append_component(nose_gear) 
    if main_landing_gear == False:
        main_gear = RCAIDE.Library.Components.Landing_Gear.Main_Landing_Gear()  
        main_gear.mass_properties.mass = W_landing_gear.main
        vehicle.append_component(main_gear)
         
    if len(vehicle.avionics) == 0:
        avionics     = RCAIDE.Library.Components.Systems.Avionics()
        W_uav        = 0. 
    else:
        avionics = vehicle.avionics
        W_uav    = avionics.mass_properties.uninstalled

    has_air_conditioner = 0
    if 'air_conditioner' in vehicle:
        has_air_conditioner = 1

    # Calculating Empty Weight of Aircraft
    W_systems           = compute_systems_weight(W_uav,V_fuel, V_fuel_int, number_of_tanks, number_of_engines, l_fus, b, TOW, Nult, num_seats, mach_number, has_air_conditioner)

    # Calculate the equipment empty weight of the aircraft

    W_empty           = (W_wing + W_fuselage + W_landing_gear.main+W_landing_gear.nose + W_energy_network_cumulative + W_systems.total + \
                          W_tail_horizontal +W_tail_vertical) 

    # packup outputs
    W_payload = compute_payload_weight(TOW, W_empty, num_pax,W_cargo)
    
    vehicle.payload.passengers = RCAIDE.Library.Components.Component()
    vehicle.payload.baggage    = RCAIDE.Library.Components.Component()
    vehicle.payload.cargo      = RCAIDE.Library.Components.Component()
    
    vehicle.payload.passengers.mass_properties.mass = W_payload.passengers
    vehicle.payload.baggage.mass_properties.mass    = W_payload.baggage
    vehicle.payload.cargo.mass_properties.mass      = W_payload.cargo        


    # Distribute all weight in the output fields
    output                                    = Data()
    output.empty                              = Data()
    output.empty.structural                   = Data()
    output.empty.structural.wings             = W_wing +  W_tail_horizontal + W_tail_vertical 
    output.empty.structural.fuselage          = W_fuselage
    output.empty.structural.landing_gear      = W_landing_gear.main +  W_landing_gear.nose 
    output.empty.structural.nacelle           = 0
    output.empty.structural.paint             = 0  
    output.empty.structural.total             = output.empty.structural.wings \
                                                     + output.empty.structural.fuselage  + output.empty.structural.landing_gear \
                                                     + output.empty.structural.paint + output.empty.structural.nacelle
          
    output.empty.propulsion                   = Data()
    output.empty.propulsion.total             = W_energy_network_cumulative
    output.empty.propulsion.fuel_system       = W_systems.W_fuel_system
  
    output.empty.systems                      = Data()
    output.empty.systems.control_systems      = W_systems.W_flight_control
    output.empty.systems.hydraulics           = W_systems.W_hyd_pnu
    output.empty.systems.avionics             = W_systems.W_avionics
    output.empty.systems.electrical           = W_systems.W_electrical
    output.empty.systems.air_conditioner      = W_systems.W_ac
    output.empty.systems.furnishings              = W_systems.W_furnish
    output.empty.systems.apu                  = 0
    output.empty.systems.instruments          = 0
    output.empty.systems.anti_ice             = 0
    output.empty.systems.total                = output.empty.systems.control_systems + output.empty.systems.apu \
                                                  + output.empty.systems.electrical + output.empty.systems.avionics \
                                                  + output.empty.systems.hydraulics + output.empty.systems.furnishings \
                                                  + output.empty.systems.air_conditioner + output.empty.systems.instruments \
                                                  + output.empty.systems.anti_ice
  
    output.payload                                = Data()
    output.payload                                = W_payload
    output.operational_items                      = Data()
    output.operational_items.oper_items           = 0
    output.operational_items.flight_crew          = 0
    output.operational_items.flight_attendants    = 0
    output.operational_items.total                = 0

    output.empty.total      = output.empty.structural.total + output.empty.propulsion.total + output.empty.systems.total
    output.operating_empty  = output.empty.total + output.operational_items.total
    output.zero_fuel_weight =  output.operating_empty + output.payload.total 

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
    hydraulics                                       = RCAIDE.Library.Components.Component()
    hydraulics.tag                                   = 'hydraulics'  
     
    nose_landing_gear = False
    main_landing_gear =  False
    for LG in vehicle.landing_gears:
        if isinstance(LG, RCAIDE.Library.Components.Landing_Gear.Main_Landing_Gear):
            LG.mass_properties.mass = W_landing_gear.main
            main_landing_gear = True
        elif isinstance(LG, RCAIDE.Library.Components.Landing_Gear.Nose_Landing_Gear):
            LG.mass_properties.mass = W_landing_gear.nose
            nose_landing_gear = True 
    if nose_landing_gear == False:
        nose_gear = RCAIDE.Library.Components.Landing_Gear.Nose_Landing_Gear()  
        nose_gear.mass_properties.mass = W_landing_gear.nose 
        vehicle.append_component(nose_gear) 
    if main_landing_gear == False:
        main_gear = RCAIDE.Library.Components.Landing_Gear.Main_Landing_Gear()  
        main_gear.mass_properties.mass = W_landing_gear.main
        vehicle.append_component(main_gear)
         
    control_systems.mass_properties.mass    = output.empty.systems.control_systems
    electrical_systems.mass_properties.mass = output.empty.systems.electrical
    furnishings.mass_properties.mass        = output.empty.systems.furnishings
    avionics.mass_properties.mass           = output.empty.systems.avionics + output.empty.systems.instruments
    air_conditioner.mass_properties.mass    = output.empty.systems.air_conditioner 
    hydraulics.mass_properties.mass         = output.empty.systems.hydraulics

    # assign components to vehicle
    vehicle.control_systems                             = control_systems
    vehicle.electrical_systems                          = electrical_systems
    vehicle.avionics                                    = avionics
    vehicle.furnishings                                 = furnishings 
    vehicle.hydraulics                                  = hydraulics
    if has_air_conditioner:
        vehicle.air_conditioner.mass_properties.mass    = output.empty.systems.air_conditioner 
    return output