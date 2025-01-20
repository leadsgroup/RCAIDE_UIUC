# RCAIDE/Library/Mission/Solver/converge_root.py
# 
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# Package imports 
import scipy.optimize
import numpy as np
import  sys

# ----------------------------------------------------------------------------------------------------------------------
# converge root
# ---------------------------------------------------------------------------------------------------------------------- 
def converge_root(segment):
    """
    Interfaces mission segment with numerical root-finding solver

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function provides an interface between mission segments and numerical 
    root-finding algorithms to solve for unknown variables that satisfy segment
    constraints.

    **Required Segment Components**

    segment:
        - state:
            numerics:
                tolerance_solution : float
                    Convergence tolerance [-]
                max_evaluations : int
                    Maximum function evaluations
                step_size : float
                    Finite difference step size
            unknowns : Data
                Unknown variables to solve for
        - settings:
            root_finder : function, optional
                Root-finding algorithm (defaults to scipy.optimize.fsolve)

    **Calculation Process**
    1. Pack unknown variables into array
    2. Call root-finding algorithm with:
       - Iteration function
       - Initial unknowns guess
       - Convergence parameters
    3. Check convergence status
    4. Update segment convergence flag

    **Major Assumptions**
    * Problem is well-posed for root-finding
    * Residuals are continuous
    * Solution exists within bounds
    * Gradients are well-behaved

    Returns
    -------
    None
        Updates segment state directly:
        - state.numerics.converged [bool]
        - segment.converged [bool]

    See Also
    --------
    iterate
    scipy.optimize.fsolve
    """       
    
    unknowns = segment.state.unknowns.pack_array()
    
    try:
        root_finder = segment.settings.root_finder
    except AttributeError:
        root_finder = scipy.optimize.fsolve 
    
    unknowns,infodict,ier,msg = root_finder( iterate,
                                         unknowns,
                                         args = segment,
                                         xtol = segment.state.numerics.tolerance_solution,
                                         maxfev = segment.state.numerics.max_evaluations,
                                         epsfcn = segment.state.numerics.step_size,
                                         full_output = 1)
    
    if ier!=1:
        print("Segment did not converge. Segment Tag: " + segment.tag)
        print("Error Message:\n" + msg)
        segment.state.numerics.converged = False
        segment.converged = False
    else:
        segment.state.numerics.converged = True
        segment.converged = True
                            
    return
    
# ---------------------------------------------------------------------------------------------------------------------- 
#  Helper Functions
# ---------------------------------------------------------------------------------------------------------------------- 
def iterate(unknowns, segment):
    """
    Performs one iteration of segment analysis

    Parameters
    ----------
    unknowns : array_like
        Current values of unknown variables
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function executes one complete iteration of the segment analysis process,
    updating the segment state with current unknowns and computing residuals.

    **Required Segment Components**

    segment:
        - state:
            unknowns : Data
                Container for unknown variables
            residuals : Data
                Container for constraint residuals
        - process:
            iterate : function
                Segment iteration process

    **Calculation Process**
    1. Unpack unknowns into segment state
    2. Execute segment iteration process
    3. Pack residuals into array

    Returns
    -------
    residuals : ndarray
        Array of constraint residuals

    See Also
    --------
    converge_root
    """       
    if isinstance(unknowns,np.ndarray):
        segment.state.unknowns.unpack_array(unknowns)
    else:
        segment.state.unknowns = unknowns
        
    segment.process.iterate(segment)
    
    residuals = segment.state.residuals.pack_array()
        
    return residuals 