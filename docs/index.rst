Home
====

Python library for reading and manipulating **fixed-width files (FWF)**.

.. image:: https://img.shields.io/badge/GitHub-Repository-blue?logo=github
   :target: https://github.com/kelsoncm/python-pyfwf
   :alt: GitHub Repository

.. image:: https://img.shields.io/badge/License-MIT-lemon.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License

.. image:: https://img.shields.io/pypi/pyversions/pyfwf.svg
   :target: https://pypi.org/project/pyfwf/
   :alt: Python

.. image:: https://github.com/kelsoncm/python-pyfwf/actions/workflows/qa.yml/badge.svg
   :target: https://github.com/kelsoncm/python-pyfwf/actions/workflows/qa.yml
   :alt: QA

.. image:: https://codecov.io/gh/kelsoncm/python-pyfwf/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/kelsoncm/python-pyfwf
   :alt: Coverage

.. image:: https://github.com/kelsoncm/python-pyfwf/actions/workflows/publish.yml/badge.svg
   :target: https://github.com/kelsoncm/python-pyfwf/actions/workflows/publish.yml
   :alt: Publish

.. image:: https://github.com/kelsoncm/python-pyfwf/actions/workflows/docs.yml/badge.svg
   :target: https://kelsoncm.github.io/python-pyfwf/
   :alt: Docs

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

What is a fixed-width file?
---------------------------

A fixed-width file (FWF) is a plain-text file where each field occupies a
predetermined number of characters in every line. Unlike CSV, there are
no delimiters — position and length define each column.

This library is necessary because large banks and the Brazilian government use a
batch file model that has 3 data blocks:

1. The **header** line identifies the file type, does not describe the file
   structure, and usually starts the line with the number 1 to indicate it
   is the header.
2. The **detail** contains the data and may have more than one type of detail.
   For example, if it starts with 2 it represents a state, if it starts with
   3 it represents a municipality of the state that came before it, and each
   type of detail has its own data structure.
3. The **footer** line signs the file, that is, it may have a line counter
   field or another field to validate if the file is complete, and usually
   starts the line with the number 9 to indicate it is the footer.

Thus, this library uses descriptors to define how the data should be read,
having **file**, **header**, **detail**, and **footer** descriptors.

Compare with others packages
----------------------------

- **pyfwf** offers an object-oriented API, support for typed columns
  (int, decimal, date, etc.), header/footer definition, and full test coverage.
  Ideal for scenarios that require validation and strict data structure.
- **fwf** and **microtrade-fwf** are simpler solutions, with fewer validation
  and configuration options, aimed at quick and basic usage.
- **petl-fwf** integrates FWF reading into the petl ecosystem, useful for ETL,
  but without a focus on type validation or detailed file structure.

.. code-block::none
    HDR SALES_REPORT                                   20240101
    D   Alice Smith                                    000001250
    D   Bob Jones                                      000000875
    FTR 00020000002125

Features
--------

- Read fixed-width format files with custom column definitions
- Support for typed columns: text, integer, decimal, date, time, datetime
- Header and footer row handling
- Render file descriptors as Markdown tables
- Serialise and deserialise file descriptors to/from JSON (hydration)
- 100% test coverage

Installation
------------

.. code-block:: bash

   pip install pyfwf

Requires Python 3.11+.

Quick example
-------------

.. code-block::python

    from pyfwf.columns import CharColumn, PositiveIntegerColumn, PositiveDecimalColumn
    from pyfwf.descriptors import DetailRowDescriptor, FileDescriptor
    from pyfwf.readers import Reader

    detail = DetailRowDescriptor([
        CharColumn('name', 30),
        PositiveIntegerColumn('age', 3),
        PositiveDecimalColumn('salary', 9, decimals=2),
    ])

    fd = FileDescriptor(details=[detail])

    with open('data.fwf', 'r') as f:
        reader = Reader(f, fd)
        for row in reader:
            print(row)
    # {'name': 'Alice Smith', 'age': 30, 'salary': 3500.00}

Next steps
----------

.. toctree::
   :maxdepth: 1

   getting-started
   contribute
   pyfwf
