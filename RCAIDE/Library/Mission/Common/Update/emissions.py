# RCAIDE/Library/Mission/Common/Update/emissions.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  emissions
# ----------------------------------------------------------------------------------------------------------------------

def emissions(segment):
    """
    Updates vehicle emissions calculations for current segment

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function evaluates the emissions model if one is defined for the
    segment. It handles all types of emissions calculations and updates
    the segment conditions accordingly.

    **Required Segment Components**

    segment:
        analyses:
            emissions : Model, optional
                Emissions analysis model

    **Major Assumptions**
    * Valid emissions model if defined
    * Compatible segment conditions
    * Well-defined operating state

    Returns
    -------
    None
        Updates segment conditions directly through emissions model

   
    """   
    emissions_model = segment.analyses.emissions
    
    if emissions_model:
        emissions_model.evaluate(segment)    