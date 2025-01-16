# RCAIDE/Framework/Mission/Segments/Single_Point/Set_Speed_Set_Altitude.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Framework.Core                           import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate      import Evaluate
from RCAIDE.Library.Mission                          import Common,Segments
from RCAIDE.Library.Methods.skip                     import skip 

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Set_Speed_Set_Altitude
# ---------------------------------------------------------------------------------------------------------------------- 
class Set_Speed_Set_Altitude(Evaluate):
    """
    Single point mission segment for analysis at fixed speed and altitude

    Attributes
    ----------
    altitude : float
        Flight altitude [m], required
    air_speed : float
        True airspeed [m/s], defaults to 10 km/hr
    distance : float
        Ground distance [m], defaults to 10 km
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
    altitude conditions. It provides a snapshot of the vehicle state and
    performance without time integration. The throttle setting is solved
    to maintain the specified flight conditions.

    The segment processes include:
    - Flight conditions initialization
    - Control surface unpacking
    - Flight dynamics evaluation
    - Basic performance calculations

    **Major Assumptions**
    * Quasi-steady flight
    * Standard atmosphere
    * Rigid aircraft
    * Small angle approximations
    * Sufficient thrust available

    **Process Flow**
    
    Initialize:
    - conditions (speed/altitude)

    Iterate:
    - unknowns.controls (control surfaces)
    - unknowns.mission (orientation)
    - residuals.flight_dynamics

    Post Process:
    - skip (inertial position)

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Evaluate
    RCAIDE.Library.Mission.Common
    RCAIDE.Framework.Mission.Segments.Single_Point.Set_Speed_Set_Altitude_No_Propulsion
    """

    def __defaults__(self):
        """
        Sets default values for segment parameters

        Notes
        -----
        Initializes segment with default values and sets up process flow.
        Called automatically when segment is instantiated.

        The process flow includes basic flight dynamics evaluation at
        the specified flight state.
        """           
        
        # --------------------------------------------------------------------------------------------------------------
        #   User Inputs
        # --------------------------------------------------------------------------------------------------------------
        self.altitude                                = None
        self.air_speed                               = 10. * Units['km/hr']
        self.distance                                = 10. * Units.km
        self.linear_acceleration_x                   = 0.
        self.linear_acceleration_y                   = 0.  
        self.linear_acceleration_z                   = 0. # note that down is positive
        self.roll_rate                               = 0.
        self.pitch_rate                              = 0.  
        self.yaw_rate                                = 0.  
        self.state.numerics.number_of_control_points = 1   
         
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------     
        initialize                               = self.process.initialize 
        initialize.expand_state                  = skip
        initialize.differentials                 = skip
        initialize.conditions                    = Segments.Single_Point.Set_Speed_Set_Altitude.initialize_conditions 
        iterate                                  = self.process.iterate 
        iterate.initials.energy                  = skip
        iterate.unknowns.controls                = Common.Unpack_Unknowns.control_surfaces
        iterate.unknowns.mission                 = Common.Unpack_Unknowns.orientation  
        iterate.conditions.planet_position       = skip    
        iterate.conditions.acceleration          = skip
        iterate.conditions.angular_acceleration  = skip 
        iterate.conditions.weights               = skip
        iterate.residuals.flight_dynamics        = Common.Residuals.flight_dynamics
        post_process                             = self.process.post_process 
        post_process.inertial_position           = skip   
        
                
                
        return

