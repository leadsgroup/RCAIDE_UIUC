from setuptools import setup, find_packages

PACKAGE_NAME = "RCAIDE"
VERSION = "1.0.0"
AUTHOR = "RCAIDE Team"
DESCRIPTION = "RCAIDE: Research Community Aerospace Interdisciplinary Design Environment"
URL = "https://github.com/leadsgroup/RCAIDE"

REQUIREMENTS = [
    "numpy",
    "scipy",
    "matplotlib",
    "scikit-learn",
    "plotly",
    "kaleido",
    "pandas",
    "importlib-metadata; python_version<'3.8'",
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    url=URL,
    package_dir={"RCAIDE": "src"},
    packages=["RCAIDE"],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)