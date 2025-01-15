# RCAIDE/Framework/Mission/Common/Conditions.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
from RCAIDE.Framework.Core                    import Data 

# python imports 
import numpy as np 
# ----------------------------------------------------------------------------------------------------------------------
#  Conditions
# ----------------------------------------------------------------------------------------------------------------------
class Conditions(Data):
    """
    Base class for storing and managing mission segment conditions data

    Attributes
    ----------
    _size : int
        Size of condition arrays, defaults to 1

    Methods
    -------
    ones_row(cols)
        Returns a row vector of ones with given columns
    ones_row_m1(cols) 
        Returns an N-1 row vector of ones
    ones_row_m2(cols)
        Returns an N-2 row vector of ones
    expand_rows(rows, override=False)
        Expands condition arrays to specified number of rows

    Notes
    -----
    This class provides the core data structure for storing conditions during
    mission analysis. It inherits from Data to provide attribute-style access
    to nested dictionaries.

    **Major Assumptions**
    * Arrays can be properly broadcast for calculations
    * Conditions follow expected structure for segment type
    """

    _size = 1
    
    def ones_row(self,cols):
        """
        Returns a row vector of ones with given number of columns

        Parameters
        ----------
        cols : int
            Number of columns for output array

        Returns
        -------
        array : ndarray
            Array of ones with shape (_size, cols)

        Notes
        -----
        Used to initialize condition arrays with proper dimensions.
        """     
        return np.ones([self._size,cols])
    
    def ones_row_m1(self,cols):
        """
        Returns an N-1 row vector of ones

        Parameters
        ----------
        cols : int
            Number of columns for output array

        Returns
        -------
        array : ndarray
            Array of ones with shape (_size-1, cols)

        Notes
        -----
        Creates arrays one row shorter than standard size.
        Used for difference calculations.
        """ 
        return expanded_array(cols, 1)
    
    def ones_row_m2(self,cols):
        """
        Returns an N-2 row vector of ones

        Parameters
        ----------
        cols : int
            Number of columns for output array

        Returns
        -------
        array : ndarray
            Array of ones with shape (_size-2, cols)

        Notes
        -----
        Creates arrays two rows shorter than standard size.
        Used for second difference calculations.
        """ 
        return expanded_array(cols, 2)
    
    
    def expand_rows(self,rows,override=False):
        """
        Expands condition arrays to specified number of rows

        Parameters
        ----------
        rows : int
            Number of rows to expand arrays to
        override : bool, optional
            Whether to override existing arrays
            Default: False

        Notes
        -----
        Recursively resizes arrays in the conditions structure.
        Will not overwrite existing arrays unless override=True.

        **Major Assumptions**
        * Arrays can be broadcast to new dimensions
        * Original data is preserved if not overridden
        """           
        
        # store
        self._size = rows
        
        # recursively initialize condition and unknown arrays 
        # to have given row length
        
        for k,v in self.items():
            try:
                rank = v.ndim
            except:
                rank = 0
            # recursion
            if isinstance(v,Conditions):
                v.expand_rows(rows,override=override)
            elif isinstance(v,expanded_array):
                self[k] = v.resize(rows)
            # need arrays here
            elif rank == 2:
                #Check if it's already expanded
                if v.shape[0]<=1 or override:
                    self[k] = np.resize(v,[rows,v.shape[1]])
        
        return
                
class expanded_array(Data):
    """
    Array class that expands to proper dimensions when mission is initialized

    Attributes
    ----------
    _size : int
        Current size of array, defaults to 1
    _adjustment : int
        Number of rows to reduce from final size
    _cols : int
        Number of columns in array
    _array : ndarray
        Underlying numpy array storage

    Methods
    -------
    resize(rows)
        Resizes array to specified number of rows minus adjustment
    __call__()
        Returns current array value
    __mul__(other)
        Handles multiplication with other values
    __rmul__(other)
        Handles reverse multiplication with other values

    Notes
    -----
    This class provides delayed array expansion for mission calculations.
    Arrays start as 1x1 and expand to proper dimensions when the mission
    is initialized. Used by Conditions class for efficient memory usage.

    **Major Assumptions**
    * Array will be resized before use in calculations
    * Adjustment value remains constant
    * Multiplication operations create new 1x1 arrays
    """

    _size = 1  
        
    def __init__(self, cols, adjustment):
        """ Initialization that sets expansion later
         
        Parameters
        ----------
        cols : int
            Number of columns for array
        adjustment : int
            Number of rows to reduce from final size

        Notes
        -----
        Creates initial 1x1 array that will be expanded later.
        Stores column count and size adjustment for future resize.
        """          
        
        self._adjustment = adjustment
        self._cols       = cols
        self._array      = np.array([[1]])
        
        
    def resize(self,rows):
        """ This function actually completes the resizing. After this it's no longer an expanded array. That way it
            doesn't propogate virally. That means if one wishes to resize later the conditions need to be reset.
         
        Parameters
        ----------
        rows : int
            Number of rows for final array

        Returns
        -------
        array : ndarray
            Resized array with shape (rows-adjustment, cols)

        Notes
        -----
        Converts expandable array to fixed numpy array.
        Called during mission initialization to set final dimensions.
        """   
        # unpack
        adjustment = self._adjustment
        
        # pack
        self._size = rows
        value      = self._array
        
        return np.resize(value,[rows-adjustment,value.shape[1]])
    
    def __call__(self):
        """ This returns the value and shape of the array as is
         
        Returns
        -------
        array : ndarray
            Current array value and shape

        Notes
        -----
        Provides direct access to underlying numpy array.
        Used when array value is needed before expansion.
        """           
        
        return self._array
    
    def __mul__(self,other):
        """ Performs multiplication and returns self
         
        Parameters
        ----------
        other : float
            Value to multiply by

        Returns
        -------
        self : expanded_array
            Updated array with new values

        Notes
        -----
        Creates new 1x1 array with multiplied value.
        Maintains expandable array properties.
        """          
        
        self._array = np.resize(other,[1,1])
        
        return self

    def __rmul__(self,other):
        """ Performs multiplication and returns self
         
        Parameters
        ----------
        other : float
            Value to multiply by

        Returns
        -------
        self : expanded_array
            Updated array with new values

        Notes
        -----
        Handles multiplication when array is second operand.
        Identical behavior to __mul__.
        """                 
        
        self._array = np.resize(other,[1,1])
        
        return self    
        
    