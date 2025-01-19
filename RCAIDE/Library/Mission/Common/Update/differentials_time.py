# RCAIDE/Library/Mission/Segments/Common/Update/differentials_time.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Update Differentials Time
# ----------------------------------------------------------------------------------------------------------------------

def differentials_time(segment):
    """
    Updates time discretization operators for segment analysis

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function rescales the dimensionless time operators based on the
    actual segment duration. It handles both differentiation and integration
    operators.

    **Required Segment Components**

    segment.state:
        numerics:
            dimensionless:
                - control_points : array
                    Normalized time points [-]
                - differentiate : array
                    Differentiation operator [-]
                - integrate : array
                    Integration operator [-]
        conditions.frames.inertial:
            - time : array
                Segment time points [s]

    **Major Assumptions**
    * Valid time discretization
    * Well-defined segment duration
    * Linear time scaling

    Returns
    -------
    None
        Updates segment numerics directly:
        - numerics.time.control_points [s]
        - numerics.time.differentiate [-]
        - numerics.time.integrate [-]

    See Also
    --------
    RCAIDE.Framework.Mission.Segments
    """    
    
    # unpack
    numerics = segment.state.numerics
    x        = numerics.dimensionless.control_points
    D        = numerics.dimensionless.differentiate
    I        = numerics.dimensionless.integrate
    
    # rescale time
    time = segment.state.conditions.frames.inertial.time
    T    = time[-1] - time[0]
    t    = x * T
    
    # rescale operators
    D = D / T
    I = I * T
    
    # pack
    numerics.time.control_points = t
    numerics.time.differentiate  = D
    numerics.time.integrate      = I

    return
