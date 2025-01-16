# RCAIDE/Framework/Mission/Segments/Cruise/Constant_Throttle_Constant_Altitude.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Framework.Mission.Segments.Evaluate  import Evaluate 
from RCAIDE.Framework.Core                       import Units   
from RCAIDE.Library.Mission                      import Common,Segments
from RCAIDE.Framework.Analyses                   import Process  

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Throttle_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------  

class Constant_Throttle_Constant_Altitude(Evaluate):
    """
    Mission segment for level acceleration at constant throttle and altitude

    Attributes
    ----------
    throttle : float
        Throttle setting [-], required
    altitude : float
        Constant altitude to maintain [m], required
    air_speed_start : float
        Initial true airspeed [m/s], required
    air_speed_end : float
        Final true airspeed [m/s], defaults to 0.0
    true_course : float
        True course angle [rad], defaults to 0 degrees

    state.residuals.final_velocity_error : float
        Error in final velocity constraint

    Notes
    -----
    This segment maintains constant altitude and throttle setting while allowing
    the vehicle to accelerate. Useful for level acceleration performance analysis.
    The segment duration is determined by the time required to reach the target
    airspeed at the specified throttle setting.

    The segment processes include extensive condition updates:
    - Time differentials
    - Velocity integration
    - Orientations and accelerations
    - Atmosphere and gravity
    - Energy and thrust
    - Aerodynamics and stability
    - Forces and moments
    - Planet position

    **Major Assumptions**
    * Standard atmosphere
    * Quasi-steady flight
    * No wind effects
    * Sufficient control authority
    * Altitude maintainable during acceleration
    * Target speed achievable at specified throttle

    **Process Flow**
    
    Initialize:
    - conditions (constant throttle cruise)

    Iterate:
    - Update all conditions (differentials through moments)
    - Evaluate flight dynamics residuals
    - Solve velocity constraints
    - Update orientation and acceleration unknowns

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Evaluate
    RCAIDE.Framework.Mission.Common
    RCAIDE.Library.Mission.Segments.Cruise
    """
    
    
    # ------------------------------------------------------------------
    #   Data Defaults
    # ------------------------------------------------------------------  

    def __defaults__(self):
        """
        Sets default values for segment parameters

        Notes
        -----
        Initializes segment with default values and sets up extensive process flow
        for condition updates. Called automatically when segment is instantiated.

        The process flow defines a comprehensive update sequence for all flight
        conditions and states during the acceleration maneuver.
        """           
        
        # -------------------------------------------------------------------------------------------------------------- 
        # User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.throttle          = None
        self.altitude          = None
        self.air_speed_start   = None
        self.air_speed_end     = 0.0 
        self.true_course       = 0.0 * Units.degrees  

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission Specific Unknowns and Residuals 
        # --------------------------------------------------------------------------------------------------------------  
        self.state.residuals.final_velocity_error = 0.0
     
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------    
        initialize                         = self.process.initialize  
        initialize.conditions              = Segments.Cruise.Constant_Throttle_Constant_Altitude.initialize_conditions      
        iterate                            = self.process.iterate             

        # Update Conditions
        iterate.conditions = Process()
        iterate.conditions.differentials         = Common.Update.differentials_time 
        iterate.conditions.velocity              = Segments.Cruise.Constant_Throttle_Constant_Altitude.integrate_velocity 
        iterate.conditions.orientations          = Common.Update.orientations    
        iterate.conditions.acceleration          = Common.Update.acceleration 
        iterate.conditions.angular_acceleration  = Common.Update.angular_acceleration  
        iterate.conditions.altitude              = Common.Update.altitude
        iterate.conditions.atmosphere            = Common.Update.atmosphere
        iterate.conditions.gravity               = Common.Update.gravity
        iterate.conditions.freestream            = Common.Update.freestream
        iterate.conditions.energy                = Common.Update.thrust
        iterate.conditions.aerodynamics          = Common.Update.aerodynamics
        iterate.conditions.stability             = Common.Update.stability
        iterate.conditions.weights               = Common.Update.weights
        iterate.conditions.forces                = Common.Update.forces
        iterate.conditions.moments               = Common.Update.moments
        iterate.conditions.planet_position       = Common.Update.planet_position
        iterate.residuals.flight_dynamics        = Common.Residuals.flight_dynamics
        iterate.residuals.velocity               = Segments.Cruise.Constant_Throttle_Constant_Altitude.solve_velocity
        iterate.unknowns.mission                 = Common.Unpack_Unknowns.orientation  
        iterate.unknowns.acceleration            = Segments.Cruise.Constant_Throttle_Constant_Altitude.unpack_unknowns  

        return