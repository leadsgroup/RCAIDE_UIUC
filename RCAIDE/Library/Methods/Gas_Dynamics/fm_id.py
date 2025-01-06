# fm_id.py
#
# Created: Dec 2024 M Clarke

# ----------------------------------------------------------------------
#  fm_id
# ---------------------------------------------------------------------- 
def fm_id(M,gamma):
    """Function that takes in the Mach number and isentropic expansion factor,
    and outputs a value for f(M) that's commonly used in compressible flow
    calculations.

    Inputs:
    M       [-]
    gamma   [-]

    Outputs:
    fm      [-]

    Spurce:
    https://web.stanford.edu/~cantwell/AA210A_Course_Material/AA210A_Course_Notes/
    """

    m0 = (gamma+1.)/(2.*(gamma-1.))
    m1 = ((gamma+1.)/2.)**m0
    m2 = (1.+(gamma-1.)/2.*M*M)**m0
    fm = m1*M/m2

    return fm
