# RCAIDE/Library/Methods/Weights/Correlation_Buildups/General_Aviation/compute_operating_empty_weight.py
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
    """
    Computes the operating empty weight breakdown of a General Aviation type aircraft using empirical correlations.

    Parameters
    ----------
    vehicle : RCAIDE.Vehicle()
        Vehicle data structure containing all vehicle information
            - reference_area : float
                Wing reference area [m^2]
            - flight_envelope : Data()
                Contains ultimate_load and design_mach_number
            - mass_properties : Data()
                Contains max_takeoff, cargo weights
            - networks : list
                List of propulsion networks
            - wings : list
                List of all wing components (main wing, tails)
            - fuselages : list
                List of fuselage components
            - landing_gears : list
                List of landing gear components
    settings : Data(), optional
        Configuration settings
            - use_max_fuel_weight : bool
                Flag for using maximum fuel weight in calculations

    Returns
    -------
    output : Data()
        Weight breakdown of the aircraft
            - empty : Data()
                Empty weight components (structural, propulsion, systems)
            - payload : Data()
                Payload weight breakdown
            - operational_items : Data()
                Crew and operational items weights
            - fuel : float
                Total fuel weight [kg]
            - total : float
                Total aircraft weight [kg]

    Notes
    -----
    This method computes the complete weight breakdown of a general aviation aircraft
    using empirical correlations. It handles multiple types of propulsion systems
    including electric, turbofan, piston, and turboprop engines. Refer to Raymer [1] 
    for more details.

    **Major Assumptions**
        * Weight correlations are based on historical general aviation aircraft data

    **Theory**
    The method uses a buildup approach where individual component weights are calculated
    separately and summed to get the total aircraft weight:

    .. math::
        W_{empty} = W_{wing} + W_{fuselage} + W_{landing\_gear} + W_{propulsion} + W_{systems} + W_{tail}

    References
    ----------
    [1] Raymer, D. P. (2018). Aircraft design: A conceptual approach: A conceptual approach. 
        American Institute of Aeronautics and Astronautics Inc. 

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation.compute_main_wing_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation.compute_fuselage_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation.compute_landing_gear_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation.compute_systems_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation.compute_horizontal_tail_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation.compute_vertical_tail_weight
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