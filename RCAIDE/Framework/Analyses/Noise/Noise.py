## @ingroup Analyses-Noise
# RCAIDE/Framework/Analyses/Noise/Noise.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

from RCAIDE.Framework.Core import Data
from RCAIDE.Framework.Analyses import Analysis

# ----------------------------------------------------------------------
#  Noise
# ----------------------------------------------------------------------
## @ingroup Analyses-Noise
class Noise(Analysis):
    """ RCAIDE.Framework.Analyses.Noise.Noise()
    
        The Top Level Noise Analysis Class
        
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
        self.tag    = 'Noise'        
  
        self.geometry = Data()
        self.settings = Data()
        
        
    def evaluate(self,state):
        """The default evaluate function.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        results   <Results class> (empty)

        Properties Used:
        N/A
        """           
        
        results = Data()
        
        return results 