## @ingroup Analyses-Energy
# RCAIDE/Framework/Analyses/Energy/Energy.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports   
from RCAIDE.Framework.Analyses import Analysis 

# ----------------------------------------------------------------------------------------------------------------------
#  ANALYSIS
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Analyses-Energy
class Energy(Analysis):
    """ RCAIDE.Framework.Analyses.Energy.Energy()
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
        self.tag      = 'energy'
        self.networks = None
        
    def evaluate_thrust(self,state):
        
        """Evaluate the thrust produced by the energy network.
    
                Assumptions:
                Network has an "evaluate_thrust" method.
    
                Source:
                N/A
    
                Inputs:
                State data container
    
                Outputs:
                Results of the thrust evaluation method.
    
                Properties Used:
                N/A                
            """
                
            
        networks = self.networks
        results  = networks.evaluate_thrust(state) 
        
        return results
    