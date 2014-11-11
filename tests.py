#  bdateutil
#  ---------
#  Adds business day logic and improved data type flexibility to
#  python-dateutil. 100% backwards compatible with python-dateutil,
#  simply replace dateutil imports with bdateutil.
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/bdateutil
#  License: MIT (see LICENSE file)


import unittest
from datetime import date, datetime

import holidays

from bdateutil import isbday
from bdateutil import relativedelta
from bdateutil import parse
from bdateutil.rrule import *

from testdateutil import *


class TestIsBday(unittest.TestCase):

    def test_isbday(self):
        self.assertFalse(isbday(date(2014, 1, 4)))
        self.assertTrue(isbday(date(2014, 1, 1)))
        self.assertFalse(isbday(date(2014, 1, 1), holidays=holidays.US()))


class TestRelativeDelta(unittest.TestCase):

    def test_init(self):
        self.assertEqual(relativedelta(date(2014, 1, 7), date(2014, 1, 3)),
                         relativedelta(days=4, bdays=2))
        self.assertEqual(relativedelta(date(2014, 1, 31), date(2014, 1, 1)),
                         relativedelta(days=30, bdays=22))
        self.assertEqual(relativedelta(date(2014, 2, 1), date(2014, 1, 1)),
                         relativedelta(months=1, bdays=23))
        self.assertEqual(relativedelta(date(2014, 2, 2), date(2014, 1, 1)),
                         relativedelta(months=1, days=1, bdays=23))
        self.assertEqual(relativedelta(date(2014, 1, 1), date(2014, 2, 2)),
                         relativedelta(months=-1, days=-1, bdays=-23))

    def test_add(self):
        rd1 = relativedelta(years=+1, months=+2, bdays=+3, days=+4)
        rd2 = relativedelta(years=+2, months=-3, bdays=+4, days=+5)
        rd3 = relativedelta(years=+3, months=-1, bdays=+7, days=+9)
        self.assertEqual(rd1 + rd2, rd3)
        self.assertEqual(relativedelta(bdays=3) + date(2014, 1, 3),
                         date(2014, 1, 8))
        rd4 = relativedelta(years=+1, months=+2, days=+1)
        rd5 = relativedelta(years=+4, months=+1, bdays=+7, days=+10)
        self.assertEqual(rd3 + rd4, rd5)
        self.assertEqual("2014-01-01" + relativedelta(weekday=FR),
                         datetime(2014, 1, 3))

    def test_radd(self):
        self.assertEqual(date(2014, 1, 3) + relativedelta(bdays=2),
                         date(2014, 1, 7))
        self.assertEqual(date(2014, 1, 7) + relativedelta(bdays=-2),
                         date(2014, 1, 3))
        self.assertEqual(date(2014, 2, 3) + relativedelta(bdays=-19),
                         date(2014, 1, 7))

    def test_sub(self):
        rd1 = relativedelta(years=+1, months=+2, bdays=+3, days=+4)
        rd2 = relativedelta(years=+2, months=-3, bdays=+4, days=+5)
        rd3 = relativedelta(years=-1, months=+5, bdays=-1, days=-1)
        self.assertEqual(rd1 - rd2, rd3)

    def test_rsub(self):
        self.assertEqual(date(2014, 1, 7) - relativedelta(bdays=2),
                         date(2014, 1, 3))
        self.assertEqual(date(2014, 1, 3) - relativedelta(bdays=-2),
                         date(2014, 1, 7))
        self.assertEqual(date(2014, 2, 3) - relativedelta(bdays=19),
                         date(2014, 1, 7))

    def test_neg(self):
        self.assertEqual(-relativedelta(years=+1, bdays=-3),
                         relativedelta(years=-1, bdays=+3))

    def test_bool(self):
        self.assertTrue(relativedelta(bdays=1))
        self.assertTrue(relativedelta(days=1))
        self.assertFalse(relativedelta())

    def test_mul(self):
        self.assertEqual(relativedelta(years=+1, bdays=-3) * 3,
                         relativedelta(years=+3, bdays=-9))
        self.assertEqual(relativedelta(years=+1, bdays=-3) * -3,
                         relativedelta(years=-3, bdays=+9))
        self.assertEqual(relativedelta(years=+1, bdays=-3) * 0,
                         relativedelta(years=0, bdays=0))

    def test_rmul(self):
        self.assertEqual(3 * relativedelta(years=+1, bdays=-3),
                         relativedelta(years=+3, bdays=-9))
        self.assertEqual(-3 * relativedelta(years=+1, bdays=-3),
                         relativedelta(years=-3, bdays=+9))
        self.assertEqual(0 * relativedelta(years=+1, bdays=-3),
                         relativedelta(years=0, bdays=0))

    def test_eq(self):
        r1 = relativedelta(years=1, months=2, days=3, bdays=1,
                           hours=4, minutes=5, seconds=6, microseconds=7)
        r2 = relativedelta(years=1, months=2, days=3, bdays=1,
                           hours=4, minutes=5, seconds=6, microseconds=7)
        self.assertEqual(r1, r2)
        self.assertTrue(r1 == r2)
        r2.days = 4
        self.assertNotEqual(r1, r2)
        self.assertFalse(r1 == r2)
        r2.days = 3
        r2.bdays = 0
        self.assertNotEqual(r1, r2)
        self.assertFalse(r1 == r2)
        self.assertEqual(relativedelta(), relativedelta())
        self.assertTrue(relativedelta() == relativedelta())
        self.assertNotEqual(relativedelta(days=1), relativedelta(bdays=1))
        self.assertFalse(relativedelta() == relativedelta(months=1))
        self.assertNotEqual(relativedelta(days=1), relativedelta(bdays=1))
        self.assertFalse(relativedelta() == relativedelta(months=1))

    def test_ne(self):
        r1 = relativedelta(years=1, months=2, days=3, bdays=1,
                           hours=4, minutes=5, seconds=6, microseconds=7)
        r2 = relativedelta(years=1, months=2, days=3, bdays=1,
                           hours=4, minutes=5, seconds=6, microseconds=7)
        self.assertFalse(r1 != r2)
        r2.days = 4
        self.assertTrue(r1 != r2)
        r2.days = 3
        r2.bdays = 0
        self.assertTrue(r1 != r2)
        self.assertFalse(relativedelta() != relativedelta())
        self.assertTrue(relativedelta() != relativedelta(months=1))
        self.assertTrue(relativedelta() != relativedelta(months=1))

    def test_div(self):
        self.assertEqual(relativedelta(years=+3, bdays=-9) / 3,
                         relativedelta(years=+1, bdays=-3))
        self.assertEqual(relativedelta(years=+3, bdays=-9) / -3,
                         relativedelta(years=-1, bdays=+3))
        self.assertRaises(ZeroDivisionError,
                          lambda: relativedelta(bdays=-3) / 0)

    def test_truediv(self):
        self.assertEqual(relativedelta(years=+4, bdays=-10) / 3.0,
                         relativedelta(years=+1, bdays=-3))

    def test_repr(self):
        rd1 = relativedelta(years=+1, months=+2, days=-3)
        self.assertEqual(str(rd1),
                         "relativedelta(years=+1, months=+2, days=-3)")
        rd2 = relativedelta(years=+1, months=+2, bdays=-7)
        self.assertEqual(str(rd2),
                         "relativedelta(years=+1, months=+2, bdays=-7)")
        rd3 = relativedelta(years=-1, months=-2, bdays=+7)
        self.assertEqual(str(rd3),
                         "relativedelta(years=-1, months=-2, bdays=+7)")
        rd4 = relativedelta(year=2014, month=1, day=2)
        self.assertEqual(str(rd4),
                         "relativedelta(year=2014, month=1, day=2)")


class TestParser(unittest.TestCase):

    def test_timestamp(self):
        self.assertEqual(parse(1388577600).date(), date(2014, 1, 1))

    def test_parserinfo(self):
        self.assertEqual(parse("1/2/2014"), datetime(2014, 1, 2))
        self.assertEqual(parse(b"1/2/2014"), datetime(2014, 1, 2))
        self.assertEqual(parse("1/2/2014", dayfirst=True),
                         datetime(2014, 2, 1))
        self.assertEqual(parse("1/2/2014", parserinfo(dayfirst=True)),
                         datetime(2014, 2, 1))

    def test_exceptions(self):
        self.assertRaises(ValueError, lambda: parse("abc"))
        self.assertRaises(TypeError, lambda: parse(['a', 'b', 'c']))


class TestRRule(unittest.TestCase):

    def test_bdaily(self):
        start = parse("2014-01-01")
        self.assertEqual(list(rrule(BDAILY, count=4, dtstart=start)),
                         [datetime(2014, 1, 1, 0, 0),
                          datetime(2014, 1, 2, 0, 0),
                          datetime(2014, 1, 3, 0, 0),
                          datetime(2014, 1, 6, 0, 0)])

    def test_parse(self):
        self.assertEqual(list(rrule(BDAILY, count=4, dtstart="2014-01-01")),
                         [datetime(2014, 1, 1, 0, 0),
                          datetime(2014, 1, 2, 0, 0),
                          datetime(2014, 1, 3, 0, 0),
                          datetime(2014, 1, 6, 0, 0)])
        self.assertEqual(list(rrule(BDAILY, count=4, dtstart="2014-01-01",
                                    until="01/04/2014")),
                         [datetime(2014, 1, 1, 0, 0),
                          datetime(2014, 1, 2, 0, 0),
                          datetime(2014, 1, 3, 0, 0)])


if __name__ == "__main__":
    unittest.main()
