# Configuration file for the Sphinx documentation builder.

import os
import sys
from unittest.mock import Mock

# Mock modules to prevent import errors
sys.modules['RCAIDE.Framework.Plugins.load_plugin'] = Mock()

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath('../..'))  # Root directory
sys.path.insert(0, os.path.abspath('../../RCAIDE'))  # RCAIDE directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath('.'))))  # Parent of docs

# -- Project information -----------------------------------------------------
project = 'RCAIDE'
copyright = '2024, Laboratory for Electric Aircraft Design and Sustainability'
author = 'Laboratory for Electric Aircraft Design and Sustainability'
release = '1.0.0'

# Add logo configuration
html_logo = 'source/_static/leads_logo.png'
html_title = "RCAIDE"

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'nbsphinx',
    'sphinx.ext.mathjax',
    'sphinx_multiversion',  # Add sphinx-multiversion
]

templates_path = ['_templates']
exclude_patterns = []
toctree_maxdepth = 40
autosummary_generate = True
add_module_names = False

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__',
    'inherited-members': False,
    'show-inheritance': False
}

# -- Options for HTML output -------------------------------------------------
html_static_path = ['_static']
html_theme = 'pydata_sphinx_theme'

html_theme_options = {
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "navbar_persistent": ["search-button"],
    "primary_sidebar_end": ["sidebar-ethical-ads"],
    "navigation_with_keys": False,
    "navbar_align": "left",
    "show_toc_level": 2,
    "navigation_depth": 3,
    'logo_only': True,
    'display_version': False,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/leadsgroup/RCAIDE_LEADS",
            "icon": "fab fa-github-square",
            "type": "fontawesome",
        }
    ],
    "logo": {
        "image_dark": "_static/leads_logo.png",
        "image_light": "_static/leads_logo.png",
        "image_dark_alt": "_static/leads_logo.png",
        "image_light_alt": "_static/leads_logo.png",
        "text": "RCAIDE",
    },
    "default_mode": "dark",
}

html_baseurl = "https://docs.rcaide.leadsresearchgroup.com"

html_context = {
    "default_mode": "light",
    "header_links": [
        ("GitHub", "https://github.com/leadsgroup/RCAIDE_LEADS", True),
    ]
}

html_theme = 'pydata_sphinx_theme'

html_context = {
    "default_mode": "auto",
}

html_css_files = ['custom.css']

# -- sphinx-multiversion configuration ---------------------------------------
smv_branch_whitelist = r'^master$|^develop$'
smv_remote_whitelist = r'^origin$'
smv_outputdir_format = '{ref.name}'
smv_retain_merges = False
smv_prefer_remote_refs = True

# Override the 'release' version based on the branch
if 'smv_tag_prefix' not in globals():
    if os.environ.get('SMV_REF_NAME') == 'develop':
        release = 'development'
    else:
        release = 'stable'
