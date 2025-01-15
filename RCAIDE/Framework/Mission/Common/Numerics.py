# RCAIDE/Framework/Analyses/Mission/Segments/Conditions/Numerics.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .Conditions import Conditions 
from RCAIDE.Library.Methods.Utilities.Chebyshev  import chebyshev_data 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Numerics
# ----------------------------------------------------------------------------------------------------------------------

class Numerics(Conditions):
    """
    Data structure for numerical solving parameters in mission analysis

    Attributes
    ----------
    tag : str
        Identifier, defaults to 'numerics'
    number_of_control_points : int
        Number of points for discretization, defaults to 16
    discretization_method : callable
        Function to generate discretization points, defaults to chebyshev_data
    solver_jacobian : str
        Type of jacobian to use, defaults to "none"
    tolerance_solution : float
        Convergence tolerance, defaults to 1e-8
    converged : bool or None
        Whether solution has converged
    max_evaluations : float
        Maximum number of function evaluations
    step_size : float or None
        Step size for numerical derivatives

    dimensionless : Conditions
        Dimensionless integration data:
        - control_points : ndarray
            Points for integration
        - differentiate : ndarray
            Differentiation matrix
        - integrate : ndarray
            Integration matrix

    time : Conditions
        Time-based integration data:
        - control_points : ndarray
            Time points
        - differentiate : ndarray
            Time differentiation matrix
        - integrate : ndarray
            Time integration matrix

    Notes
    -----
    This class stores all numerical parameters needed for solving mission segments.
    It inherits from Conditions to provide data structure functionality.

    **Major Assumptions**
    * Discretization method provides required matrices
    * Integration schemes are compatible with solver
    * Control points are properly distributed
    * Time and dimensionless parameters are synchronized

    **Extra modules required**
    * numpy
    * RCAIDE.Library.Methods.Utilities.Chebyshev
    """
    
    def __defaults__(self):
        """
        Sets default values for numerical parameters

        Notes
        -----
        Initializes all numerical parameters with default values.
        Creates empty arrays for integration matrices.
        Called automatically when class is instantiated.
        """           
        self.tag                              = 'numerics' 
        self.number_of_control_points         = 16
        self.discretization_method            = chebyshev_data 
        self.solver_jacobian                  = "none"
        self.tolerance_solution               = 1e-8
        self.converged                        = None
        self.max_evaluations                  = 0.
        self.step_size                        = None
        
        self.dimensionless                    = Conditions()
        self.dimensionless.control_points     = np.empty([0,0])
        self.dimensionless.differentiate      = np.empty([0,0])
        self.dimensionless.integrate          = np.empty([0,0]) 
            
        self.time                             = Conditions()
        self.time.control_points              = np.empty([0,0])
        self.time.differentiate               = np.empty([0,0])
        self.time.integrate                   = np.empty([0,0]) 
        
        
        
        