# Cubic_Spline_Blender.py
# 
# Created:  Feb 2019, T. MacDonald
# Modified: Jan 2020, T. MacDonald (moved from Method/Aerodynamics/Supersonic_Zero/Drag)

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np

# ----------------------------------------------------------------------
#  Blender Class
# ----------------------------------------------------------------------

class Cubic_Spline_Blender():
    """
    A cubic spline interpolation class for smoothly blending between two calculations 
    or regimes while preserving continuous first derivatives.

    Parameters
    ----------
    x_start : float
        Starting x-coordinate of the blending region
    x_end : float
        Ending x-coordinate of the blending region

    Notes
    -----
    This class implements a cubic Hermite spline to create smooth transitions between 
    different calculation regimes. The blending function has continuous first derivatives 
    and varies smoothly from 1 at x_start to 0 at x_end.

    **Theory**
    The blending is achieved using a cubic polynomial of the form:
    .. math::
        y = 2η³ - 3η² + 1

    where η is the normalized coordinate:
    .. math::
        η = (x - x_start)/(x_end - x_start)

    **Major Assumptions**
        * The transition should be smooth (C¹ continuous)
        * The blending function should be monotonic
        * Values outside the blending region are clamped (1 below x_start, 0 above x_end)

    See Also
    --------
    compute : Method to calculate the blending value at a given x
    eta_transform : Method to calculate the normalized coordinate
    """
    
    def __init__(self, x_start, x_end):
        """This sets the default start and end position.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """           
        self.x_start = x_start
        self.x_end   = x_end
    
    
    def compute(self,x):
        """
        Computes the blending coefficient at a given x-coordinate.

        Parameters
        ----------
        x : float or array_like
            The x-coordinate(s) at which to compute the blending coefficient

        Returns
        -------
        y : float or array_like
            The blending coefficient(s) at x. Values are clamped to [0,1]
        """          
        eta = self.eta_transform(x)
    
        y = 2*eta*eta*eta-3*eta*eta+1
        y[eta<0] = 1
        y[eta>1] = 0
        return y

    def eta_transform(self,x):
        """
        Transforms x-coordinates to normalized coordinates η, eta.

        Parameters
        ----------
        x : float or array_like
            The x-coordinate(s) to transform

        Returns
        -------
        eta : float or array_like
            The normalized coordinate(s) η = (x - x_start)/(x_end - x_start)
        """          
        x_start = self.x_start
        x_end   = self.x_end
        
        eta     = (x-x_start)/(x_end-x_start)
        
        return eta