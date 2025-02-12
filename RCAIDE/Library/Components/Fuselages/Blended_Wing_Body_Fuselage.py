# RCAIDE/Compoments/Fuselages/Blended_Wing_Body_Fuselage.py
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from RCAIDE.Library.Components            import Component
from RCAIDE.Library.Components.Component  import Container
from RCAIDE.Framework.Core                import Data 

# python imports 
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Blended_Wing_Body_Fuselage
# ----------------------------------------------------------------------------------------------------------------------  
class Blended_Wing_Body_Fuselage(Component):
    """
    A blended wing body (BWB) fuselage design that smoothly integrates the wing and fuselage 
    into a single lifting body configuration.

    Attributes
    ----------
    tag : str
        Unique identifier for the BWB fuselage component, defaults to 'bwb_fuselage'
    
    aft_centerbody_area : float
        Cross-sectional area of the aft centerbody section in square meters
        
    aft_centerbody_taper : float
        Taper ratio of the aft centerbody section, defined as the ratio of tip 
        to root chord lengths
        
    cabin_area : float
        Total available cabin floor area in square meters

    Notes
    -----
    The blended wing body design offers several advantages over conventional tube-and-wing
    configurations:
    
    * Reduced wetted area leading to lower skin friction drag
    * Improved lift-to-drag ratio due to the lifting body design
    * Potential for increased internal volume and better weight distribution

    **Definitions**

    'Centerbody'
        The central section of the BWB that houses the passenger cabin and cargo hold
        
    'Aft Centerbody'
        The rear section of the centerbody that transitions into the outer wing sections

    See Also
    --------
    RCAIDE.Library.Components.Fuselages.Fuselage
        Base fuselage class that provides common functionality
    RCAIDE.Library.Components.Fuselages.Tube_Fuselage
        Conventional tube fuselage design for comparison

    """
        
    def __defaults__(self):
        """
        Sets default values for all fuselage attributes.
        """      
        
        self.tag                                    = 'blended_wing_fuselage'
    
        self.origin                                 = [[0.0,0.0,0.0]]
        #self.aerodynamic_center                     = [0.0,0.0,0.0] 
        self.differential_pressure                  = 0.0    
        #self.seat_pitch                             = 0.0
        self.number_coach_seats                     = 0.0
        self.aft_centerbody_area                    = 0.0
        self.aft_centerbody_taper                   = 0.0
        self.cabin_area                             = 0.0

        self.areas                                  = Data()
        self.areas.front_projected                  = 0.0
        self.areas.aft_centerbody_area                    = 0.0
        self.areas.cabin_area                             = 0.0
        self.areas.side_projected                   = 0.0
        self.areas.wetted                           = 0.0
        
        self.effective_diameter                     = 0.0
        self.width                                  = 0.0  
        
        # self.heights                                = Data() 
        # self.heights.maximum                        = 0.0
        # self.heights.at_quarter_length              = 0.0
        # self.heights.at_three_quarters_length       = 0.0
        # self.heights.at_wing_root_quarter_chord     = 0.0
        # self.heights.at_vertical_root_quarter_chord = 0.0 
        
        self.lengths                                = Data()     
        self.lengths.nose                           = 0.0
        self.lengths.tail                           = 0.0
        self.lengths.total                          = 0.0 
        self.lengths.cabin                          = 0.0 
        self.lengths.fore_space                     = 0.0
        self.lengths.aft_space                      = 0.0 
           
        self.fuel_tanks                             = Container()
 
        # self.vsp_data                               = Data()
        # self.vsp_data.xsec_surf_id                  = ''    # There is only one XSecSurf in each VSP geom.
        # self.vsp_data.xsec_num                      = None  # Number if XSecs in fuselage geom. 
        # self.segments                               = Container()

        # self.vsp_data                               = Data()
        # self.vsp_data.xsec_id                       = ''       
        # self.vsp_data.shape                         = ''                
        
    def append_segment(self,segment):
        """
        Adds a new segment to the fuselage's segment container.

        Parameters
        ----------
        segment : Data
            Fuselage segment to be added
        """

        # Assert database type
        if not isinstance(segment,RCAIDE.Library.Components.Fuselages.Segments.Segment):
            raise Exception('input component must be of type Segment')

        # Store data
        self.segments.append(segment)

        return
    
    def append_fuel_tank(self,fuel_tank):
        """
        Adds a new fuel tank to the fuselage's fuel tank container.

        Parameters
        ----------
        fuel_tank : Data
            Fuel tank component to be added
        """

        # Assert database type
        if not isinstance(fuel_tank,Data):
            raise Exception('input component must be of type Data()')
    
        # Store data
        self.Fuel_Tanks.append(fuel_tank)

        return 

    def compute_moment_of_inertia(self, center_of_gravity=[[0, 0, 0]]): 
        """
        Computes the moment of inertia tensor for the fuselage.

        Parameters
        ----------
        center_of_gravity : list, optional
            Reference point coordinates for moment calculation, defaults to [[0, 0, 0]]

        Returns
        -------
        I : ndarray
            3x3 moment of inertia tensor in kg*m^2

        See Also
        --------
        RCAIDE.Library.Methods.Weights.Moment_of_Inertia.compute_fuselage_moment_of_inertia
            Implementation of the moment of inertia calculation
        """
        I = compute_fuselage_moment_of_inertia(self,center_of_gravity) 
        return I    