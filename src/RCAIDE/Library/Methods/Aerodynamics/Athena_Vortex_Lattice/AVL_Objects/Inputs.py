# RCAIDE/Library/Methods/Aerodynamics/Athena_Vortex_Lattice/AVL_Objects/Inputs.py
#
# Created: Oct 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
import RCAIDE
from   RCAIDE.Framework.Core import  Data  

# ----------------------------------------------------------------------------------------------------------------------
# Inputs
# ----------------------------------------------------------------------------------------------------------------------  
class Inputs(Data):
	""" A data class defining filenames for the AVL executable

	Assumptions:
	    None
    
	Source:
	    None
    
	Inputs:
	    None
    
	Outputs:
	    None
    
	Properties Used:
	    N/A
	"""    
	

	def __defaults__(self):
		""" Defines the data structure  and defaults of aircraft configuration and cases 
	
		Assumptions:
		    None
	    
		Source:
		    None
	    
		Inputs:
		    None
	    
		Outputs:
		    None
	    
		Properties Used:
		    N/A
		""" 		
		self.configuration  = Data()
		self.aircraft       = Data()
		self.cases          = Data()
		self.avl_bin_path   ='avl'
		
		filenames           = Data()
		filenames.geometry  = 'aircraft.avl'
		filenames.results   = []
		filenames.cases     = 'aircraft.cases'
		filenames.deck      = 'commands.run'
		filenames.reference_path = RCAIDE.__path__[0] + '/temporary_files/'
		self.input_files = filenames