# RCAIDE/Library/Mission/Common/Update/altitude.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Altitude
# ---------------------------------------------------------------------------------------------------------------------- 
def altitude(segment):
    """
    Updates freestream altitude from inertial position

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function extracts the altitude from the negative z-component
    of the inertial position vector.

    **Required Segment Components**

    segment.state.conditions:
        frames.inertial:
            - position_vector : array
                Vehicle position [m]

    **Major Assumptions**
    * Flat earth
    * Z-axis points down
    * Altitude is negative of z-position

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.freestream.altitude [m]

    See Also
    --------
    RCAIDE.Framework.Mission.Segments
    """    
    altitude = -segment.state.conditions.frames.inertial.position_vector[:,2]
    segment.state.conditions.freestream.altitude[:,0] = altitude 