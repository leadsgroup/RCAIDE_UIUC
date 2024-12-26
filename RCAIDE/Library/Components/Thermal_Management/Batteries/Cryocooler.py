# RCAIDE/Library/Components/Thermal_Management/Batteries/Cryocooler.py
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports  
from RCAIDE.Library.Components import Component  
from RCAIDE.Library.Methods.Thermal_Management.Cryogenics.cryocooler_model import cryocooler_model

# ---------------------------------------------------------------------------------------------------------------------- 
#  Cryocooler
# ----------------------------------------------------------------------------------------------------------------------      
class Cryocooler(Component):
    """
    A class representing a cryogenic cooling system for maintaining extremely low 
    temperatures in battery or other systems.

    Attributes
    ----------
    cooler_type : str
        Type of cryocooler system being used, defaults to None
        
    rated_power : float
        Maximum power rating of the cryocooler, defaults to 0.0
        
    min_cryo_temp : float
        Minimum achievable cryogenic temperature, defaults to 0.0
        
    ambient_temp : float
        Ambient temperature for heat rejection, defaults to 300.0
        
    inputs.cooling_power : float
        Required cooling power at cryogenic temperature, defaults to 0.0
        
    inputs.cryo_temp : float
        Target cryogenic temperature, defaults to 0.0
        
    mass_properties.mass : float
        Mass of the cryocooler system, defaults to 0.0
        
    outputs.input_power : float
        Power required by the cryocooler, defaults to 0.0

    Notes
    -----
    The cryocooler provides cooling power at cryogenic temperatures. It requires 
    electrical power input to provide cooling, with the required input power 
    depending on:
    
    * Operating temperature differential
    * Required cooling power
    * System efficiency
    
    **Definitions**

    'Cooling Power'
        Heat removal capacity at the cryogenic temperature
        
    'Input Power'
        Electrical power required to achieve the cooling effect

    See Also
    --------
    RCAIDE.Library.Components.Thermal_Management.Batteries.Air_Cooled
        Alternative cooling approach for moderate temperatures
    RCAIDE.Library.Components.Thermal_Management.Batteries.Liquid_Cooled_Wavy_Channel
        Alternative cooling approach using liquid coolant
    """
    
    def __defaults__(self):
        """
        Sets default values for the cryocooler attributes.
        """
        self.cooler_type          = None
        self.rated_power          = 0.0
        self.min_cryo_temp        = 0.0 
        self.ambient_temp         = 300.0
        self.inputs.cooling_power = 0.0
        self.inputs.cryo_temp     = 0.0
        self.mass_properties.mass = 0.0
        self.rated_power          = 0.0
        self.outputs.input_power  = 0.0

    def energy_calc(self, conditions):
        """
        Calculates the required input power for the cryocooler.

        Parameters
        ----------
        conditions : Data
            Operating conditions for the calculation

        Returns
        -------
        float
            Required input power in Watts

        Notes
        -----
        Uses the cryocooler model to determine power requirements based on:
        * Target cryogenic temperature
        * Required cooling power
        * Cooler type and characteristics
        """
        output = cryocooler_model(self)
        self.outputs.input_power = output[0]

        return output[0]

    

