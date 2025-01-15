# RCAIDE/Framework/Analyses/Mission/Segments/Conditions/State.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Framework.Core import DataOrdered
from .Conditions           import Conditions
from .Unknowns             import Unknowns
from .Residuals            import Residuals
from .Numerics             import Numerics   

# python imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  State
# ----------------------------------------------------------------------------------------------------------------------
class State(Conditions):
    """
    Data structure for storing complete mission segment state information

    Attributes
    ----------
    tag : str
        Identifier, defaults to 'state'
    initials : Conditions
        Initial conditions at segment start
    numerics : Numerics
        Numerical integration parameters
    unknowns : Unknowns
        Variables to be solved
    conditions : Conditions
        Current state conditions
    residuals : Residuals
        Constraint residuals

    Methods
    -------
    expand_rows(rows, override=False)
        Expands state arrays to specified number of rows
    merged()
        Combines states from multiple segments

    Notes
    -----
    This class provides the complete state representation for mission segments,
    including both the physical state and numerical solution state. It inherits
    from Conditions to provide data structure functionality.

    **Major Assumptions**
    * State variables are properly initialized
    * Array dimensions are consistent
    * Segment type determines required state variables
    * Initial conditions are valid

    See Also
    --------
    RCAIDE.Framework.Mission.Common.Conditions
    RCAIDE.Framework.Mission.Common.Numerics
    RCAIDE.Framework.Mission.Common.Unknowns
    RCAIDE.Framework.Mission.Common.Residuals
    """
    
    
    def __defaults__(self):
        """
        Sets default values for state container

        Notes
        -----
        Initializes basic state structure with empty containers.
        Additional state variables are added based on segment type.
        Called automatically when class is instantiated.
        """           
        
        self.tag        = 'state'
        self.initials   = Conditions()
        self.numerics   = Numerics()
        self.unknowns   = Unknowns()
        self.conditions = Conditions()
        self.residuals  = Residuals()
        
    def expand_rows(self,rows,override=False):
        """
        Expands state arrays to specified number of rows

        Parameters
        ----------
        rows : int
            Number of rows to expand arrays to
        override : bool, optional
            Whether to override existing arrays
            Default: False

        Notes
        -----
        Recursively resizes arrays in state structure except initials and numerics.
        Will not overwrite existing arrays unless override=True.

        **Major Assumptions**
        * Arrays can be broadcast to new dimensions
        * Original data is preserved if not overridden
        """         
        
        # store
        self._size = rows
        
        for k,v in self.items(): 
            try:
                rank = v.ndim
            except:
                rank = 0            
            # don't expand initials or numerics
            if k in ('initials','numerics'):
                continue
            
            # recursion
            elif isinstance(v,Conditions):
                v.expand_rows(rows,override=override)
            # need arrays here
            elif rank == 2:
                self[k] = np.resize(v,[rows,v.shape[1]])
            #: if type
        #: for each key,value        
        
# ----------------------------------------------------------------------------------------------------------------------
# Container
# ----------------------------------------------------------------------------------------------------------------------        
                
class Container(State):
    """
    Container for managing multiple segment states

    Attributes
    ----------
    segments : DataOrdered
        Ordered dictionary of segment states

    Methods
    -------
    merged()
        Combines states from all segments

    Notes
    -----
    This class provides organization for multiple segment states and methods
    to combine them. Inherits from State to provide state functionality.

    **Major Assumptions**
    * Segments are properly ordered
    * Segment states are compatible for merging
    """

    def __defaults__(self):
        """
        Sets default values for container initialization

        Attributes
        ----------
        segments : DataOrdered
            Empty ordered dictionary for storing mission segments

        Notes
        -----
        This method initializes the container with an empty DataOrdered dictionary
        that will store mission segments in the order they are added. Called
        automatically when class is instantiated.

        **Major Assumptions**
        * Segments will be added in correct execution order
        * DataOrdered maintains insertion order
        * Container starts empty

        See Also
        --------
        RCAIDE.Framework.Core.DataOrdered
        """
        self.segments = DataOrdered()
        
    def merged(self):
        """
        Combines the states of multiple segments

        Returns
        -------
        state_out : State
            Combined state containing all segment data

        Notes
        -----
        Merges unknowns, conditions, and residuals from all segments.
        Maintains time ordering of segments.

        **Major Assumptions**
        * Segments have compatible state structures
        * Arrays can be vertically stacked
        """              
        
        state_out = State()
        
        for i,(tag,sub_state) in enumerate(self.segments.items()):
            for key in ['unknowns','conditions','residuals']:
                if i == 0:
                    state_out[key].update(sub_state[key])
                else:
                    state_out[key] = state_out[key].do_recursive(append_array,sub_state[key])
            
        return state_out
        
State.Container = Container 
        
# ----------------------------------------------------------------------------------------------------------------------
# append_array
# ---------------------------------------------------------------------------------------------------------------------- 

def append_array(A,B=None):
    """
    Stacks arrays vertically for state merging

    Parameters
    ----------
    A : ndarray
        First array to stack
    B : ndarray, optional
        Second array to stack
        Default: None

    Returns
    -------
    array : ndarray or None
        Vertically stacked array if inputs are arrays, None otherwise

    Notes
    -----
    Helper function for merging segment states.
    Returns None if inputs are not both numpy arrays.
    """       
    if isinstance(A,np.ndarray) and isinstance(B,np.ndarray):
        return np.vstack([A,B])
    else:
        return None