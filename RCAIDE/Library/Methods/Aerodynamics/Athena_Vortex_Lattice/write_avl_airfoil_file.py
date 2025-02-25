# RCAIDE/Library/Methods/Aerodynamics/Athena_Vortex_Lattice/write_avl_airfoil_file.py
#
# Created: Oct 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Library.Methods.Aerodynamics.Athena_Vortex_Lattice.purge_files  import purge_files
from RCAIDE.Library.Methods.Geometry.Airfoil.import_airfoil_geometry        import import_airfoil_geometry 

# python imports
import os

# ----------------------------------------------------------------------------------------------------------------------
#  write_avl_airfoil_file
# ---------------------------------------------------------------------------------------------------------------------- 
def write_avl_airfoil_file(rcaide_airfoil_filename):
    """ This function writes the standard airfoil file format from Airfoil tools 
    to avl file format

    Assumptions:
        None
        
    Source: 
   
    Inputs:
        filename
   
    Outputs:
        airfoil.dat
   
    Properties Used:
        N/A
    """       
    

    # unpack avl_inputs
    avl_airfoil_filename =  rcaide_airfoil_filename.split(".")[-2].split("/")[-1] + '.dat'
    
    # purge file 
    purge_files([avl_airfoil_filename]) 
    
    # read airfoil file header 
    origin  = os.getcwd()
    os_path = os.path.split(origin)[0]
    f_path  = rcaide_airfoil_filename
    f = open(f_path)  
    data_block = f.readlines() 
    f.close()   
    airfoil_name = data_block[0].strip()
    
    # import airfoil coordinates 
    airfoil_geometry_data = import_airfoil_geometry(f_path)
    dim = len(airfoil_geometry_data.x_coordinates)
              
    # write file  
    with open(avl_airfoil_filename,'w') as afile:
            afile.write(airfoil_name + "\n")  
            for i in range(dim - 1):
                if i == int(dim/2):
                    pass  
                elif airfoil_geometry_data.y_coordinates[i] < 0.0:
                    case_text = '\t' + format(airfoil_geometry_data.x_coordinates[i], '.7f')+ "   " + format(airfoil_geometry_data.y_coordinates[i], '.7f') + "\n" 
                    afile.write(case_text)
                else:   
                    case_text = '\t' + format(airfoil_geometry_data.x_coordinates[i], '.7f')+ "    " + format(airfoil_geometry_data.y_coordinates[i], '.7f') + "\n" 
                    afile.write(case_text)
    afile.close()
    return avl_airfoil_filename 
 
