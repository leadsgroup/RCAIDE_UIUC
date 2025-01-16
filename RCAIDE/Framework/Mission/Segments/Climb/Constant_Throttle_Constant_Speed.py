# RCAIDE/Framework/Mission/Segments/Climb/Constant_Throttle_Constant_Speed.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core                       import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate  import Evaluate
from RCAIDE.Framework.Mission.Segments.Cruise    import Constant_Throttle_Constant_Altitude
from RCAIDE.Library.Mission                      import Common,Segments
from RCAIDE.Framework.Analyses                   import Process  

# ----------------------------------------------------------------------------------------------------------------------
# Constant_Throttle_Constant_Speed
# ---------------------------------------------------------------------------------------------------------------------- 
 
class Constant_Throttle_Constant_Speed(Evaluate):
    """
    Mission segment for climbing at constant throttle setting and true airspeed

    Attributes
    ----------
    altitude_start : float
        Initial altitude [m], optional
    altitude_end : float
        Final altitude [m], defaults to 10 km
    throttle : float
        Throttle setting [-], defaults to 0.5
    air_speed : float
        True airspeed to maintain [m/s]
    true_course : float
        True course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment maintains constant throttle and true airspeed while climbing.
    The climb rate is determined by available excess thrust. This segment may
    not always converge if insufficient thrust is available at the specified
    throttle setting. Useful for evaluating climb performance at top of climb.

    The segment processes include extensive condition updates:
    - Velocity vector from wind angle
    - Body angle unpacking
    - Altitude differentials
    - Time differentials
    - Orientations
    - Acceleration
    - Atmosphere
    - Gravity
    - Freestream conditions
    - Energy/thrust
    - Aerodynamics
    - Stability
    - Weights
    - Forces and moments
    - Planet position

    **Major Assumptions**
    * Throttle setting provides sufficient thrust for climb
    * Quasi-steady flight
    * Standard atmosphere
    * No wind effects
    * Thrust available exceeds drag at specified conditions

    **Process Flow**
    
    Initialize:
    - conditions

    Iterate:
    - Update all conditions (velocities through moments)
    - Evaluate flight dynamics residuals

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Evaluate
    RCAIDE.Framework.Mission.Common
    """
    
    def __defaults__(self):
        """
        Sets default values for segment parameters

        Notes
        -----
        Initializes segment with default values and sets up extensive process flow
        for condition updates. Called automatically when segment is instantiated.

        The process flow defines a comprehensive update sequence for all flight
        conditions and states during the climb.
        """          
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start    = None # Optional
        self.altitude_end      = 10. * Units.km
        self.throttle          = 0.5
        self.air_speed         = None
        self.true_course       = 0.0 * Units.degrees       

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------      
        initialize                         = self.process.initialize   
        initialize.conditions              = Segments.Climb.Constant_Throttle_Constant_Speed.initialize_conditions 
        
        iterate                            = self.process.iterate 
         
        # Update Conditions
        iterate.conditions = Process()
        iterate.conditions.velocities                 = Segments.Climb.Constant_Throttle_Constant_Speed.update_velocity_vector_from_wind_angle 
        iterate.conditions.angles                     = Segments.Climb.Constant_Throttle_Constant_Speed.unpack_body_angle  
        iterate.conditions.differentials_altitude     = Segments.Climb.Constant_Throttle_Constant_Speed.update_differentials_altitude  
        iterate.conditions.differentials              = Common.Update.differentials_time 
        iterate.conditions.orientations               = Common.Update.orientations   
        iterate.conditions.acceleration               = Common.Update.acceleration          
        iterate.conditions.atmosphere                 = Common.Update.atmosphere
        iterate.conditions.gravity                    = Common.Update.gravity
        iterate.conditions.freestream                 = Common.Update.freestream 
        iterate.conditions.energy                     = Common.Update.thrust
        iterate.conditions.aerodynamics               = Common.Update.aerodynamics
        iterate.conditions.stability                  = Common.Update.stability
        iterate.conditions.weights                    = Common.Update.weights
        iterate.conditions.forces                     = Common.Update.forces
        iterate.conditions.moments                    = Common.Update.moments
        iterate.conditions.planet_position            = Common.Update.planet_position
        iterate.residuals.flight_dynamics             = Common.Residuals.flight_dynamics 
        
        return

