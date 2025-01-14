# RCAIDE/Library/Methods/Utilities/Chebyshev/linear_data.py

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np

# ----------------------------------------------------------------------
#  Method
# ---------------------------------------------------------------------- 
def linear_data(N=16, integration=True, **options):
    """
    Calculates differentiation and integration matrices using linearly spaced samples 
    for numerical operations.

    Parameters
    ----------
    N : int, optional
        Number of points for discretization (default: 16)
    integration : bool, optional
        Flag to compute integration operator (default: True)
    **options : dict
        Additional options (reserved for future use)

    Returns
    -------
    x : numpy.ndarray
        Linearly spaced control points in range [0,1]
    D : numpy.ndarray
        Differentiation operator matrix (N x N)
    I : numpy.ndarray or None
        Integration operator matrix (N x N) if integration=True, 
        None otherwise

    Notes
    -----
    Implements a linear spacing variant of the pseudospectral method for numerical 
    differentiation and integration. While potentially less accurate than Chebyshev 
    spacing for some applications, linear spacing can be more intuitive and easier 
    to work with.

    **Theory**
    
    Points are distributed uniformly:
    .. math::
        x_i = i/(N-1)
    
    The differentiation matrix D is constructed using:
    .. math::
        D_{ij} = \\frac{c_i}{c_j} \\frac{(-1)^{i+j}}{x_i - x_j}
    
    where c₀ = cₙ = 2, cᵢ = 1 otherwise

    **Major Assumptions**
        * Function is smooth and well-behaved
        * Domain is normalized to [0,1]
        * Sufficient points for desired accuracy
        * Matrix operations are numerically stable
        * Linear spacing provides adequate resolution

    See Also
    --------
    RCAIDE.Library.Methods.Utilities.Chebyshev.chebyshev_data : Alternative using Chebyshev point distribution
    """           
    
    # setup
    N = int(N)
    if N <= 0: raise RuntimeError("N = %i, must be > 0" % N)
    
    
    # --- X vector
    
    # linear spaced in range [0,1]
    x = np.linspace(0,1,N)   


    # --- Differentiation Operator
    
    # coefficients
    c = np.array( [2.] + [1.]*(N-2) + [2.] )
    c = c * ( (-1.) ** np.arange(0,N) )
    A = np.tile( x, (N,1) ).T
    dA = A - A.T + np.eye( N )
    cinv = 1./c; 

    # build operator
    D = np.zeros( (N,N) );
    
    # math
    c    = np.array(c)
    cinv = np.array([cinv])
    cs   = np.multiply(c,cinv.T)
    D    = np.divide(cs.T,dA)

    # more math
    D = D - np.diag( np.sum( D.T, axis=0 ) );

    # --- Integration operator
    
    if integration:
        # invert D except first row and column
        I = np.linalg.inv(D[1:,1:]); 
        
        # repack missing columns with zeros
        I = np.append(np.zeros((1,N-1)),I,axis=0)
        I = np.append(np.zeros((N,1)),I,axis=1)
        
    else:
        I = None
        
    # done!
    return x, D, I