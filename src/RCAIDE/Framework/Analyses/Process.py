# RCAIDE/Framework/Analyses/Process.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Framework.Core import ContainerOrdered
from RCAIDE.Framework.Core import Data 

# ----------------------------------------------------------------------------------------------------------------------
# Process
# ----------------------------------------------------------------------------------------------------------------------  
class Process(ContainerOrdered):
    """ RCAIDE.Framework.Analyses.Process()
    
        The Top Level Process Container Class
        
            Assumptions:
            None
            
            Source:
            N/A
    """     
    
    def evaluate(self,*args,**kwarg):
        """This is used to execute the evaluate functions of the analyses
            stored in the container.
        
                Assumptions:
                None
        
                Source:
                N/A
        
                Inputs:
                None
        
                Outputs:
                Results of the Evaluate Functions
        
                Properties Used:
                N/A
            """        
        
        results = Data() 
        
        for tag,step in self.items():  
            
            if hasattr(step,'evaluate'): 
                result = step.evaluate(*args,**kwarg)
            else:
                result = step(*args,**kwarg)
                
            results[tag] = result
         
        return results
        
    def __call__(self,*args,**kwarg):
        """This is used to set the class' call behavior to the evaluate functions.
        
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
        return self.evaluate(*args,**kwarg) 
    
