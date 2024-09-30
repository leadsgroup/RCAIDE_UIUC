# setup.py
# 
# 
# Created:  June 2023, E. Botero
# Modified: 
#           
#          

""" RCAIDE setup script
"""

# ----------------------------------------------------------------------------------------------------------------------
#  Main
# ----------------------------------------------------------------------------------------------------------------------

def main():
    
    # imports
    import sys
    
    the_package = 'RCAIDE'
    version     = '24.2.0'
    date        = 'Sep 30th, 2024'
    
    if len(sys.argv) >= 2:
        command = sys.argv[1]
    else:
        command = ''
    
    if command == 'uninstall':
        uninstall(the_package,version,date)
    else:
        write_version_py(version)
        install(the_package,version,date)


# ----------------------------------------------------------------------------------------------------------------------
#  Write Version
# ----------------------------------------------------------------------------------------------------------------------
def write_version_py(version,filename='RCAIDE/version.py'):
    cnt = """
# THIS FILE IS GENERATED
version = '%(version)s'

"""

    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': version})
    finally:
        a.close()        
        


# ----------------------------------------------------------------------------------------------------------------------
#  Install
# ----------------------------------------------------------------------------------------------------------------------

def install(the_package,version,date):
    
    # imports
    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup
        
    # test for requirements
    import_tests()
    
    # list all RCAIDE sub packages
    #print 'Listing Packages and Sub-Packages:'
    packages = list_subpackages(the_package,verbose=False)
    packages = list(map( '.'.join, packages ))
    
    requires = ['numpy','scipy','sklearn','plotly','matplotlib']
    python_v = '>=3.6'

    # run the setup!!!
    setup(
        name = the_package,
        version = version, 
        description = 'RCAIDE: Research Community Aerospace Interdisciplinary Design Environment',
        author = 'Laboratory of Electric Aircraft Design and Sustainability',
        #author_email = '',
        maintainer = 'The Developers',
        url = 'leadsresearchgroup.com',
        packages = packages,
        include_package_data = True,
        #license = '',
        platforms = ['Win, Linux, Unix, Mac OS-X'],
        zip_safe  = False,
        requires  = requires,
        python_requires = python_v, 
    )  
    
    return


# ----------------------------------------------------------------------------------------------------------------------
#  Uninstall
# ----------------------------------------------------------------------------------------------------------------------

def uninstall(the_package,version,date):
    """ emulates command "pip uninstall"
        just for syntactic sugar at the command line
    """
    
    import sys, shutil
    
    # clean up local egg-info
    try:
        shutil.rmtree(the_package + '.egg-info')
    except:
        pass        
        
    # import pip
    try:
        import pip
    except ImportError:
        raise ImportError('pip is required to uninstall this package')
    
    # setup up uninstall arguments
    args = sys.argv
    del args[0:1+1]
    args = ['uninstall', the_package] + args
    
    # uninstall
    try:
        pip.main(args)
    except:
        pass
    
    return
    
    
# ----------------------------------------------------------------------------------------------------------------------
#  list subpackages
# ----------------------------------------------------------------------------------------------------------------------

def list_subpackages(package_trail,verbose=False):
    """ package_trails = list_subpackages(package_trail)
        returns a list of package trails

        Inputs: 
            package_trail : a list of dependant package names, as strings
            example: os.path -> ['os','path']

        Outputs:
            package_trails : a list of package trails
            can be processed with >>> map( '.'.join, package_trails )
    """
        
    # imports
    import os

    # error checking
    if isinstance(package_trail,str):
        package_trail = [package_trail]
    elif not isinstance(package_trail,(list,tuple)):
        raise Exception('%s is not iterable' % package)

    # print current package
    if verbose:
        print('.'.join(package_trail))

    # get absolute path for package
    package_dir = os.path.abspath( os.path.join(*package_trail) )

    # find all packages
    packages = [ 
        p for p in os.listdir( package_dir ) \
        if ( os.path.isdir(os.path.join(package_dir, p)) and              # package is a directory
             os.path.isfile(os.path.join(package_dir, p, '__init__.py')) ) # and has __init__.py
    ]

    # append package trail
    packages = [ package_trail + [p] for p in packages ]

    # recursion, check for sub packages
    packages = [ subpackage \
                 for package in packages \
                 for subpackage in list_subpackages(package,verbose) ]

    # include this package trail
    package_trails = [package_trail] + packages

    # done!leadsresearchgroup.com
    return package_trails

# ----------------------------------------------------------------------------------------------------------------------
#  Import Tests
# ----------------------------------------------------------------------------------------------------------------------


def import_tests():
    """ simple check for dependencies
    """
    
    # imports
    import sys    
    
    if sys.version_info[:2] < (3, 6):
        raise RuntimeError("Python version >= 3.6 required.")    
    try:
        import numpy
    except ImportError:
        raise ImportError('numpy is required for this package') 
     
    try:
        import scipy
    except ImportError:
        raise ImportError('scipy is required for this package')
    
    try:
        import matplotlib
    except ImportError:
        raise ImportError('matplotlib is required for this package')
    
    try:
        import sklearn
    except ImportError:
        raise ImportError('scikit-learn is required for this package')    
 
    try:
        import plotly
    except ImportError:
        raise ImportError('plotly is required for this package') 
    
    try:
        import kaleido
    except ImportError:
        raise ImportError('kaleido is required for this package')   

    try:
        import pandas
    except ImportError:
        raise ImportError('pandas is required for this package')
     
    try:
        import geopy
    except ImportError:
        raise ImportError('geopy is required for this package')
    
    try:
        import importlib_metadata
    except ImportError:
        raise ImportError('importlib_metadata is required for this package')        
    
    return
    
def read(path):
    """Build a file path from *paths and return the contents."""
    with open(path, 'r') as f:
        return f.read()
    
    
# ----------------------------------------------------------------------------------------------------------------------
#  Call Main
# ----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
