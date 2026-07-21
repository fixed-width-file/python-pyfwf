from datetime import date, datetime, time
from unittest import TestCase

from pyfwf.columns import (
    CharColumn,
    DateColumn,
    DateTimeColumn,
    PositiveDecimalColumn,
    PositiveIntegerColumn,
    RightCharColumn,
    TimeColumn,
)


class TestCharColumn(TestCase):
    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, "missing 2", CharColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(CharColumn("type", 1, "desc"), CharColumn)

    def test_constructor_set_attr(self):
        cd = CharColumn("type", 2, "desc")
        self.assertEqual("type", cd.name)
        self.assertEqual(2, cd.size)
        self.assertEqual("desc", cd.description)

        cd2 = CharColumn("name", 1)
        self.assertEqual(1, cd2.size)
        self.assertEqual("name", cd2.description)

    def test_constructor_wrong_name_arg(self):
        self.assertRaises(TypeError, CharColumn, None, "", "")
        self.assertRaises(ValueError, CharColumn, "", "", "")
        self.assertRaises(ValueError, CharColumn, " ", "", "")

    def test_constructor_wrong_size_arg(self):
        self.assertRaises(TypeError, CharColumn, "name", "")
        self.assertRaises(ValueError, CharColumn, "name", 0)

    def test_constructor_wrong_description_arg(self):
        self.assertRaises(TypeError, CharColumn, "name", 1, 1)
        self.assertRaises(TypeError, CharColumn, "name", 1, False)

    def test_end(self):
        cd = CharColumn("name", 2, "desc")
        cd.start = 1
        self.assertEqual(2, cd.end)
        cd.start = 0
        with self.assertRaises(ValueError):
            _ = cd.end
        cd.start = "a"
        with self.assertRaises(TypeError):
            _ = cd.end

    def test_to_value_invalid(self):
        cd = CharColumn("name", 2, "desc")
        self.assertRaises(TypeError, cd.to_value, 1)
        self.assertRaises(ValueError, cd.to_value, "1")
        self.assertRaises(ValueError, cd.to_value, "333")

    def test_to_value_valid(self):
        cd = CharColumn("name", 2, "desc")
        self.assertEqual("22", cd.to_value("22"))
        self.assertEqual("2", cd.to_value("2 "))
        self.assertEqual("2", cd.to_value(" 2"))

    def test_to_str_invalid(self):
        cd = CharColumn("name", 4, "desc")
        self.assertRaises(TypeError, cd.to_str, 1)
        self.assertRaises(TypeError, cd.to_str, 12345)
        self.assertRaises(TypeError, cd.to_str, True)
        self.assertRaises(ValueError, cd.to_str, "12345")
        self.assertRaises(ValueError, cd.to_str, "123  ")

    def test_to_str_valid(self):
        cd = CharColumn("name", 4, "desc")
        self.assertEqual("asdf", cd.to_str("asdf"))
        self.assertEqual("a   ", cd.to_str("a "))
        self.assertEqual("    ", cd.to_str(""))
        self.assertEqual("    ", cd.to_str(" "))


class TestRightCharColumn(TestCase):
    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, "missing 2", RightCharColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(RightCharColumn("type", 2, "desc"), RightCharColumn)

    def test_constructor_set_attr(self):
        cd = RightCharColumn("type", 2, "desc")
        self.assertEqual("type", cd.name)
        self.assertEqual(2, cd.size)
        self.assertEqual("desc", cd.description)

        cd2 = RightCharColumn("name", 1)
        self.assertEqual(1, cd2.size)
        self.assertEqual("name", cd2.description)

    def test_constructor_wrong_name_arg(self):
        self.assertRaises(TypeError, RightCharColumn, None, "a")
        self.assertRaises(ValueError, RightCharColumn, "", "")
        self.assertRaises(ValueError, RightCharColumn, " ", "")

    def test_constructor_wrong_size_arg(self):
        self.assertRaises(TypeError, RightCharColumn, "name", "")
        self.assertRaises(ValueError, RightCharColumn, "name", 0)

    def test_constructor_wrong_description_arg(self):
        self.assertRaises(TypeError, RightCharColumn, "name", 1, 1)
        self.assertRaises(TypeError, RightCharColumn, "name", 1, False)

    def test_end(self):
        cd = RightCharColumn("name", 2, "desc")
        cd.start = 1
        self.assertEqual(2, cd.end)
        cd.start = 0
        with self.assertRaises(ValueError):
            _ = cd.end
        cd.start = "a"
        with self.assertRaises(TypeError):
            _ = cd.end

    def test_to_value_invalid(self):
        cd = RightCharColumn("name", 2, "desc")
        self.assertRaises(TypeError, cd.to_value, 1)
        self.assertRaises(TypeError, cd.to_value, 12345)
        self.assertRaises(TypeError, cd.to_value, True)
        self.assertRaises(ValueError, cd.to_value, "1")
        self.assertRaises(ValueError, cd.to_value, "333")

    def test_to_value_valid(self):
        cd = RightCharColumn("name", 2, "desc")
        self.assertEqual("22", cd.to_value("22"))
        self.assertEqual("2", cd.to_value("2 "))
        self.assertEqual("2", cd.to_value(" 2"))

    def test_to_str_invalid(self):
        cd = RightCharColumn("name", 4, "desc")
        self.assertRaises(TypeError, cd.to_str, 1)
        self.assertRaises(TypeError, cd.to_str, 12345)
        self.assertRaises(TypeError, cd.to_str, True)
        self.assertRaises(ValueError, cd.to_str, "12345")
        self.assertRaises(ValueError, cd.to_str, "123  ")

    def test_to_str_valid(self):
        cd = RightCharColumn("name", 4, "desc")
        self.assertEqual("asdf", cd.to_str("asdf"))
        self.assertEqual("  a ", cd.to_str("a "))
        self.assertEqual("   a", cd.to_str("a"))
        self.assertEqual("    ", cd.to_str(""))
        self.assertEqual("    ", cd.to_str(" "))
        self.assertEqual("    ", cd.to_str(None))


class TestPositiveIntegerColumn(TestCase):
    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, "missing 2", PositiveIntegerColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(PositiveIntegerColumn("type", 1, "desc"), PositiveIntegerColumn)

    def test_constructor_set_attr(self):
        cd = PositiveIntegerColumn("type", 2, "the type")
        self.assertEqual("type", cd.name)
        self.assertEqual(2, cd.size)
        self.assertEqual("the type", cd.description)

        cd2 = PositiveIntegerColumn("name", 1)
        self.assertEqual(1, cd2.size)
        self.assertEqual("name", cd2.name)
        self.assertEqual(cd2.name, cd2.description)

    def test_constructor_wrong_name_arg(self):
        self.assertRaises(TypeError, PositiveIntegerColumn, None, "a", "a")
        self.assertRaises(ValueError, PositiveIntegerColumn, "", "", "")
        self.assertRaises(ValueError, PositiveIntegerColumn, " ", "", "")

    def test_constructor_wrong_size_arg(self):
        self.assertRaises(TypeError, PositiveIntegerColumn, "name", "")
        self.assertRaises(ValueError, PositiveIntegerColumn, "name", 0)

    def test_constructor_wrong_description_arg(self):
        self.assertRaises(TypeError, PositiveIntegerColumn, "name", 1, 1)
        self.assertRaises(TypeError, PositiveIntegerColumn, "name", 1, False)

    def test_end(self):
        cd = PositiveIntegerColumn("name", 2, "desc")
        cd.start = 1
        self.assertEqual(2, cd.end)

    def test_to_value_invalid(self):
        cd = PositiveIntegerColumn("name", 2, "desc")
        self.assertRaises(TypeError, cd.to_value, 12)
        self.assertRaises(TypeError, cd.to_value, True)
        self.assertRaises(ValueError, cd.to_value, "1")
        self.assertRaises(ValueError, cd.to_value, "-1")
        self.assertRaises(ValueError, cd.to_value, "333")
        self.assertRaises(ValueError, cd.to_value, "A1")

    def test_to_value_valid(self):
        cd = PositiveIntegerColumn("name", 2, "desc")
        self.assertEqual(22, cd.to_value("22"))
        self.assertEqual(2, cd.to_value("2 "))
        self.assertEqual(2, cd.to_value(" 2"))

    def test_to_str_invalid(self):
        cd = PositiveIntegerColumn("name", 4, "desc")
        self.assertRaises(TypeError, cd.to_str, "1")
        self.assertRaises(TypeError, cd.to_str, "-123")
        self.assertRaises(TypeError, cd.to_str, "12345")
        self.assertRaises(TypeError, cd.to_str, True)
        self.assertRaises(TypeError, cd.to_str, -1)
        self.assertRaises(ValueError, cd.to_str, 12345)

    def test_to_str_valid(self):
        cd = PositiveIntegerColumn("name", 4, "year")
        self.assertEqual("0001", cd.to_str(1))
        self.assertEqual("1234", cd.to_str(1234))
        self.assertEqual("0000", cd.to_str(0))
        self.assertEqual("0000", cd.to_str(None))


class TestPositiveDecimalColumn(TestCase):
    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, "missing 2", PositiveDecimalColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(PositiveDecimalColumn("type", 3), PositiveDecimalColumn)
        self.assertIsInstance(PositiveDecimalColumn("type", 3, 2), PositiveDecimalColumn)
        self.assertIsInstance(PositiveDecimalColumn("type", 3, 2, "desc"), PositiveDecimalColumn)

    def test_constructor_set_attr(self):
        cd2 = PositiveDecimalColumn("value", 4)
        self.assertEqual(4, cd2.size)
        self.assertEqual("value", cd2.description)

        cd2 = PositiveDecimalColumn("value", 4, 2)
        self.assertEqual(4, cd2.size)
        self.assertEqual("value", cd2.description)

    def test_constructor_wrong_name_arg(self):
        self.assertRaises(TypeError, PositiveDecimalColumn, None, "a", "a")
        self.assertRaises(ValueError, PositiveDecimalColumn, "", "", "")
        self.assertRaises(ValueError, PositiveDecimalColumn, " ", "", "")

    def test_constructor_wrong_size_arg(self):
        self.assertRaises(TypeError, PositiveDecimalColumn, "name", "")
        self.assertRaises(ValueError, PositiveDecimalColumn, "name", 0)

    def test_constructor_wrong_decimals_args(self):
        self.assertRaises(TypeError, PositiveDecimalColumn, "name", 1, "1")
        self.assertRaises(ValueError, PositiveDecimalColumn, "value", 1, 0)
        self.assertRaises(ValueError, PositiveDecimalColumn, "value", 1)
        self.assertRaises(ValueError, PositiveDecimalColumn, "value", 1, 2)
        self.assertRaises(ValueError, PositiveDecimalColumn, "value", 1, 1)
        self.assertRaises(ValueError, PositiveDecimalColumn, "value", 1, 0)

    def test_constructor_wrong_description_arg(self):
        self.assertRaises(TypeError, PositiveDecimalColumn, "name", 3, 1, -1)
        self.assertRaises(TypeError, PositiveDecimalColumn, "name", 3, 1, False)

    def test_end(self):
        cd = PositiveDecimalColumn("name", 2, 1, "desc")
        cd.start = 1
        self.assertEqual(2, cd.end)

    def test_to_value_invalid(self):
        cd = PositiveDecimalColumn("name", 2, 1, "desc")
        self.assertRaises(TypeError, cd.to_value, 12)
        self.assertRaises(TypeError, cd.to_value, -1.0)
        self.assertRaises(TypeError, cd.to_value, True)
        self.assertRaises(ValueError, cd.to_value, "1")
        self.assertRaises(ValueError, cd.to_value, "-1")
        self.assertRaises(ValueError, cd.to_value, "333")
        self.assertRaises(ValueError, cd.to_value, "A1")

    def test_to_value_valid(self):
        cd = PositiveDecimalColumn("value", 3, 2)
        self.assertEqual(1.23, cd.to_value("123"))
        self.assertEqual(0.01, cd.to_value("1  "))
        self.assertEqual(0.02, cd.to_value(" 2 "))
        self.assertEqual(0.03, cd.to_value("  3"))

    def test_to_str_invalid(self):
        cd = PositiveDecimalColumn("value", 4, 2)
        self.assertRaises(TypeError, cd.to_str, "1")
        self.assertRaises(TypeError, cd.to_str, "-123")
        self.assertRaises(TypeError, cd.to_str, "12345")
        self.assertRaises(TypeError, cd.to_str, True)
        self.assertRaises(TypeError, cd.to_str, -1)
        self.assertRaises(ValueError, cd.to_str, 123.45)
        self.assertRaises(ValueError, cd.to_str, 123.0)
        self.assertRaises(ValueError, cd.to_str, 1234.0)

    def test_to_str_valid(self):
        cd = PositiveDecimalColumn("value", 4)
        self.assertEqual("0100", cd.to_str(1.0))
        self.assertEqual("1234", cd.to_str(12.34))
        self.assertEqual("0000", cd.to_str(0.0))
        self.assertEqual("0012", cd.to_str(0.12))
        self.assertEqual("0010", cd.to_str(0.1))
        self.assertEqual("0000", cd.to_str(None))


class TestDateTimeColumn(TestCase):
    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, "missing 1", DateTimeColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(DateTimeColumn("type"), DateTimeColumn)
        self.assertIsInstance(DateTimeColumn("type", "%d%m%Y%H%M"), DateTimeColumn)
        self.assertIsInstance(DateTimeColumn("type", "%d%m%Y%H%M", "desc"), DateTimeColumn)

    def test_constructor_set_attr(self):
        cd2 = DateTimeColumn("dt")
        self.assertEqual(12, cd2.size)
        self.assertEqual("dt", cd2.description)

        cd2 = DateTimeColumn("dt", "%d%m%Y%H%M")
        self.assertEqual(12, cd2.size)
        self.assertEqual("dt", cd2.description)

    def test_constructor_wrong_name_arg(self):
        self.assertRaises(TypeError, DateTimeColumn, None, "a", "a")
        self.assertRaises(ValueError, DateTimeColumn, "", "")
        self.assertRaises(ValueError, DateTimeColumn, " ", "")

    def test_constructor_wrong_format_arg(self):
        self.assertRaises(TypeError, DateTimeColumn, "dt", None)
        self.assertRaises(ValueError, DateTimeColumn, "dt", "")
        self.assertRaises(ValueError, DateTimeColumn, "dt", " ")
        self.assertRaises(ValueError, DateTimeColumn, "dt", "%d%m%Y%H")

    def test_constructor_wrong_description_arg(self):
        self.assertRaises(TypeError, DateTimeColumn, "dt", description=1)
        self.assertRaises(TypeError, DateTimeColumn, "dt", description=False)

    def test_end(self):
        cd = DateTimeColumn("dt")
        cd.start = 1
        self.assertEqual(12, cd.end)

    def test_to_value_invalid(self):
        cd = DateTimeColumn("dt")
        self.assertRaises(TypeError, cd.to_value, 12)
        self.assertRaises(TypeError, cd.to_value, -1.0)
        self.assertRaises(TypeError, cd.to_value, True)
        self.assertRaises(ValueError, cd.to_value, "1")
        self.assertRaises(ValueError, cd.to_value, "310220010000")

    def test_to_value_valid(self):
        cd = DateTimeColumn("dt")
        self.assertEqual(datetime(2001, 2, 28, 0, 0), cd.to_value("280220010000"))

        cd = DateTimeColumn("dt", "%d%m%y%H%M")
        self.assertEqual(datetime(2001, 2, 28, 0, 0), cd.to_value("2802010000"))

    def test_to_str_invalid(self):
        cd = DateTimeColumn("dt")
        self.assertRaises(TypeError, cd.to_str, 1)
        self.assertRaises(TypeError, cd.to_str, 1.1)
        self.assertRaises(TypeError, cd.to_str, False)
        self.assertRaises(TypeError, cd.to_str, "123")
        self.assertRaises(TypeError, cd.to_str, "1234567890123")
        self.assertRaises(TypeError, cd.to_str, date.today())
        self.assertRaises(TypeError, cd.to_str, datetime.now().time())

    def test_to_str_valid(self):
        self.assertEqual("280220012359", DateTimeColumn("dt").to_str(datetime(2001, 2, 28, 23, 59)))
        self.assertEqual("000000000000", DateTimeColumn("dt").to_str(None))
        self.assertEqual(
            "2802012359",
            DateTimeColumn("dt", "%d%m%y%H%M").to_str(datetime(2001, 2, 28, 23, 59)),
        )


class TestDateColumn(TestCase):
    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, "missing 1", DateColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(DateColumn("type"), DateColumn)
        self.assertIsInstance(DateColumn("type", "%d%m%Y"), DateColumn)
        self.assertIsInstance(DateColumn("type", "%d%m%Y", "desc"), DateColumn)

    def test_constructor_set_attr(self):
        cd2 = DateColumn("dt")
        self.assertEqual(8, cd2.size)
        self.assertEqual("dt", cd2.description)

        cd2 = DateColumn("dt", "%d%m%y")
        self.assertEqual(6, cd2.size)
        self.assertEqual("dt", cd2.description)

    def test_constructor_wrong_name_arg(self):
        self.assertRaises(TypeError, DateColumn, None, "a", "a")
        self.assertRaises(ValueError, DateColumn, "", "")
        self.assertRaises(ValueError, DateColumn, " ", "")

    def test_constructor_wrong_format_args(self):
        self.assertRaises(TypeError, DateColumn, "name", 0)
        self.assertRaises(TypeError, DateColumn, "name", None)
        self.assertRaises(ValueError, DateColumn, "name", "")
        self.assertRaises(ValueError, DateColumn, "name", " ")
        self.assertRaises(ValueError, DateColumn, "name", "%d%m%Y%H")

    def test_constructor_wrong_description_arg(self):
        self.assertRaises(TypeError, DateColumn, "dt", description=1)
        self.assertRaises(TypeError, DateColumn, "dt", description=False)

    def test_end(self):
        cd = DateColumn("dt")
        cd.start = 1
        self.assertEqual(8, cd.end)

    def test_to_value_invalid(self):
        cd = DateColumn("dt")
        self.assertRaises(TypeError, cd.to_value, 12)
        self.assertRaises(TypeError, cd.to_value, -1.0)
        self.assertRaises(TypeError, cd.to_value, True)
        self.assertRaises(ValueError, cd.to_value, "1")
        self.assertRaises(ValueError, cd.to_value, "12345678")

    def test_to_value_valid(self):
        self.assertEqual(date(2001, 2, 28), DateColumn("dt").to_value("28022001"))
        self.assertEqual(date(2001, 2, 28), DateColumn("dt", "%d%m%y").to_value("280201"))

    def test_to_str_invalid(self):
        cd = DateColumn("dt")
        self.assertRaises(TypeError, cd.to_str, 1)
        self.assertRaises(TypeError, cd.to_str, 1.1)
        self.assertRaises(TypeError, cd.to_str, False)
        self.assertRaises(TypeError, cd.to_str, "123")
        self.assertRaises(TypeError, cd.to_str, "1234567890123")
        self.assertRaises(TypeError, cd.to_str, datetime.now().time())

    def test_to_str_valid(self):
        self.assertEqual("28022001", DateColumn("dt").to_str(date(2001, 2, 28)))
        self.assertEqual("28022001", DateColumn("dt").to_str(datetime(2001, 2, 28, 23, 59)))
        self.assertEqual("280201", DateColumn("dt", "%d%m%y").to_str(date(2001, 2, 28)))


class TestTimeColumn(TestCase):
    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, "missing 1", TimeColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(TimeColumn("type"), TimeColumn)
        self.assertIsInstance(TimeColumn("type", "%H:%M"), TimeColumn)

    def test_constructor_set_attr(self):
        cd2 = TimeColumn("time")
        self.assertEqual(4, cd2.size)
        self.assertEqual("time", cd2.description)

        cd2 = TimeColumn("time", "%H:%M")
        self.assertEqual(5, cd2.size)
        self.assertEqual("time", cd2.description)

    def test_constructor_wrong_name_arg(self):
        self.assertRaises(TypeError, TimeColumn, None, "a", "a")
        self.assertRaises(ValueError, TimeColumn, "", "")
        self.assertRaises(ValueError, TimeColumn, " ", "")

    def test_constructor_wrong_format_args(self):
        self.assertRaises(TypeError, TimeColumn, "time", 0)
        self.assertRaises(TypeError, TimeColumn, "time", None)
        self.assertRaises(ValueError, TimeColumn, "time", "")
        self.assertRaises(ValueError, TimeColumn, "time", " ")
        self.assertRaises(ValueError, TimeColumn, "time", "%d%m%Y%H")

    def test_constructor_wrong_description_arg(self):
        self.assertRaises(TypeError, TimeColumn, "time", description=1)
        self.assertRaises(TypeError, TimeColumn, "time", description=False)

    def test_end(self):
        cd = TimeColumn("time")
        cd.start = 1
        self.assertEqual(4, cd.end)

        cd = TimeColumn("time", "%H:%M")
        cd.start = 1
        self.assertEqual(5, cd.end)

    def test_to_value_invalid(self):
        cd = TimeColumn("time")
        self.assertRaises(TypeError, cd.to_value, 12)
        self.assertRaises(TypeError, cd.to_value, -1.0)
        self.assertRaises(TypeError, cd.to_value, True)
        self.assertRaises(ValueError, cd.to_value, "1")
        self.assertRaises(ValueError, cd.to_value, "7894")

    def test_to_value_valid(self):
        self.assertEqual(time(23, 59), TimeColumn("time").to_value("2359"))
        self.assertEqual(time(23, 59), TimeColumn("time", "%H:%M").to_value("23:59"))

    def test_to_str_invalid(self):
        cd = TimeColumn("time")
        self.assertRaises(TypeError, cd.to_str, 1)
        self.assertRaises(TypeError, cd.to_str, 1.1)
        self.assertRaises(TypeError, cd.to_str, False)
        self.assertRaises(TypeError, cd.to_str, "123")
        self.assertRaises(TypeError, cd.to_str, "1234567890123")
        self.assertRaises(TypeError, cd.to_str, date.today())

    def test_to_str_valid(self):
        self.assertEqual("2359", TimeColumn("time").to_str(time(23, 59)))
        self.assertEqual("23:59", TimeColumn("time", "%H:%M").to_str(time(23, 59)))
