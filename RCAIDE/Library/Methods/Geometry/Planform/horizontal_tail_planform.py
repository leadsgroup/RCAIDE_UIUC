
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from .wing_planform import wing_planform

# ----------------------------------------------------------------------
#  Methods
# ----------------------------------------------------------------------
def horizontal_tail_planform(Wing):
    """Calls generic wing planform function to compute wing planform values

    Assumptions:
    None

    Source:
    None

    Inputs:
    Wing             [RCAIDE data structure]

    Outputs:
    Changes to Wing (see wing_planform)

    Properties Used:
    N/A
    """   
    wing_planform(Wing)
    
    return 0