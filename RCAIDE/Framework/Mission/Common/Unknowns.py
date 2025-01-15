# RCAIDE/Framework/Analyses/Mission/Segments/Conditions/Unknowns.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from .Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Unknowns
# ----------------------------------------------------------------------------------------------------------------------

class Unknowns(Conditions):
    """
    Data structure for storing variables to be solved in mission segments

    Attributes
    ----------
    tag : str
        Identifier, defaults to 'unknowns'

    Notes
    -----
    This class stores variables that need to be determined during mission
    segment solving. It inherits from Conditions to provide data structure
    functionality.

    The unknowns represent variables that are adjusted by the solver to
    satisfy segment constraints. These typically include control inputs,
    state variables, and other free parameters specific to each segment type.

    **Major Assumptions**
    * Unknown arrays match segment requirements
    * Values are properly scaled for solver
    * Initial guesses are provided where needed
    * Structure matches segment type

    See Also
    --------
    RCAIDE.Framework.Mission.Common.Conditions
    RCAIDE.Framework.Mission.Common.State
    RCAIDE.Framework.Mission.Common.Residuals
    """

    def __defaults__(self):
        """
        Sets default values for unknowns container

        Notes
        -----
        Initializes basic unknowns structure with tag.
        Additional unknown arrays are added based on segment type.
        Called automatically when class is instantiated.

        **Major Assumptions**
        * Specific unknowns defined by segment
        * Arrays sized appropriately for solver
        """
        self.tag = 'unknowns'