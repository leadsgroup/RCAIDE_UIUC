# RCAIDE/Library/Compoments/Energy/Cryogenic_Tanks/Cryogenic_Tank.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Library.Components          import Component
from RCAIDE.Library.Methods.Energy.Sources.Cryogenic_Tanks.append_cryogenic_tank_conditions import append_cryogenic_tank_conditions 

# ----------------------------------------------------------------------------------------------------------------------
#  Cryogenic Tank
# ---------------------------------------------------------------------------------------------------------------------     
class Cryogenic_Tank(Component):
    """
    Base class for aircraft cryogenic tank implementations
    
    Attributes
    ----------
    tag : str
        Identifier for the cryogenic tank (default: 'cryogenic_tank')
        
    cryogenic_selector_ratio : float
        Ratio of cryogenic flow allocation (default: 1.0)
        
    mass_properties.empty_mass : float
        Mass of empty tank structure [kg] (default: 0.0)
        
    secondary_cryogenic_flow : float
        Secondary cryogenic flow rate [kg/s] (default: 0.0)
        
    cryogenic : Component, optional
        Cryogenic type stored in tank (default: None)

    Notes
    -----
    The cryogenic tank base class provides common attributes and methods for
    different types of aircraft cryogenic tanks. It handles basic cryogenic storage
    and flow management functionality.
    """
    
    def __defaults__(self):
        """
        Sets default values for cryogenic tank attributes
        """          
        self.tag                         = 'cryogenic_tank'
        self.pressure                    = 1.0 
        self.mass_properties.empty_mass  = 0.0   
        self.secondary_cryogenic_flow         = 0.0
        self.cryogen                     = None
         

    def append_operating_conditions(self,segment,cryogenic_line):  
        """
        Append cryogenic tank operating conditions for a flight segment
        
        Parameters
        ----------
        segment : Segment
            Flight segment containing state conditions
        cryogenic_line : Component
            Connected cryogenic line component
        """
        append_cryogenic_tank_conditions(self,segment, cryogenic_line)  
        return                                          