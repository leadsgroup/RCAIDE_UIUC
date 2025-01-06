# TRMM_setup.py
#
# Created:  Apr 2017, T. MacDonald
# Modified: 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from RCAIDE.Framework.Optimization.Packages.trmm import Trust_Region_Optimization as tro
from RCAIDE.Framework.Optimization.Packages.trmm.Trust_Region import Trust_Region

# ----------------------------------------------------------------------
#  TRMM_Solve
# ----------------------------------------------------------------------

def TRMM_Solve(problem,tr=None,tr_opt=None,print_output=False):
    """ This solves your TRMM

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        problem       [nexus()]
        tr            [Trust_Region()]
        tr_opt        [Trust_Region_Optimization()]
        print_output  [bool]

        Outputs:
        None

        Properties Used:
        None
        """     

    if tr == None:
        tr = Trust_Region()
    problem.trust_region = tr
    if tr_opt == None:
        TRM_opt = tro.Trust_Region_Optimization()
    else:
        TRM_opt = tr_opt
    TRM_opt.optimize(problem,print_output=print_output)

    return
