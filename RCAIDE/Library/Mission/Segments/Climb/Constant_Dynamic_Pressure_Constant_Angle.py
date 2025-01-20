# RCAIDE/Library/Mission/Segments/Climb/Constant_Dynamic_Pressure_Constant_Angle.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE 
import RCAIDE 

# Package imports  
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------
def initialize_conditions_unpack_unknowns(segment):
    """
    Initializes conditions for constant dynamic pressure climb with fixed angle

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function sets up the initial conditions for a climb segment with constant
    dynamic pressure and constant climb angle. It handles both initialization and
    unpacking of solver unknowns.

    **Required Segment Components**

    segment:
        - climb_angle : float
            Fixed climb angle [rad]
        - dynamic_pressure : float
            Dynamic pressure to maintain [Pa]
        - altitude_start : float
            Initial altitude [m]
        - sideslip_angle : float
            Aircraft sideslip angle [rad]
        - state:
            conditions : Data
                State conditions container
            unknowns:
                altitude : array
                    Altitude profile [m]

    **Calculation Process**
    1. Compute atmospheric properties at altitude
    2. Calculate true airspeed from dynamic pressure:
       V = sqrt(2q/ρ) where:
       - q is dynamic pressure
       - ρ is air density
    3. Decompose velocity into components using climb angle

    **Major Assumptions**
    * Constant dynamic pressure
    * Fixed climb angle
    * Standard atmosphere model
    * Small angle approximations
    * Quasi-steady flight

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.frames.inertial.velocity_vector [m/s]
        - conditions.frames.inertial.position_vector [m]
        - conditions.freestream.altitude [m]

    See Also
    --------
    RCAIDE.Framework.Mission.Segments
    RCAIDE.Library.Mission.Common.Update.atmosphere
    """
    
    # unpack
    climb_angle = segment.climb_angle
    q           = segment.dynamic_pressure
    alt0        = segment.altitude_start  
    conditions  = segment.state.conditions
    beta        = segment.sideslip_angle
    rho         = conditions.freestream.density[:,0]  
    
    # unpack unknowns  
    alts     = conditions.frames.inertial.position_vector[:,2]

    # Update freestream to get density
    RCAIDE.Library.Mission.Common.Update.atmosphere(segment)
    rho = conditions.freestream.density[:,0]   

    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 * segment.state.initials.conditions.frames.inertial.position_vector[-1,2]
    
    # pack conditions    
    conditions.freestream.altitude[:,0] =  -alts  # positive altitude in this context    
    

    # check for initial velocity
    if q is None: 
        if not segment.state.initials: raise AttributeError('dynamic pressure not set')
        v_mag = np.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1])
    else: 
        # Update freestream to get density
        RCAIDE.Library.Mission.Common.Update.atmosphere(segment)
        rho = conditions.freestream.density[:,0]       
    
        # process velocity vector
        v_mag = np.sqrt(2*q/rho)
        
    v_x   = np.cos(beta)*v_mag * np.cos(climb_angle)
    v_y   = np.sin(beta)*v_mag * np.cos(climb_angle)
    v_z   = -v_mag * np.sin(climb_angle)
    
    # pack conditions    
    conditions.frames.inertial.velocity_vector[:,0] = v_x
    conditions.frames.inertial.velocity_vector[:,1] = v_y
    conditions.frames.inertial.velocity_vector[:,2] = v_z   
    
def residual_altitude(segment):
    """
    Computes the altitude residual for solver iteration

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function calculates the difference between the solver's altitude guess
    and the actual altitude computed from segment conditions. The residual is
    normalized by the final altitude.

    **Required Segment Components**

    segment.state:
        unknowns:
            altitude : array
                Solver's altitude guess [m]
        conditions.freestream:
            altitude : array
                Computed altitude [m]

    Returns
    -------
    None
        Updates segment residuals directly:
        - residuals.altitude : array
            Normalized altitude error [-]
    """
    
    # Unpack results 
    alt_in  = segment.state.unknowns.altitude[:,0] 
    alt_out = segment.state.conditions.freestream.altitude[:,0]  
    segment.state.residuals.altitude[:,0] = (alt_in - alt_out)/alt_out[-1]

    return


# ----------------------------------------------------------------------------------------------------------------------  
# Update Differentials
# ----------------------------------------------------------------------------------------------------------------------     
def update_differentials(segment):
    """
    Updates time derivatives and integration for altitude-based discretization

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function handles the time integration for segments discretized in altitude.
    It scales the differentiation and integration operators based on the vertical
    velocity profile.

    **Required Segment Components**

    segment:
        state:
            numerics:
                dimensionless:
                    - control_points : array
                        Discretization points [-]
                    - differentiate : array
                        Differentiation operator
                    - integrate : array
                        Integration operator
            conditions:
                frames.inertial:
                    - position_vector : array
                        Position vector [m]
                    - velocity_vector : array
                        Velocity vector [m/s]
                    - time : array
                        Time vector [s]

    **Process Flow**
    1. Calculate time step from altitude change and vertical velocity
    2. Scale operators by time step
    3. Integrate altitude profile
    4. Update time vector

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.frames.inertial.time [s]
        - conditions.frames.inertial.position_vector [m]
        - conditions.freestream.altitude [m]
    """    

    # unpack
    numerics   = segment.state.numerics
    conditions = segment.state.conditions
    x          = numerics.dimensionless.control_points
    D          = numerics.dimensionless.differentiate
    I          = numerics.dimensionless.integrate 
    r          = segment.state.conditions.frames.inertial.position_vector
    v          = segment.state.conditions.frames.inertial.velocity_vector
    alt0       = segment.altitude_start
    altf       = segment.altitude_end    

    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 * segment.state.initials.conditions.frames.inertial.position_vector[-1,2]
        
    dz = altf - alt0
    vz = -v[:,2,None] # maintain column array

    # get overall time step
    dt = (dz/np.dot(I,vz))[-1]

    # rescale operators
    x = x * dt
    D = D / dt
    I = I * dt
    
    # Calculate the altitudes
    alt = np.dot(I,vz) + alt0
    
    # pack
    t_initial                                       = segment.state.conditions.frames.inertial.time[0,0]
    numerics.time.control_points                    = x
    numerics.time.differentiate                     = D
    numerics.time.integrate                         = I
    conditions.frames.inertial.time[1:,0]            = t_initial + x[1:,0]
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0]  
    conditions.freestream.altitude[:,0]             =  alt[:,0]  

    return