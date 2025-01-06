
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
from   RCAIDE import  * 
from   RCAIDE.Framework.Core import Units
import numpy as np

# ----------------------------------------------------------------------
#  compute_slat_lift
# ----------------------------------------------------------------------

def compute_slat_lift(slat_angle,sweep_angle):
    """Computes the increase in lift due to slats

    Assumptions:
    None

    Source:
    adg.stanford.edu (Stanford AA241 A/B Course Notes)

    Inputs:
    slat_angle   [radians]
    sweep_angle  [radians]

    Outputs:
    dcl_slat     [Unitless]

    Properties Used:
    N/A
    """     

    # unpack
    sa = slat_angle  / Units.deg
    sw = sweep_angle

    # AA241 Method from adg.stanford.edu
    dcl_slat = (sa/23.)*(np.cos(sw))**1.4 * np.cos(sa * Units.deg)**2

    #returning dcl_slat
    return dcl_slat
 