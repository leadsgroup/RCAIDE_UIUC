# RCAIDE/Compoments/Fuselages/Fuselage.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from RCAIDE.Framework.Core                import Data 
from RCAIDE.Library.Components.Component  import Container
from RCAIDE.Library.Components            import Component
from RCAIDE.Library.Methods.Weights.Moment_of_Inertia.compute_fuselage_moment_of_inertia import  compute_fuselage_moment_of_inertia

 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Fuselage
# ---------------------------------------------------------------------------------------------------------------------- 
class Fuselage(Component):
    """ This is a standard fuselage for a tube and wing aircraft.
    
    Assumptions:
    Conventional fuselage
    
    Source:
    N/A
    """
    
    def __defaults__(self):
        """ This sets the default values for the component to function.
        
        Assumptions:
        None
    
        Source:
        N/A
    
        Inputs:
        None
    
        Outputs:
        None
    
        Properties Used:
        None
        """      
        
        self.tag                                    = 'fuselage'
        self.origin                                 = [[0.0,0.0,0.0]]
        self.aerodynamic_center                     = [0.0,0.0,0.0] 
        self.differential_pressure                  = 0.0    
        self.seats_abreast                          = 0.0
        self.seat_pitch                             = 0.0
        self.number_coach_seats                     = 0.0

        self.areas                                  = Data()
        self.areas.front_projected                  = 0.0
        self.areas.side_projected                   = 0.0
        self.areas.wetted                           = 0.0
        
        self.effective_diameter                     = 0.0
        self.width                                  = 0.0  
        
        self.heights                                = Data() 
        self.heights.maximum                        = 0.0
        self.heights.at_quarter_length              = 0.0
        self.heights.at_three_quarters_length       = 0.0
        self.heights.at_wing_root_quarter_chord     = 0.0
        self.heights.at_vertical_root_quarter_chord = 0.0 
        
        self.lengths                                = Data()     
        self.lengths.nose                           = 0.0
        self.lengths.tail                           = 0.0
        self.lengths.total                          = 0.0 
        self.lengths.cabin                          = 0.0 
        self.lengths.fore_space                     = 0.0
        self.lengths.aft_space                      = 0.0 
        
        self.x_rotation                             = 0.0
        self.y_rotation                             = 0.0
        self.z_rotation                             = 0.0 

        self.fineness                               = Data() 
        self.fineness.nose                          = 0.0 
        self.fineness.tail                          = 0.0  
        self.nose_curvature                         = 1.5
        self.tail_curvature                         = 1.5   
    
        self.fuel_tanks                             = Container()
 
        self.vsp_data                               = Data()
        self.vsp_data.xsec_surf_id                  = ''    # There is only one XSecSurf in each VSP geom.
        self.vsp_data.xsec_num                      = None  # Number if XSecs in fuselage geom. 
        self.Segments                               = Container()
        
    def append_segment(self,segment):
        """ Adds a segment to the fuselage. 
    
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

        # Assert database type
        if not isinstance(segment,Data):
            raise Exception('input component must be of type Data()')

        # Store data
        self.Segments.append(segment)

        return
    
    def append_fuel_tank(self,fuel_tank):
        """ Adds a fuel tank to the fuselage 
    
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

        # Assert database type
        if not isinstance(fuel_tank,Data):
            raise Exception('input component must be of type Data()')
    
        # Store data
        self.Fuel_Tanks.append(fuel_tank)

        return 

    def compute_moment_of_inertia(self, center_of_gravity=[[0, 0, 0]]): 
        I =  compute_fuselage_moment_of_inertia(self,center_of_gravity) 
        return I    