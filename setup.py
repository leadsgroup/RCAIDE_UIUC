from setuptools import setup, find_packages

setup(
    name="RCAIDE",
    version="0.1.0",
    package_dir={"": "src"},  # Look for packages in `src`
    packages=find_packages(where="src"),  # Automatically find all packages
  install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "scikit-learn",
        "plotly",
        "kaleido",
        "pandas",
        "importlib_metadata; python_version<'3.8'",  
    ],
    python_requires=">=3.8",  # Minimum Python version
    description="RCAIDE package",
    author="Your Name",
    url="https://github.com/yourusername/RCAIDE_LEADS",
)
