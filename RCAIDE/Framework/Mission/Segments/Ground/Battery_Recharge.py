# RCAIDE/Framework/Mission/Segments/Ground/Battery_Charge.py 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Framework.Mission.Segments.Evaluate      import Evaluate
from RCAIDE.Library.Mission.Segments                 import Ground   
from RCAIDE.Framework.Core                           import Units
from RCAIDE.Library.Methods.skip                     import skip 

# ----------------------------------------------------------------------------------------------------------------------
#  SEGMENT
# ---------------------------------------------------------------------------------------------------------------------- 
class Battery_Recharge(Evaluate): 
    """
    Mission segment for recharging battery while vehicle is on ground

    Attributes
    ----------
    altitude : float
        Ground altitude [m], required
    overcharge_contingency : float
        Safety factor for charge capacity, defaults to 1.10
    cutoff_SOC : float
        Target state of charge ratio, defaults to 1.0 (full charge)
    true_course : float
        True course angle [rad], defaults to 0 degrees
    cooling_time : float
        Additional time for battery cooling [hr], defaults to 0.0 hr

    Notes
    -----
    This segment simulates battery recharging while the vehicle is stationary
    on the ground. Useful for between-flight charging operations. Aerodynamic
    and stability calculations are skipped since the vehicle is stationary.

    The segment processes include:
    - Ground battery charging conditions initialization
    - Energy state tracking
    - Battery thermal management
    - Charge cutoff monitoring

    **Major Assumptions**
    * Vehicle is stationary
    * No aerodynamic forces
    * Constant charge rate
    * Battery thermal limits maintained
    * Ground charging equipment available
    * Sufficient power supply available

    **Process Flow**
    
    Initialize:
    - conditions (battery charge)

    Iterate:
    - unknowns.mission (skipped)
    - conditions.aerodynamics (skipped)
    - conditions.stability (skipped)

    Post Process:
    - noise (skipped)
    - emissions (skipped)

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Evaluate
    RCAIDE.Library.Mission.Segments.Ground
    RCAIDE.Framework.Mission.Segments.Ground.Battery_Discharge
    """

    # ------------------------------------------------------------------
    #   Data Defaults
    # ------------------------------------------------------------------  

    def __defaults__(self):  
        """
        Sets default values for segment parameters

        Notes
        -----
        Initializes segment with default values and sets up process flow.
        Called automatically when segment is instantiated.

        The process flow skips aerodynamic and stability calculations since
        the vehicle is stationary on the ground.
        """              
        
        # --------------------------------------------------------------
        #   User Inputs
        # --------------------------------------------------------------
        self.altitude                      = None 
        self.overcharge_contingency        = 1.10
        self.cutoff_SOC                    = 1.0
        self.true_course                   = 0.0 * Units.degrees  
        self.cooling_time                  = 0.0 * Units.hr
         
        initialize                         = self.process.initialize  
        initialize.conditions              = Ground.Battery_Charge_Discharge.initialize_conditions  
        iterate                            = self.process.iterate 
        iterate.unknowns.mission           = skip
        iterate.conditions.aerodynamics    = skip
        iterate.conditions.stability       = skip  
        post_process                       = self.process.post_process  
        post_process.noise                 = skip
        post_process.emissions             = skip
        
        return
