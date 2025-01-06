.. _contributing:

=================
Contributing Guide
=================

Thank you for your interest in contributing to RCAIDE! This guide outlines how to propose changes, add new features, improve documentation, and ensure your code meets project standards.

.. contents::
   :local:
   :depth: 2

Overview
========

Contributions to RCAIDE are welcome from anyone. Whether you're fixing a bug, adding a new feature, or improving documentation, your work can help the community. Before getting started, please review this guide to ensure a smooth integration process.


Code Style and Structure
========================

RCAIDE uses a code style guide similar to `PEP 8 <https://peps.python.org/pep-0008/>`_ with some modifications for a more data-oriented structure. We encourage you to follow these conventions to maintain readability and consistency throughout the codebase.

Naming Convention
-----------------

- **Variables and fields**: 
  Use lowercase names with underscores, e.g. ``any_variable_name`` or ``field_name``.
  
- **Functions**: 
  Use lowercase names with underscores, e.g. ``function_name``.

- **Classes and Packages**:
  Classes and package names follow a capitalized with underscores convention, e.g. ``Class_Type`` or ``Package_Name``.
  
  Underscores are used in class names to allow for inclusion of acronyms if needed and maintain stylistic symmetry with field names.

Verbosity and Clarity
---------------------

- **Be explicit**: Choose descriptive, specific names for variables, functions, and classes. Avoid opaque abbreviations or acronyms unless commonly understood in the field.
  
- **Group related fields**: Whenever possible, group similar data fields under a containing attribute for organizational clarity. For example, group all aerodynamic parameters under a single data structure like ``analysis.aerodynamics``.

Following these conventions ensures that anyone reading the code will easily understand its purpose and functionality.


Project Structure and Modules
=============================

RCAIDE uses a modular approach to keep code organized and flexible. Sub-packages often mirror the main branches of functionality to separate data structures, analysis, and methods:

- **RCAIDE.Methods**: Contains Python functions used throughout the codebase.
- **RCAIDE.Analyses**: Houses objects and classes that manage analysis tasks (e.g., aerodynamic performance evaluations).
- **RCAIDE.Components**: Includes data structures representing physical components (e.g., wings, engines) or other major design elements.
- **RCAIDE.Attributes**: Holds data storage containers and reference data (e.g., standard atmospheres, material properties).

Aim to place your contributions in the most appropriate module. If you're uncertain, consider opening a discussion or posting on the forum (if available) to seek guidance from maintainers or other contributors.


Development Life Cycle
======================

Contributions typically evolve through these stages:

1. **Prototype**  
   Begin by experimenting in a separate branch or folder. Test your idea thoroughly before integrating it into RCAIDE’s main structure. Early on, you can focus on standalone functions or data structures using Python’s built-in types or a general-purpose data container.

2. **Initial Integration**  
   After confirming that your feature works and is well-tested, place it in the correct location within the RCAIDE code tree:
   
   - For standalone functions, consider placing them under ``RCAIDE.Methods``.
   - For analysis routines, use ``RCAIDE.Analyses`` and possibly create a new class or method that integrates with existing analyses.
   - For new components, leverage or create classes in ``RCAIDE.Components``.
   - For data containers or reference conditions, use or add files under ``RCAIDE.Attributes``.

   At this point, you may want to open a pull request (PR) on GitHub, including your tests and documentation. This allows maintainers and the community to review and provide feedback.

3. **Subpackages and Further Abstraction**  
   As your contributions grow in scope and complexity, you might factor them into a dedicated subpackage. Following the one-class-per-file rule and grouping related classes and methods is encouraged once your code reaches a level of maturity and abstraction that warrants its own modular structure.


Testing and Continuous Integration
==================================

Before submitting a PR, ensure that your changes pass all existing tests and add new tests if introducing functionality. Testing helps maintain code quality, catches regressions, and ensures that the code works as intended. RCAIDE’s test suite can be run locally; check the project documentation on how to run tests and interpret results.

The project uses continuous integration (CI) tools. 

Documentation and Examples
==========================

All new features, functions, and classes should be documented. This includes:

- **Docstrings**: Add clear, concise docstrings to all public classes, methods, and functions. Use `NumPy style docstrings <https://numpydoc.readthedocs.io/en/latest/format.html>`_ or `Google style docstrings <https://google.github.io/styleguide/pyguide.html>`_ for consistency.
  
- **User Guides and Tutorials**: If your contribution introduces significant new features, consider adding or updating tutorials and user guides in the documentation.
  
- **Examples**: Provide simple code snippets or example workflows demonstrating how to use your new features. This helps new users quickly understand how to apply your code to their problems.


Submitting a Pull Request
=========================

When you believe your contribution is ready:

1. Ensure your code follows the style guide and passes all tests.
2. Add or update documentation to reflect your changes.
3. Open a pull request on the project’s repository (e.g., GitHub). In your PR description:
   - Briefly summarize what your changes do.
   - Reference any related issues.
   - Provide guidance on how reviewers can test or evaluate your code.

A project maintainer will review your contribution, provide feedback, and guide you through any required revisions.


Questions and Support
=====================

If you have any questions or need help at any point in the contribution process, feel free to reach out through the project’s communication channels, such as:

- The project’s issue tracker on GitHub
- Github Discussions
- Slack

Your contributions are greatly appreciated, and we’re excited to work with you to improve RCAIDE!
