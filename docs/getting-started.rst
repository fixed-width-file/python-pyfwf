Getting Started
===============

Installation
----------------

.. code-block::bash
    pip install pyfwf

Requires Python **3.11 or later**.

Understanding the file structure
--------------------------------

A fixed-width file has one or more of these row types:

======================= ====================================================
Row type                Role
======================= ====================================================
**Header**              First line with metadata (file date, type, etc.)
**Detail**              Data lines — can have multiple layouts
**Footer**              Last line with summary data (record counts, totals)
======================= ====================================================

All rows in a file share the same line length.


Step 1 — Define your columns
----------------------------

Each column is an instance of a typed class from `pyfwf.columns`.
The first argument is the field name, the second is the width in characters.

.. code-block::python
    from pyfwf.columns import (
        CharColumn,
        RightCharColumn,
        PositiveIntegerColumn,
        PositiveDecimalColumn,
        DateColumn,
        TimeColumn,
        DateTimeColumn,
    )

    header_cols = [
        CharColumn('row_type', 1),
        CharColumn('file_type', 5),
        CharColumn('fill', 157),
    ]

    detail_cols = [
        CharColumn('row_type', 1),
        CharColumn('name', 60),
        RightCharColumn('right_name', 60),
        PositiveIntegerColumn('age', 9),
        PositiveDecimalColumn('salary', 9, decimals=2),
        DateTimeColumn('created_at', '%d%m%Y%H%M'),
        DateColumn('birth_date', '%d%m%Y'),
        TimeColumn('check_in', '%H%M'),
    ]

    footer_cols = [
        CharColumn('row_type', 1),
        PositiveIntegerColumn('detail_count', 4),
        PositiveIntegerColumn('row_count', 4),
        CharColumn('fill', 154),
    ]

Step 2 — Define your row descriptors
------------------------------------

Wrap each column list in the matching descriptor class from `pyfwf.descriptors`.

.. code-block::python
    from pyfwf.descriptors import (
        HeaderRowDescriptor,
        DetailRowDescriptor,
        FooterRowDescriptor,
        FileDescriptor,
    )

    header = HeaderRowDescriptor(header_cols)
    detail = DetailRowDescriptor(detail_cols)
    footer = FooterRowDescriptor(footer_cols)

Then create a `FileDescriptor` that ties them together:

.. code-block::python
    fd = FileDescriptor(
        details=[detail],
        header=header,
        footer=footer,
    )

`header` and `footer` are optional. `details` must contain at least one `DetailRowDescriptor`.


Step 3 — Read the file
----------------------

Pass an open file (or string, `StringIO`, or list of lines) and the `FileDescriptor` to `Reader`.

.. code-block::python
    from pyfwf.readers import Reader

    with open('data.fwf', 'r') as f:
        reader = Reader(f, fd)
        for row in reader:
            print(row)


Each `row` is a plain `dict` mapping column names to typed Python values:

.. code-block::python
    {
        'row_type': 'D',
        'name': 'Alice Smith',
        'right_name': 'Alice Smith',
        'age': 30,
        'salary': 1234.56,
        'created_at': datetime(2024, 1, 15, 9, 30),
        'birth_date': date(1994, 3, 22),
        'check_in': time(9, 30),
    }


Step 4 — Write values back (to_str)
-----------------------------------

Each column also knows how to serialise a Python value back to a fixed-width string:

.. code-block::python
    col = CharColumn('name', 20)
    col.start = 1
    col.to_str('Alice Smith')   # 'Alice Smith         '

    col2 = PositiveDecimalColumn('price', 9, decimals=2)
    col2.start = 1
    col2.to_str(12.50)          # '000001250'

Rendering a Markdown table
--------------------------

You can render a `FileDescriptor` as a Markdown table — useful for documentation:

.. code-block::python
    from io import StringIO
    from pyfwf.renders import render_as_markdown

    buf = StringIO()
    render_as_markdown(fd, buf)
    print(buf.getvalue())

Output:

.. code-block::none
    |    # | Column    | Size | Start |  End | Type       | Description
    | ---- | --------- | ---- | ----- | ---- | ---------- | -----------
    |    1 | row_type  |    1 |     1 |    1 | CharColumn | row_type
    ...

    # DETAILS 1

    |    # | Column    | Size | Start |  End | Type       | Description


## Supported input types for Reader

============================= ============================================
Input type Notes
============================= ============================================
**TextIOWrapper** (open file) Standard file object
**StringIO**                  In-memory text stream
**str**                       Raw string content
**list**                      List of raw line strings
============================= ============================================

The `newline` argument defaults to `"\n\r"`. Pass `"\n"` or `"\r"` if your file uses a different line ending.
