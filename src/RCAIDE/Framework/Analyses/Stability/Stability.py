 
from RCAIDE.Framework.Core import Data
from RCAIDE.Framework.Analyses import Analysis


# ----------------------------------------------------------------------
#  Analysis
# ---------------------------------------------------------------------- 
class Stability(Analysis):
    """This is the base class for stability analyses. It contains functions
    that are built into the default class.
    
    Assumptions:
    None
    
    Source:
    N/A
    """
     
    def __defaults__(self):
        """This sets the default values and methods for the analysis.         

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
        self.tag      = 'stability'
        self.vehicle  = Data()
        self.settings = Data()
 
        return


