.. _install:

##############
Install
##############

This section provides instructions to install RCAIDE and its dependencies.

**System Requirements**
========================
Before installing RCAIDE, ensure that your system meets the following requirements:

- Python >= 3.8
- pip >= 20.0
- Supported OS: Linux, macOS, Windows

**Installing RCAIDE**
========================

Follow these steps to install RCAIDE:

1. **Using pip**  
  
   Coming soon...



2. **From Source**  

   Alternatively, clone the RCAIDE repository and install it manually:
   

   .. code-block:: bash

      git clone https://github.com/leadsgroup/RCAIDE_LEADS.git
    
   Install the dependencies:

   .. code-block:: bash

      pip install -r requirements.txt

   Install RCAIDE:

   .. code-block:: bash

      cd RCAIDE
      python3 setup.py develop
     

3. **Optional Dependencies**  
   To enable additional features, install the following optional dependencies:

   .. code-block:: bash

      pip install -r requirements.txt

**Verifying the Installation**
===============================
To confirm that RCAIDE has been successfully installed, run the following command:

.. code-block:: bash

   python -c "import RCAIDE; print(RCAIDE.__version__)"

If RCAIDE is installed correctly, it will print the installed version number.

