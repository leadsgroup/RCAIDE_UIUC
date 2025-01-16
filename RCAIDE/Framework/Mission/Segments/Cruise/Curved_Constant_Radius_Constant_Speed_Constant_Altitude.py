# RCAIDE/Framework/Mission/Segments/Cruise/Curved_Constant_Radius_Constant_Speed_Constant_Altitude.py
# 
# 
# Created:  September 2024, A. Molloy, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Framework.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Framework.Core                        import Units   
from RCAIDE.Library.Mission                       import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Curved_Constant_Radius_Constant_Speed_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------  

class Curved_Constant_Radius_Constant_Speed_Constant_Altitude(Evaluate):
    """
    Mission segment for curved path cruise at constant radius, speed, and altitude

    Attributes
    ----------
    altitude : float
        Constant altitude to maintain [m], required
    air_speed : float
        True airspeed to maintain [m/s], required
    turn_radius : float
        Radius of turn [m], required
    turn_angle : float
        Total angle of turn [rad], defaults to 0 degrees
        Positive for right turn, negative for left turn
    true_course : float
        Initial true course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment maintains constant altitude and airspeed while following a
    curved path of specified radius. The turn direction is determined by the
    sign of the turn angle. The segment distance is determined by the arc
    length of the specified turn angle and radius.

    The segment processes include:
    - Constant altitude/speed conditions initialization
    - Control surface unpacking
    - Flight dynamics residual evaluation
    - Curvilinear position updates

    **Major Assumptions**
    * Standard atmosphere
    * Quasi-steady flight
    * No wind effects
    * Sufficient thrust available
    * Constant altitude maintainable
    * Turn radius achievable at specified speed
    * Coordinated turn (no sideslip)

    **Process Flow**
    
    Initialize:
    - conditions (curved path cruise)

    Iterate:
    - unknowns.mission (orientation)
    - unknowns.controls (control surfaces)
    - residuals.flight_dynamics

    Post Process:
    - inertial_position (curvilinear path)

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Evaluate
    RCAIDE.Framework.Mission.Common
    RCAIDE.Library.Mission.Common.Update.curvilinear_inertial_horizontal_position
    """
    
    def __defaults__(self):
        """
        Sets default values for segment parameters

        Notes
        -----
        Initializes segment with default values and sets up process flow.
        Called automatically when segment is instantiated.

        The process flow defines how the segment is evaluated:
        1. Initialize conditions
        2. Iterate on orientation and flight dynamics
        3. Update curvilinear position
        """           
        
        # -------------------------------------------------------------------------------------------------------------- 
        # User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude          = None
        self.air_speed         = None 
        self.turn_radius       = None
        self.turn_angle        = 0.0 * Units.degrees # + indicated right hand turn, negative indicates left-hand turn defaults to straight flight
        self.true_course       = 0.0 * Units.degrees 

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # -------------------------------------------------------------------------------------------------------------- 
        initialize                         = self.process.initialize  
        initialize.conditions              = Segments.Cruise.Curved_Constant_Radius_Constant_Speed_Constant_Altitude.initialize_conditions  
        iterate                            = self.process.iterate     
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics 
        post_process                       = self.process.post_process 
        post_process.inertial_position     = Common.Update.curvilinear_inertial_horizontal_position
 
        return

