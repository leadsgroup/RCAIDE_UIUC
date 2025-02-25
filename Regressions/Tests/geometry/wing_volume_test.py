# NACA_volume_compute.py
# 
# Created:  April 2018, W. Maier
# Modified: 

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------
import RCAIDE
from RCAIDE.Framework.Core import Data
from RCAIDE.Library.Methods.Geometry.Planform.estimate_wing_internal_volume import estimate_wing_internal_volume

import numpy as np


# ---------------------------------------------------------------------- 
#   Main
# ----------------------------------------------------------------------
def main():
    
    # ------------------------------------------------------------------
    # Testing Arbitrary Wing
    # ------------------------------------------------------------------
    wing                    = Data()
    wing.chords             = Data()
    wing.spans              = Data()

    camber                  = 0.02
    camber_loc              = 0.4
    wing.thickness_to_chord = 0.10
    wing.taper              = 0.5
    wing.chords.root        = 5.0  #[m^2]
    wing.chords.tip         = 2.5  #[m^2]
    wing.spans.projected    = 10.0 #[m^2]
    
    volume  = estimate_wing_internal_volume(wing, camber, camber_loc) 
    
    truth_volume = 5.0016322889806188 # [m^2]

    # Compute Errors
    error       = Data() 
    error.volume = np.abs(volume-truth_volume)/truth_volume
    
    print("Error: ",error.volume)
    
    for k,v in list(error.items()):
        assert np.any(np.abs(v)<1e-6)
    
if __name__ == '__main__':
    
    main()