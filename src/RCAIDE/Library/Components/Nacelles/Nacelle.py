 # RCAIDE/Compoments/Nacelles/Nacelle.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from RCAIDE.Framework.Core              import Data 
from RCAIDE.Library.Components          import Component   
import scipy as sp
import numpy as np
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Nacalle
# ----------------------------------------------------------------------------------------------------------------------  
class Nacelle(Component):
    """ This is a nacelle for a generic aircraft.
    
    Assumptions:
    None
    
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
        """      
        
        self.tag                       = 'nacelle'
        self.origin                    = [[0.0,0.0,0.0]]
        self.aerodynamic_center        = [0.0,0.0,0.0]  
        self.areas                     = Data()
        self.areas.front_projected     = 0.0
        self.areas.side_projected      = 0.0
        self.areas.wetted              = 0.0 
        self.diameter                  = 0.0 
        self.inlet_diameter            = 0.0
        self.length                    = 0.0   
        self.orientation_euler_angles  = [0.,0.,0.]    
        self.flow_through              = True
        self.has_pylon                 = True
        self.differential_pressure     = 0.0    
        self.cowling_airfoil_angle     = 0.0

    def append_operating_conditions(self,segment,propulsor): 
        return

    def nac_vel_to_body(self):
        """This rotates from the systems body frame to the nacelles velocity frame

        Assumptions:
        There are two nacelle frames, the vehicle frame describing the location and the nacelle velocity frame
        velocity frame is X out the nose, Z towards the ground, and Y out the right wing
        vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None 
        """
        
        body2nacvel = self.body_to_nac_vel()
        
        r = sp.spatial.transform.Rotation.from_matrix(body2nacvel)
        r = r.inv()
        rot_mat = r.as_matrix()

        return rot_mat
    
    def body_to_nac_vel(self):
        """This rotates from the systems body frame to the nacelles velocity frame

        Assumptions:
        There are two nacelle frames, the vehicle frame describing the location and the nacelle velocity frame
        velocity frame is X out the nose, Z towards the ground, and Y out the right wing
        vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None 
        """
        
        # Go from body to vehicle frame
        body_2_vehicle = sp.spatial.transform.Rotation.from_rotvec([0,np.pi,0]).as_matrix()
        
        # Go from vehicle frame to nacelle vehicle frame: rot 1 including the extra body rotation
        rots    = np.array(self.orientation_euler_angles) * 1. 
        vehicle_2_nac_vec = sp.spatial.transform.Rotation.from_rotvec(rots).as_matrix()        
        
        # GO from the nacelle vehicle frame to the nacelle velocity frame: rot 2
        nac_vec_2_nac_vel = self.vec_to_vel()
        
        # Do all the matrix multiplies
        rot1    = np.matmul(body_2_vehicle,vehicle_2_nac_vec)
        rot_mat = np.matmul(rot1,nac_vec_2_nac_vel) 
        return rot_mat    
    
    

    def vec_to_vel(self):
        """This rotates from the nacelles vehicle frame to the nacelles velocity frame

        Assumptions:
        There are two nacelle frames, the vehicle frame describing the location and the nacelle velocity frame
        velocity frame is X out the nose, Z towards the ground, and Y out the right wing
        vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """
        
        rot_mat = sp.spatial.transform.Rotation.from_rotvec([0,np.pi,0]).as_matrix()
        
        return rot_mat
    
    
        