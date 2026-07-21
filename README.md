<!-- markdownlint-disable MD013 -->
# python-pyfwf

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![FWF Compliance](https://img.shields.io/badge/FWF_Compliance-5%2F5_cases_passed-brightgreen?logo=github)](https://github.com/fixed-width-file/fwf-compliance-tests)
[![QA](https://github.com/fixed-width-file/python-pyfwf/actions/workflows/qa.yml/badge.svg)](https://github.com/fixed-width-file/python-pyfwf/actions/workflows/qa.yml)
[![Coverage](https://codecov.io/gh/fixed-width-file/python-pyfwf/branch/main/graph/badge.svg)](https://codecov.io/gh/fixed-width-file/python-pyfwf)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

**python-pyfwf** is a fast, type-safe Python 3.9+ library for parsing, validating, and exporting **Fixed Width Files (FWF)**.

It is part of the [Fixed Width File Ecosystem](https://fixed-width-file.github.io/) and fully implements the **[fwf-compliance-tests v1.0.0](https://github.com/fixed-width-file/fwf-compliance-tests)** specification.

---

## 🌟 Key Features

- **Type-Safe Columns**: `CharColumn`, `RightCharColumn`, `PositiveIntegerColumn`, `PositiveDecimalColumn`, `DateColumn`, `TimeColumn`, and `DateTimeColumn`.
- **Flexible Descriptors**: Structured records with `HeaderRowDescriptor`, `DetailRowDescriptor`, and `FooterRowDescriptor`.
- **Multiple Output Renders**: Export layout specifications to Markdown, ReStructuredText (RST), or HTML tables via `RenderUtils`.
- **Full Test Suite & Compliance**: 100% compliant with `fwf-compliance-tests` v1.0.0.
- **Git Hooks Ready**: Pre-configured `pre-commit` and `pre-push` hooks.

---

## 🚀 Installation

Install via `pip`:

```bash
pip install pyfwf
```

---

## 💡 Quickstart

```python
from pyfwf.columns import CharColumn, PositiveIntegerColumn
from pyfwf.descriptors import DetailRowDescriptor, FileDescriptor
from pyfwf.readers import Reader

# 1. Define columns
name_col = CharColumn('name', 20, 'User Name')
age_col = PositiveIntegerColumn('age', 3, 'Age in years')

# 2. Define row and file descriptors
detail = DetailRowDescriptor([name_col, age_col])
file_descriptor = FileDescriptor([detail])

# 3. Read fixed-width file content
content = "KELSON MEDEIROS     045\nMARIA SILVA         030\n"
reader = Reader(content, file_descriptor, "\n")

for row in reader:
    print(f"Name: {row['name']} | Age: {row['age']}")
```

---

## 🧪 Testing & Compliance

Run all unit tests using pytest:

```bash
pytest
```

---

## ⚓ Pre-Commit & Pre-Push Setup

Set up pre-commit and pre-push hooks:

```bash
pre-commit install
pre-commit install --hook-type pre-push
```

Run checks manually:

```bash
pre-commit run --all-files
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
