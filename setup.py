import os
import sys
from setuptools import setup, find_packages

PACKAGE_NAME = "RCAIDE"
VERSION = "1.0.0"
DESCRIPTION = "RCAIDE: Research Community Aerospace Interdisciplinary Design Environment"
AUTHOR = "RCAIDE Trust"
MAINTAINER = "The Developers"
URL = "https://rcaide.org"
REQUIRED_PYTHON = ">=3.8, <3.14"
REQUIREMENTS = [
    "numpy",
    "scipy",
    "scikit-learn",
    "plotly",
    "matplotlib",
    "kaleido",
    "pandas",
    "importlib_metadata; python_version<'3.8'"
]

# Utility function to read a file's contents
def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

# Write version.py dynamically
def write_version_file(version, filename="RCAIDE/version.py"):
    content = f"""# THIS FILE IS GENERATED
version = '{version}'
"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as version_file:
        version_file.write(content)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        uninstall_package()
    else:
        write_version_file(VERSION)
        setup_package()

def setup_package():
    setup(
        name=PACKAGE_NAME,
        version=VERSION,
        description=DESCRIPTION,
        author=AUTHOR,
        maintainer=MAINTAINER,
        url=URL,
        packages=find_packages(include=["RCAIDE", "RCAIDE.*"]),
        include_package_data=True,
        python_requires=REQUIRED_PYTHON,
        install_requires=REQUIREMENTS,
        platforms=["Windows", "Linux", "Unix", "Mac OS-X"],
        zip_safe=False
    )

def uninstall_package():
    """Uninstalls the package using pip."""
    try:
        import pip
        args = ["uninstall", "-y", PACKAGE_NAME]
        sys.exit(pip.main(args))
    except ImportError:
        print("pip is required to uninstall this package.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
