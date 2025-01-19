# RCAIDE/Library/Mission/Common/Update/gravity.py
# 
# 
# Created:  Jul 2023, M. Clarke


# ----------------------------------------------------------------------------------------------------------------------
#  Update Gravity
# ----------------------------------------------------------------------------------------------------------------------
def gravity(segment):
    """
    Updates gravitational acceleration for current altitude

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function computes the local gravitational acceleration based on
    altitude using the planet's gravity model. Currently uses a simple
    sea-level gravity model.

    **Required Segment Components**

    segment:
        analyses:
            planet:
                features:
                    - sea_level_gravity : float
                        Surface gravity [m/s²]
                - compute_gravity : function
                    Gravity model function
        conditions:
            freestream:
                - altitude : array
                    Vehicle altitude [m]

    **Major Assumptions**
    * Spherical planet
    * Simple gravity model
    * No terrain effects
    * No planetary rotation effects

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.freestream.gravity [m/s²]

    See Also
    --------
    RCAIDE.Attributes.Planets
    """      

    # unpack
    planet = segment.analyses.planet
    H      = segment.conditions.freestream.altitude
    
    # calculate
    g      = planet.compute_gravity(H)

    # pack
    segment.state.conditions.freestream.gravity[:,0] = g[:,0]

    return 