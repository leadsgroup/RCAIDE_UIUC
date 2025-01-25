# RCAIDE/Library/Components/Energy/Networks/Distribution/Cryogenic_Line.py 
# 
# Created:  Jan 2025, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Library.Components                                import Component
from RCAIDE.Library.Components.Component                      import Container    

# ----------------------------------------------------------------------------------------------------------------------
#  Cryogenic Line
# ---------------------------------------------------------------------------------------------------------------------- 
class Cryogenic_Line(Component):
    """
    Class for managing cryogenic distribution between aircraft cryogenic system components
    
    Attributes
    ----------
    tag : str
        Identifier for the cryogenic line (default: 'cryogenic_line')
        
    cryogenic_tanks : Container
        Collection of cryogenic tanks connected to this line
        
    assigned_propulsors : list
        List of propulsion systems supplied by this cryogenic line
        
    active : bool
        Flag indicating if the cryogenic line is operational (default: True)
        
    efficiency : float
        Cryogenic transfer efficiency (default: 1.0)

    Notes
    -----
    The cryogenic line manages cryogenic distribution between tanks and engines, handling
    cryogenic transfer and flow control. It supports multiple cryogenic tanks and propulsors
    in various aircraft configurations.

    See Also
    --------
    RCAIDE.Library.Components.Energy.Sources.Cryogenic_Tanks
        Cryogenic tank components
    RCAIDE.Library.Components.Propulsors
        Aircraft propulsion system components
    """ 
    
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """          
        self.tag                           = 'cryogenic_line'  
        self.cryogenic_tanks               = Container()
        self.assigned_propulsors           = []
        self.active                        = True 
        self.efficiency                    = 1.0 