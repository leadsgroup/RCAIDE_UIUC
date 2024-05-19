## @ingroup Library-Methods-Missions-Common-Unpack_Unknowns
# RCAIDE/Library/Methods/Missions/Common/Unpack_Unknowns/control_surfaces.py
# 
# 
# Created:  Jul 2023, M. Clarke
import RCAIDE

# ----------------------------------------------------------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Missions-Common-Unpack_Unknowns
def control_surfaces(segment):
    flight_controls   = segment.flight_controls
    control_surfaces  = segment.state.conditions.control_surfaces
    wings             = segment.analyses.aerodynamics.geometry.wings
    # loop through wings on aircraft
    for wing in wings:
        # Elevator Control
        if flight_controls.elevator_deflection.active:
            for control_surface in wing.control_surfaces:
                if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Elevator:
                    num_elev_ctrls = len(flight_controls.elevator_deflection.assigned_surfaces)
                    for i in range(num_elev_ctrls):   
                        for j in range(len(flight_controls.elevator_deflection.assigned_surfaces[i])):
                            elevator_name = flight_controls.elevator_deflection.assigned_surfaces[i][j]

                            # set deflection on vehicle
                            wing.control_surfaces[elevator_name].deflection = segment.state.unknowns["elevator_" + str(i)]

                            # set deflection in results data structure
                            control_surfaces.elevator.deflection  = segment.state.unknowns["elevator_" + str(i)]
                
        # Slat Control
        if flight_controls.slat_deflection.active:
            for control_surface in wing.control_surfaces:
                if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Slat:
                    num_slat_ctrls = len(flight_controls.slat_deflection.assigned_surfaces)
                    for i in range(num_slat_ctrls):   
                        for j in range(len(flight_controls.slat_deflection.assigned_surfaces[i])):
                            slat_name = flight_controls.slat_deflection.assigned_surfaces[i][j]

                            # set deflection on vehicle
                            wing.control_surfaces[slat_name].deflection = segment.state.unknowns["slat_" + str(i)]

                            # set deflection in results data structure
                            control_surfaces.slat.deflection  = segment.state.unknowns["slat_" + str(i)]


        # Rudder Control
        if flight_controls.rudder_deflection.active:
            for control_surface in wing.control_surfaces:
                if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Rudder:
                    num_rud_ctrls = len(flight_controls.rudder_deflection.assigned_surfaces)
                    for i in range(num_rud_ctrls):
                        for j in range(len(flight_controls.rudder_deflection.assigned_surfaces[i])):
                            rudder_name = flight_controls.rudder_deflection.assigned_surfaces[i][j]

                            # set deflection on vehicle
                            wing.control_surfaces[rudder_name].deflection = segment.state.unknowns["rudder_" + str(i)]

                            # set deflection in results data structure
                            control_surfaces.rudder.deflection  = segment.state.unknowns["rudder_" + str(i)]

        # flap Control
        if flight_controls.flap_deflection.active:
            for control_surface in wing.control_surfaces:
                if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Flap:
                    num_flap_ctrls = len(flight_controls.flap_deflection.assigned_surfaces)
                    for i in range(num_flap_ctrls):   
                        for j in range(len(flight_controls.flap_deflection.assigned_surfaces[i])):
                            flap_name = flight_controls.flap_deflection.assigned_surfaces[i][j]

                            # set deflection on vehicle
                            wing.control_surfaces[flap_name].deflection = segment.state.unknowns["flap_" + str(i)]

                            # set deflection in results data structure
                            control_surfaces.flap.deflection  = segment.state.unknowns["flap_" + str(i)]

        # Aileron Control
        if flight_controls.aileron_deflection.active:
            for control_surface in wing.control_surfaces:
                if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Aileron:
                    num_aile_ctrls = len(flight_controls.aileron_deflection.assigned_surfaces)
                    for i in range(num_aile_ctrls):   
                        for j in range(len(flight_controls.aileron_deflection.assigned_surfaces[i])):
                            aileron_name = flight_controls.aileron_deflection.assigned_surfaces[i][j]

                            # set deflection on vehicle
                            wing.control_surfaces[aileron_name].deflection = segment.state.unknowns["aileron_" + str(i)]

                            # set deflection in results data structure
                            control_surfaces.aileron.deflection  = segment.state.unknowns["aileron_" + str(i)]


    
    return