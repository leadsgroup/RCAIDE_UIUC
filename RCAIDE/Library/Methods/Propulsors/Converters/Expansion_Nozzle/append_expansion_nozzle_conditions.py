# RCAIDE/Library/Methods/Propulsors/Converters/expansion_nozzle/append_expansion_nozzle_conditions.py
# 
# Created:  Jun 2024, M. Clarke  

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
# append_expansion_nozzle_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_expansion_nozzle_conditions(expansion_nozzle,segment,propulsor_conditions):   
    """
    Initializes condition containers for expansion nozzle analysis by creating input 
    and output data structures for the specified nozzle.

    Parameters
    ----------
    expansion_nozzle : RCAIDE.Core.Propulsors.Converters.Expansion_Nozzle
        The expansion nozzle instance to analyze
    segment : RCAIDE.Core.Analyses.Mission.Segments
        The mission segment being analyzed
    propulsor_conditions : dict
        Dictionary containing all propulsor conditions for the analysis

    Returns
    -------
    None

    Notes
    -----
    This function creates empty Conditions() objects for both inputs and outputs for propulsor_conditions
    that will be populated during the expansion nozzle performance calculations.
    
    **Major Assumptions**
        * Each expansion nozzle requires its own unique tag in propulsor_conditions
    
    See Also
    --------
    RCAIDE.Library.Methods.Propulsors.Converters.Expansion_Nozzle.compute_expansion_nozzle_performance
    """
    propulsor_conditions[expansion_nozzle.tag]                      = Conditions()
    propulsor_conditions[expansion_nozzle.tag].inputs               = Conditions()
    propulsor_conditions[expansion_nozzle.tag].outputs              = Conditions() 
    return 