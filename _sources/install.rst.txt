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



2. **From Source (editable mode)**  

   Alternatively, clone the RCAIDE repository and install it manually:
   

   .. code-block:: bash

      git clone https://github.com/leadsgroup/RCAIDE_LEADS.git
      cd RCAIDE_LEADS
    
   Install the dependencies and RCAIDE in editable mode:

   .. code-block:: bash

      pip install -e .

**Verifying the Installation**
===============================
To confirm that RCAIDE has been successfully installed, run the following command:

.. code-block:: bash

   python -c "import RCAIDE; print(RCAIDE.__version__)"

If RCAIDE is installed correctly, it will print the installed version number.

