import io
from unittest import TestCase

from pyfwf.columns import CharColumn
from pyfwf.descriptors import DetailRowDescriptor, FileDescriptor
from pyfwf.readers import Reader


class TestReaderWithStringIO(TestCase):
    """Test Reader with StringIO"""

    def setUp(self):
        self.fd = FileDescriptor([DetailRowDescriptor([CharColumn("c1", 5), CharColumn("c2", 4)])])

    def test_stringio_direct(self):
        """Test reading from StringIO directly"""
        content = io.StringIO("AAAAA BBB\n")
        reader = Reader(content, self.fd, newline="\n")
        rows = list(reader)
        self.assertEqual(1, len(rows))
        self.assertEqual({"c1": "AAAAA", "c2": "BBB"}, rows[0])

    def test_stringio_multiple_lines(self):
        """Test reading multiple lines from StringIO"""
        content = io.StringIO("AAAAA BBB\nCCCCC DDD\n")
        reader = Reader(content, self.fd, newline="\n")
        rows = list(reader)
        self.assertEqual(2, len(rows))


class TestReaderEdgeCases(TestCase):
    """Test Reader edge cases"""

    def setUp(self):
        self.fd = FileDescriptor([DetailRowDescriptor([CharColumn("c1", 5), CharColumn("c2", 4)])])

    def test_line_counting(self):
        """Test line counting"""
        content = "AAAAA BBB\nCCCCC DDD\n"
        reader = Reader(content, self.fd, newline="\n")
        self.assertEqual(0, reader.line_num)
        next(reader)
        self.assertEqual(1, reader.line_num)
        next(reader)
        self.assertEqual(2, reader.line_num)

    def test_unsupported_iterable_type(self):
        """Test that Reader rejects unsupported iterable types"""
        # Tuple with one element per line works, but dict should not
        self.assertRaisesRegex(TypeError, "Unsupported Iterable", Reader, {}, self.fd)
