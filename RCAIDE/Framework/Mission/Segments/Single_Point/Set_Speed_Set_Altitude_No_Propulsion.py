# RCAIDE/Framework/Mission/Segments/Single_Point/Set_Speed_Set_Altitude_No_Propulsion.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Library.Methods                           import skip   
from RCAIDE.Framework.Core                            import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate       import Evaluate
from RCAIDE.Library.Mission                           import Common,Segments
 
# Package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Set_Speed_Set_Altitude_No_Propulsion
# ---------------------------------------------------------------------------------------------------------------------- 
class Set_Speed_Set_Altitude_No_Propulsion(Evaluate):
    """
    Single point mission segment for aerodynamic analysis at fixed speed and altitude without propulsion

    Attributes
    ----------
    temperature_deviation : float
        Temperature offset from standard atmosphere [K], defaults to 0.0
    sideslip_angle : float
        Aircraft sideslip angle [rad], defaults to 0.0
    angle_of_attack : float
        Aircraft angle of attack [rad], required
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
    This segment performs a single-point aerodynamic analysis at specified speed
    and altitude conditions without considering propulsion effects. Useful for
    pure aerodynamic studies and stability analysis.

    The segment processes include:
    - Flight dynamics initialization
    - Atmosphere and freestream conditions
    - Aerodynamic analysis
    - Force and moment calculations
    - Stability derivatives evaluation

    **Major Assumptions**
    * Quasi-steady flow
    * No propulsion effects
    * Rigid aircraft
    * Standard atmosphere (with optional temperature deviation)
    * Small angle approximations
    * Linear aerodynamics

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
    RCAIDE.Framework.Mission.Segments.Single_Point.Set_Speed_Set_Altitude_AVL_Trimmed
    """

    def __defaults__(self):
        """
        Sets default values for segment parameters

        Notes
        -----
        Initializes segment with default values and sets up process flow.
        Called automatically when segment is instantiated.

        The process flow includes aerodynamic analysis without propulsion
        effects at the specified flight state.
        """
        
        # --------------------------------------------------------------------------------------------------------------
        #   User Inputs
        # --------------------------------------------------------------------------------------------------------------
        self.altitude                                = None
        self.air_speed                               = 10. * Units['km/hr']
        self.distance                                = 1.  * Units.km
        self.linear_acceleration_z                   = 0. # note that down is positive
        self.roll_rate                               = 0
        self.pitch_rate                              = 0
        self.yaw_rate                                = 0
        self.state.numerics.number_of_control_points = 1

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------             
        initialize                         = self.process.initialize 
        initialize.expand_state            = skip
        initialize.differentials           = skip
        initialize.conditions              = Segments.Single_Point.Set_Speed_Set_Altitude_No_Propulsion.initialize_conditions 
        iterate                            = self.process.iterate
        iterate.conditions.differentials   = skip 
        iterate.conditions.weights         = Common.Update.weights
        iterate.conditions.planet_position = skip 
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.unknowns.orientation       = Common.Unpack_Unknowns.orientation
        
        return

