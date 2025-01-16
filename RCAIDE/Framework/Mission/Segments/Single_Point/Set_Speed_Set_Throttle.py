# RCAIDE/Framework/Mission/Segments/Single_Point/Set_Speed_Set_Throttle.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports   
from RCAIDE.Library.Methods.skip                      import skip 
from RCAIDE.Framework.Core                            import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate       import Evaluate
from RCAIDE.Library.Mission                           import Common,Segments

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Set_Speed_Set_Throttle
# ---------------------------------------------------------------------------------------------------------------------- 
class Set_Speed_Set_Throttle(Evaluate):
    """
    Single point mission segment for analysis at fixed speed and throttle setting

    Attributes
    ----------
    altitude : float
        Flight altitude [m], required
    air_speed : float
        True airspeed [m/s], defaults to 10 km/hr
    throttle : float
        Engine throttle setting [-], defaults to 1.0
    linear_acceleration_x : float
        Body-axis x acceleration [m/s^2], defaults to 0.0
    linear_acceleration_y : float
        Body-axis y acceleration [m/s^2], defaults to 0.0
    linear_acceleration_z : float
        Body-axis z acceleration [m/s^2], defaults to 0.0 (positive down)
    roll_rate : float
        Body-axis roll rate [rad/s], defaults to 0.0
    pitch_rate : float
        Body-axis pitch rate [rad/s], defaults to 0.0
    yaw_rate : float
        Body-axis yaw rate [rad/s], defaults to 0.0
    state.numerics.number_of_control_points : int
        Number of analysis points, defaults to 1

    Notes
    -----
    This segment performs a single-point analysis at specified speed and
    throttle conditions. It provides a snapshot of the vehicle state and
    performance without time integration. The acceleration is solved based
    on the fixed throttle setting and flight conditions.

    The segment processes include:
    - Flight conditions initialization
    - Control surface unpacking
    - Orientation unpacking
    - Acceleration unpacking
    - Flight dynamics evaluation

    **Major Assumptions**
    * Quasi-steady flight
    * Standard atmosphere
    * Rigid aircraft
    * Small angle approximations
    * Fixed throttle setting
    * No thrust transients

    **Process Flow**
    
    Initialize:
    - conditions (speed/throttle)

    Iterate:
    - unknowns.controls (control surfaces)
    - unknowns.orientation
    - unknowns.acceleration
    - residuals.flight_dynamics

    Post Process:
    - skip (inertial position)

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Evaluate
    RCAIDE.Library.Mission.Common
    RCAIDE.Framework.Mission.Segments.Single_Point.Set_Speed_Set_Altitude
    """

    def __defaults__(self):
        """
        Sets default values for segment parameters

        Notes
        -----
        Initializes segment with default values and sets up process flow.
        Called automatically when segment is instantiated.

        The process flow includes acceleration calculation and flight
        dynamics evaluation at the specified throttle setting.
        """
        
        # --------------------------------------------------------------------------------------------------------------
        #   User Inputs
        # --------------------------------------------------------------------------------------------------------------
        self.altitude                                = None
        self.air_speed                               = 10. * Units['km/hr']
        self.throttle                                = 1.
        self.linear_acceleration_x                   = 0.  
        self.linear_acceleration_y                   = 0.  
        self.linear_acceleration_z                   = 0. # note that down is positive 
        self.roll_rate                               = 0
        self.pitch_rate                              = 0
        self.yaw_rate                                = 0  
        self.state.numerics.number_of_control_points = 1  

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------             
        initialize                               = self.process.initialize 
        initialize.expand_state                  = skip
        initialize.differentials                 = skip
        initialize.conditions                    = Segments.Single_Point.Set_Speed_Set_Throttle.initialize_conditions 
        iterate                                  = self.process.iterate 
        iterate.initials.energy                  = skip    
        iterate.unknowns.controls                = Common.Unpack_Unknowns.control_surfaces
        iterate.unknowns.orientation             = Common.Unpack_Unknowns.orientation 
        iterate.unknowns.acceleration            = Segments.Single_Point.Set_Speed_Set_Throttle.unpack_unknowns  
        iterate.conditions.differentials         = skip 
        iterate.conditions.planet_position       = skip    
        iterate.conditions.acceleration          = skip
        iterate.conditions.angular_acceleration  = skip 
        iterate.conditions.weights               = skip 
        iterate.residuals.flight_dynamics        = Common.Residuals.flight_dynamics
        post_process                             = self.process.post_process 
        post_process.inertial_position           = skip    
                
                
        return

