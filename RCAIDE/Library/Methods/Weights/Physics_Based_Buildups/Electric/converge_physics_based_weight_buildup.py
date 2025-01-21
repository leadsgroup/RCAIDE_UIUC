# RCAIDE/Library/Methods/Weights/Buildups/eVTOL/converge_physics_based_weight_buildup.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE
import RCAIDE 

# ----------------------------------------------------------------------------------------------------------------------
# converge_physics_based_weight_buildup
# ---------------------------------------------------------------------------------------------------------------------- 
def converge_physics_based_weight_buildup(base_vehicle,
                    print_iterations              = False,
                    miscelleneous_weight_factor   = 1.1,):
    """
    Iteratively converges the maximum takeoff weight (MTOW) of an electric aircraft by running successive physics-based 
    weight estimations until the computed weight matches the assumed weight.

    Parameters
    ----------
    base_vehicle : RCAIDE.Vehicle()
        RCAIDE vehicle data structure containing initial vehicle configuration
    print_iterations : bool, optional
        Flag to print weight difference at each iteration (default: False)
    miscelleneous_weight_factor : float, optional
        Factor to account for miscellaneous weights in the buildup (default: 1.1)

    Returns
    -------
    vehicle : RCAIDE.Vehicle()
        Vehicle data structure with converged weights
    breakdown : Data()
        Detailed weight breakdown of the converged configuration
            - empty : Data()
                Empty weight components
            - payload : Data()
                Payload weight components
            - total : float
                Total converged weight

    Notes
    -----
    The function uses an iterative process to converge the vehicle weight:
        1. Performs initial weight estimation
        2. Compares estimated weight to assumed MTOW
        3. Updates MTOW assumption
        4. Repeats until difference is less than 1 kg
    
    **Major Assumptions**
        * Convergence threshold of 1 kg is sufficient for design purposes
        * Maximum 100 iterations allowed for convergence
    
    See Also
    --------
    RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Electric.compute_operating_empty_weight
    RCAIDE.Framework.Analyses.Weights.Weights_EVTOL
    """
    

    weight_analysis          = RCAIDE.Framework.Analyses.Weights.Weights_EVTOL()
    weight_analysis.vehicle  = base_vehicle
    weight_analysis.settings.miscelleneous_weight_factor =  miscelleneous_weight_factor
    breakdown                = weight_analysis.evaluate() 
    build_up_mass            = breakdown.total    
    diff                     = weight_analysis.vehicle.mass_properties.max_takeoff - build_up_mass
    iterations               = 0
    
    while(abs(diff)>1):
        weight_analysis.vehicle.mass_properties.max_takeoff = weight_analysis.vehicle.mass_properties.max_takeoff - diff 
        breakdown      = weight_analysis.evaluate()         
        build_up_mass  = breakdown.total    
        diff           = weight_analysis.vehicle.mass_properties.max_takeoff - build_up_mass 
        iterations     += 1
        if print_iterations:
            print(round(diff,3))
        if iterations == 100:
            print('Weight convergence failed!')
            return False 
    print('Converged MTOW = ' + str(round(weight_analysis.vehicle.mass_properties.max_takeoff)) + ' kg') 
    
    return weight_analysis.vehicle , breakdown
