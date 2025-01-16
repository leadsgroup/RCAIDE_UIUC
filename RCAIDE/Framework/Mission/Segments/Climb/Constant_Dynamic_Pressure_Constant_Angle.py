# RCAIDE/Framework/Mission/Segments/Climb/Constant_Dynamic_Pressure_Constant_Angle.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Framework.Core                                     import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate       import Evaluate
from RCAIDE.Library.Mission                          import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
# Constant_Dynamic_Pressure_Constant_Angle
# ---------------------------------------------------------------------------------------------------------------------- 
 
class Constant_Dynamic_Pressure_Constant_Angle(Evaluate):
    """
    Mission segment for climbing at constant dynamic pressure and angle

    Attributes
    ----------
    altitude_start : float
        Initial altitude [m], optional
    altitude_end : float
        Final altitude [m], defaults to 10 km
    climb_angle : float
        Climb angle [rad], defaults to 3 degrees
    dynamic_pressure : float
        Dynamic pressure to maintain [Pa]
    true_course : float
        True course angle [rad], defaults to 0 degrees

    state.residuals.altitude : ndarray
        Altitude constraint residual
    state.unknowns.altitude : ndarray
        Altitude values to be solved

    Notes
    -----
    This segment maintains constant dynamic pressure while climbing at a fixed angle.
    It requires additional computation time due to extra unknowns and residuals for
    maintaining dynamic pressure.

    The segment processes include:
    - Conditions and unknowns initialization
    - Orientation and control surface updates
    - Kinematics calculations
    - Differential updates
    - Flight dynamics and altitude residual evaluation

    **Major Assumptions**
    * Standard atmosphere
    * Quasi-steady flight
    * No wind effects
    * Dynamic pressure achievable throughout climb

    **Process Flow**
    
    Initialize:
    - conditions and unknowns

    Iterate:
    - unknowns.mission (orientation)
    - unknowns.controls (control surfaces)
    - unknowns.kinematics
    - conditions.differentials
    - residuals.flight_dynamics
    - residuals.altitude

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
        Initializes segment with default values and sets up process flow.
        Called automatically when segment is instantiated.

        The process flow defines how the segment is evaluated:
        1. Initialize conditions and unknowns
        2. Iterate on orientation, controls, kinematics
        3. Update differentials
        4. Evaluate flight dynamics and altitude residuals
        """
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start            = None # Optional
        self.altitude_end              = 10.  * Units.km
        self.climb_angle               = 3.   * Units.degrees
        self.dynamic_pressure          = None
        self.true_course               = 0.0 * Units.degrees
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission Specific Unknowns and Residuals 
        # --------------------------------------------------------------------------------------------------------------    
        ones_row = self.state.ones_row             
        self.state.residuals.altitude      = ones_row(1) * 0.0
        self.state.unknowns.altitude       = ones_row(1) * 0.0                                         
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize
        initialize.conditions              = Segments.Climb.Constant_Dynamic_Pressure_Constant_Angle.initialize_conditions_unpack_unknowns 
        iterate                            = self.process.iterate 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.unknowns.kinematics        = Segments.Climb.Constant_Dynamic_Pressure_Constant_Angle.initialize_conditions_unpack_unknowns
        iterate.conditions.differentials   = Segments.Climb.Constant_Dynamic_Pressure_Constant_Angle.update_differentials 
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        iterate.residuals.altitude         = Segments.Climb.Constant_Dynamic_Pressure_Constant_Angle.residual_altitude
        return
       