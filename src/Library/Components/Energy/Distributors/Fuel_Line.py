# RCAIDE/Library/Compoments/Energy/Networks/Distribution/Fuel_Line.py 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Library.Components                                import Component
from RCAIDE.Library.Components.Component                      import Container    

# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Line
# ---------------------------------------------------------------------------------------------------------------------- 
class Fuel_Line(Component):
    """ Fuel line class.
    """ 
    
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """          
        self.tag                           = 'fuel_line'  
        self.fuel_tanks                    = Container()
        self.assigned_propulsors           = []
        self.active                        = True 
        self.efficiency                    = 1.0 