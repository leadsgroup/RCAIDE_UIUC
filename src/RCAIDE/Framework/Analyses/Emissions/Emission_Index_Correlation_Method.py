# RCAIDE/Framework/Analyses/Emissions/Emission_Index_Correlation_Method.py
#  
# Created:  Jul 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Framework.Analyses    import Process 
from RCAIDE.Library.Methods.Emissions.Emission_Index_Empirical_Method import *  
from .Emissions            import Emissions 
  

# ----------------------------------------------------------------------------------------------------------------------
#  Correlation_Buildup
# ---------------------------------------------------------------------------------------------------------------------- 
class Emission_Index_Correlation_Method(Emissions): 
    """ 
    Emissions Index Correlation Method
    """    
    
    def __defaults__(self): 
        """
        This sets the default values and methods for the analysis.
    
        Assumptions:
        None
    
        Source:
        None 
        """ 

        # build the evaluation process
        compute                         = Process()  
        compute.emissions               = None  
        self.process                    = Process()
        self.process.compute            = compute 
                
        return
            
    def initialize(self):   
        """
        This function computes the emissions of different species from the Emission Indices 
        available in literature.
    
        Assumptions:
        None
    
        Source:
        None 
        """         
        
        compute   =  self.process.compute     
        compute.emissions  = evaluate_correlation_emissions_indices
        return 


    def evaluate(self,segment):
        """
        The default evaluate function.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        results   <RCAIDE data class>

        Properties Used:
        self.settings
        self.vehicle
        """          
        settings = self.settings
        vehicle  = self.vehicle   
        results  = self.process.compute(segment,settings,vehicle)

        return results             