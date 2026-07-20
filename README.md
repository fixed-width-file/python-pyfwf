# Python FWF

[![License](https://img.shields.io/badge/License-MIT-lemon.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/pypi/pyversions/pyfwf.svg)](https://pypi.org/project/pyfwf/)
[![QA](https://github.com/kelsoncm/python-pyfwf/actions/workflows/qa.yml/badge.svg)](https://github.com/kelsoncm/python-pyfwf/actions/workflows/qa.yml)
[![Coverage](https://codecov.io/gh/kelsoncm/python-pyfwf/branch/main/graph/badge.svg)](https://codecov.io/gh/kelsoncm/python-pyfwf)
[![Docs](https://github.com/kelsoncm/python-pyfwf/actions/workflows/docs.yml/badge.svg)](https://kelsoncm.github.io/python-pyfwf/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

Python library for reading and manipulating **fixed width files (FWF)**.

> See each package's [documentation](https://kelsoncm.github.io/python-pyfwf/)
> for details and usage examples.

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

## Compare with others packages

<!-- markdownlint-disable MD013 -->
| Package                                                    | Main Focus / Features                                                                   | API Style    | Typed Columns | Header/Footer | Documentation | Test Coverage |
|------------------------------------------------------------|-----------------------------------------------------------------------------------------|--------------|---------------|---------------|---------------|---------------|
| **pyfwf**                                                  | Flexible, typed columns, descriptors, header/footer, 100% coverage                      | Pythonic/OOP | Yes           | Yes           | Extensive     | 100%          |
| [fwf](https://pypi.org/project/fwf/)                       | Simple FWF reader/writer, minimal configuration                                         | Functional   | No            | No            | Minimal       | Unknown       |
| [microtrade-fwf](https://pypi.org/project/microtrade-fwf/) | Basic FWF parsing, focused on simplicity, limited features                              | Functional   | No            | No            | Minimal       | Unknown       |
| [petl-fwf](https://pypi.org/project/petl-fwf/)             | FWF support as part of [petl](https://petl.readthedocs.io/) ETL toolkit, table-oriented | Table/ETL    | No            | No            | Good (petl)   | Good (petl)   |
<!-- markdownlint-enable MD013 -->

**Summary of differences:**

- **pyfwf** offers an object-oriented API, support for typed columns
  (int, decimal, date, etc.), header/footer definition, and full test coverage.
  Ideal for scenarios that require validation and strict data structure.
- **fwf** and **microtrade-fwf** are simpler solutions, with fewer validation
  and configuration options, aimed at quick and basic usage.
- **petl-fwf** integrates FWF reading into the petl ecosystem, useful for ETL,
  but without a focus on type validation or detailed file structure.

## Features

- 📖 Read fixed-width format files with custom column definitions
- 🔧 Support for typed columns (integer, decimal, date, time, etc.)
- 📋 Header and footer row handling
- 🎯 Simple and intuitive API
- ✅ Fully tested (100% coverage)

## Installation

```bash
pip install pyfwf
```

## Quick Start

```python
from pyfwf.columns import CharColumn, PositiveIntegerColumn
from pyfwf.descriptors import DetailRowDescriptor, FileDescriptor
from pyfwf.readers import Reader

# Define columns
detail = DetailRowDescriptor([
    CharColumn(name='name', pos=1, size=20),
    PositiveIntegerColumn(name='age', pos=21, size=3),
])

# Create file descriptor
fd = FileDescriptor(line_size=23, details=[detail])

# Read file
with open('data.fwf', 'r') as f:
    reader = Reader(f, fd)
    for row in reader:
        print(row)
```

## Development & Pre-commit Hooks

This project uses [`pre-commit`](https://pre-commit.com/) to enforce
code quality, linting, formatting, and unit tests before committing and pushing.

### Installing Git Hooks

To set up the pre-commit and pre-push hooks locally:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit and pre-push hooks
pre-commit install
pre-commit install --hook-type pre-push
```

### Running Hooks Manually

You can execute the hooks manually against all files at any time:

```bash
# Run commit-stage hooks (Black, Ruff, doc8, markdownlint, whitespace)
pre-commit run --all-files

# Run push-stage hooks (pytest & 100% coverage gate)
pre-commit run --hook-stage pre-push --all-files
```

## Security

Please report vulnerabilities according to [SECURITY.md](SECURITY.md).

## Author

Kelson da Costa Medeiros <kelsoncm@gmail.com>
