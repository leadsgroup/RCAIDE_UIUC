# RCAIDE/Library/Missions/Segments/Common/Update/differentials_time.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Update Differentials Time
# ----------------------------------------------------------------------------------------------------------------------

def differentials_time(segment):
    """ Updates the time descretization 
        
        Assumptions:
        N/A
        
        Inputs:
            segment.state.conditions:
                .frames.inertial.time         [s]
        Outputs:
            segment.state.numerics.time
                .control_points               [s]
                .differentiate                [-]
                .integrate                    [-]

      
        Properties Used:
        N/A
                    
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
