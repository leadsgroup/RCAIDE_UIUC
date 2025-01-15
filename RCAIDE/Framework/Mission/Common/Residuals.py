# RCAIDE/Framework/Analyses/Mission/Segments/Conditions/Residuals.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Residuals
# ----------------------------------------------------------------------------------------------------------------------

class Residuals(Conditions):
    """
    Data structure for storing mission segment residual values

    Attributes
    ----------
    tag : str
        Identifier, defaults to 'residuals'

    Notes
    -----
    This class stores residual values that need to be driven to zero during
    mission segment solving. It inherits from Conditions to provide data
    structure functionality.

    The residuals represent the difference between target values and current
    values for various segment constraints and conditions. These are used by
    the solver to determine convergence.

    **Major Assumptions**
    * Residual arrays match segment unknowns
    * Values are properly scaled for solver
    * Residuals approach zero at solution
    * Structure matches segment type requirements

    See Also
    --------
    RCAIDE.Framework.Mission.Common.Conditions
    RCAIDE.Framework.Mission.Common.State
    RCAIDE.Framework.Mission.Common.Numerics
    """

    def __defaults__(self):
        """
        Sets default values for residuals container

        Notes
        -----
        Initializes basic residuals structure with tag.
        Additional residual arrays are added based on segment type.
        Called automatically when class is instantiated.
        """           
        self.tag      = 'residuals'