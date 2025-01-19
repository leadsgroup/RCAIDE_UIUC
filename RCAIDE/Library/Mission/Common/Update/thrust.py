# RCAIDE/Library/Mission/Common/Update/thrust.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Thrust
# ---------------------------------------------------------------------------------------------------------------------- 
def thrust(segment):
    """
    Updates propulsion system thrust and fuel consumption

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function evaluates the energy model to compute thrust forces,
    moments, and fuel consumption rates for all propulsors.

    **Required Segment Components**

    segment:
        analyses:
            energy : Model
                Energy/propulsion model
        state.conditions:
            frames.body:
                - thrust_force_vector : array
                    Propulsive forces [N]
                - thrust_moment_vector : array
                    Propulsive moments [N·m]
            weights:
                - vehicle_mass_rate : array
                    Total mass rate [kg/s]
                - vehicle_fuel_rate : array, optional
                    Main fuel consumption [kg/s]
                - vehicle_additional_fuel_rate : array, optional
                    Secondary fuel consumption [kg/s]

    **Major Assumptions**
    * Valid propulsion model
    * Quasi-steady operation
    * Well-defined energy networks
    * Compatible fuel systems

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.frames.body.thrust_force_vector [N]
        - conditions.frames.body.thrust_moment_vector [N·m]
        - conditions.weights.vehicle_mass_rate [kg/s]
        - conditions.weights.vehicle_fuel_rate [kg/s]
        - conditions.weights.vehicle_additional_fuel_rate [kg/s]

    
    """ 

    # unpack
    energy_model = segment.analyses.energy

    # evaluate
    energy_model.evaluate(segment.state)

    # pack conditions
    conditions = segment.state.conditions
    conditions.frames.body.thrust_force_vector       = conditions.energy.thrust_force_vector
    conditions.frames.body.thrust_moment_vector      = conditions.energy.thrust_moment_vector
    conditions.weights.vehicle_mass_rate             = conditions.energy.vehicle_mass_rate 

    if "vehicle_additional_fuel_rate" in conditions.energy: 
        conditions.weights.has_additional_fuel             = True
        conditions.weights.vehicle_fuel_rate               = conditions.energy.vehicle_fuel_rate
        conditions.weights.vehicle_additional_fuel_rate    = conditions.energy.vehicle_additional_fuel_rate  