# RCAIDE/Framework/Mission/Segments/Single_Point/Set_Speed_Set_Altitude_AVL_Trimmed.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Framework.Core                           import Units  
from RCAIDE.Framework.Mission.Segments               import Segment
from RCAIDE.Framework.Mission.Common.Results         import Results
from RCAIDE.Library.Mission                          import Common , Segments
from RCAIDE.Framework.Analyses                       import Process   
from RCAIDE.Library.Mission                          import Common,Segments
from RCAIDE.Library.Methods.skip                     import skip 

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Set_Speed_Set_Altitude
# ---------------------------------------------------------------------------------------------------------------------- 
class Set_Speed_Set_Altitude_AVL_Trimmed(Segment):
    """
    Single point mission segment for AVL trim analysis at fixed speed and altitude

    Attributes
    ----------
    temperature_deviation : float
        Temperature offset from standard atmosphere [K], defaults to 0.0
    sideslip_angle : float
        Aircraft sideslip angle [rad], defaults to 0.0
    angle_of_attack : float
        Aircraft angle of attack [rad], required
    trim_lift_coefficient : float
        Target lift coefficient for trim [-], required
    bank_angle : float
        Aircraft bank angle [rad], defaults to 0.0
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
    This segment performs a single-point analysis using AVL (Athena Vortex Lattice)
    to determine trim conditions at a specified speed and altitude. The segment
    solves for control surface deflections and orientation angles to achieve the
    target lift coefficient with zero moments.

    The segment processes include:
    - Flight dynamics and controls initialization
    - Atmosphere and freestream conditions
    - AVL aerodynamic analysis
    - Force and moment calculations
    - Trim residual evaluation

    **Major Assumptions**
    * Quasi-steady flow
    * Linear aerodynamics
    * Small angle approximations
    * No propulsion-aerodynamic interactions
    * Rigid aircraft
    * Standard atmosphere (with optional temperature deviation)

    **Process Flow**
    
    Initialize:
    - differentials (dimensionless)
    - conditions (speed/altitude)

    Iterate:
    - initials (time, weights, position)
    - unknowns (orientation)
    - conditions (atmosphere through moments)
    - residuals (flight dynamics)

    Post Process:
    - noise
    - skip (energy, emissions, position)

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Segment
    RCAIDE.Library.Mission.Common
    RCAIDE.Library.Mission.Segments.Single_Point
    """
    
    def __defaults__(self):
        """
        Sets default values for segment parameters

        Notes
        -----
        Initializes segment with default values and sets up process flow.
        Called automatically when segment is instantiated.

        The process flow includes AVL aerodynamic analysis and trim
        condition evaluation at the specified flight state.
        """           

        
        # --------------------------------------------------------------
        #   State
        # --------------------------------------------------------------
        
        # conditions
        self.temperature_deviation                   = 0.0
        self.sideslip_angle                          = 0.0 
        self.angle_of_attack                         = None
        self.trim_lift_coefficient                   = None        
        self.bank_angle                              = 0.0 
        self.linear_acceleration_x                   = 0.
        self.linear_acceleration_y                   = 0.  
        self.linear_acceleration_z                   = 0. # note that down is positive
        self.roll_rate                               = 0.
        self.pitch_rate                              = 0.  
        self.yaw_rate                                = 0.  
        self.state.numerics.number_of_control_points = 1     
        self.state.conditions.update(Results())
        
        # ---------------------------------------------------------------
        # Define Flight Controls and Residuals 
        # ---------------------------------------------------------------     
        self.flight_dynamics_and_controls()    
        
        # --------------------------------------------------------------
        #   Initialize - before iteration
        # -------------------------------------------------------------- 
        initialize                         = self.process.initialize 
        initialize.expand_state            = skip 
        initialize.differentials           = Common.Initialize.differentials_dimensionless 
        initialize.conditions              = Segments.Single_Point.Set_Speed_Set_Altitude_AVL_Trimmed.initialize_conditions  
        
        # --------------------------------------------------------------          
        #   Iterate  
        # -------------------------------------------------------------- 
        iterate                            = self.process.iterate 
        iterate.initials                   = Process()
        iterate.initials.time              = Common.Initialize.time
        iterate.initials.weights           = Common.Initialize.weights
        iterate.initials.energy            = skip
        iterate.initials.inertial_position = Common.Initialize.inertial_position
        iterate.initials.planet_position   = Common.Initialize.planet_position
        
        
        # Unpack Unknowns
        iterate.unknowns                   = Process()
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation  
        
        # Update Conditions
        iterate.conditions = Process()
        iterate.conditions.differentials         = Common.Update.differentials_time
        iterate.conditions.orientations          = Common.Update.orientations
        iterate.conditions.acceleration          = skip 
        iterate.conditions.angular_acceleration  = skip 
        iterate.conditions.altitude              = Common.Update.altitude
        iterate.conditions.atmosphere            = Common.Update.atmosphere
        iterate.conditions.gravity               = Common.Update.gravity
        iterate.conditions.freestream            = Common.Update.freestream 
        iterate.conditions.thrust                = Common.Update.thrust
        iterate.conditions.aerodynamics          = Common.Update.aerodynamics
        iterate.conditions.stability             = Common.Update.stability
        iterate.conditions.weights               = skip # Common.Update.weights
        iterate.conditions.forces                = Common.Update.forces
        iterate.conditions.moments               = Common.Update.moments
        iterate.conditions.planet_position       = skip

        # Solve Residuals 
        #iterate.unknowns.controls                = Common.Unpack_Unknowns.control_surfaces
        #iterate.unknowns.mission                 = Common.Unpack_Unknowns.orientation  
        iterate.residuals.flight_dynamics        = Common.Residuals.flight_dynamics

        # --------------------------------------------------------------  
        #  Post Process   
        # -------------------------------------------------------------- 
        post_process                    = self.process.post_process   
        post_process.inertial_position  = skip
        post_process.energy             = skip
        post_process.noise              = Common.Update.noise
        post_process.emissions          = skip 
                
        return

