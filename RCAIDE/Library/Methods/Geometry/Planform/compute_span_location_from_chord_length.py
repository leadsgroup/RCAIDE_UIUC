
# ----------------------------------------------------------------------
#  Compute Span Location from Chord Length
# ---------------------------------------------------------------------- 
def compute_span_location_from_chord_length(wing,chord_length):
    """Computes the location along the half-span given a chord length.

    Assumptions:
    Linear variation of chord with span. Returns 0 if constant chord wing.

    Source:
    None

    Inputs:
    wing.chords.
      root                [m]
      tip                 [m]
    wing.spans.projected  [m]
    chord_length          [m]

    Outputs:
    span_location         [m] 

    Properties Used:
    N/A
    """      
    
    #unpack
    ct = wing.chords.tip
    cr = wing.chords.root
    b  = wing.spans.projected
    
    b_2 = b/2.
    
    if (cr-ct)==0:
        span_location = 0.
    else:
        span_location = b_2*(1-(chord_length-ct)/(cr-ct))
    
        
    return span_location