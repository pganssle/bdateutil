#  bdateutil
#  ---------
#  Adds business day logic and improved data type flexibility to
#  python-dateutil. 100% backwards compatible with python-dateutil,
#  simply replace dateutil imports with bdateutil.
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/bdateutil
#  License: MIT (see LICENSE file)


import datetime as dt
import unittest

import holidays


from bdateutil import isbday
from bdateutil import relativedelta
from bdateutil import parse
from bdateutil.rrule import *
from bdateutil import date, datetime

from testdateutil import *


class TestIsBday(unittest.TestCase):

    def test_isbday(self):
        self.assertFalse(isbday(date(2014, 1, 4)))
        self.assertFalse(isbday("2014-01-04"))
        self.assertTrue(isbday(date(2014, 1, 1)))
        self.assertTrue(isbday("2014-01-01"))
        self.assertFalse(isbday(date(2014, 1, 1), holidays=holidays.US()))
        self.assertTrue(isbday(datetime(2014, 1, 1, 16, 30)))
        self.assertTrue(isbday(datetime(2014, 1, 1, 17, 30)))
        self.assertFalse(isbday(datetime(2014, 1, 1, 16, 30),
                         holidays=holidays.US()))
        self.assertFalse(isbday(datetime(2014, 1, 1, 17, 30),
                         holidays=holidays.US()))


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

    def test_init_time(self):
        self.assertEqual(relativedelta(datetime(2015, 1, 5, 9, 15),
                                       datetime(2015, 1, 2, 16, 45)),
                         relativedelta(days=2, hours=16, minutes=30,
                                       bminutes=30))
        self.assertEqual(relativedelta(datetime(2015, 1, 20, 21, 22),
                                       datetime(2015, 1, 9, 3, 0)),
                         relativedelta(days=11, hours=18, minutes=22,
                                       bdays=7, bhours=8, bminutes=0))
        self.assertEqual(relativedelta(datetime(2015, 1, 20, 21, 22),
                                       datetime(2015, 1, 9, 3, 0),
                                       holidays=holidays.US()),
                         relativedelta(days=11, hours=18, minutes=22,
                                       bdays=6, bhours=8, bminutes=0))

    def test_add(self):
        rd1 = relativedelta(years=+1, months=+2, bdays=+3, days=+4,
                            bhours=+5, bminutes=+6, bseconds=+7,
                            hours=+8, minutes=+9, seconds=+10)
        rd2 = relativedelta(years=+10, months=-9, bdays=+8, days=-7,
                            bhours=+6, bminutes=-5, bseconds=+4,
                            hours=-3, minutes=+2, seconds=-1)
        rd3 = relativedelta(years=+11, months=-7, bdays=+11, days=-3,
                            bhours=+11, bminutes=+1, bseconds=+11,
                            hours=+5, minutes=+11, seconds=+9)
        self.assertEqual(rd1 + rd2, rd3)
        self.assertEqual(relativedelta(bdays=3) + date(2014, 1, 3),
                         date(2014, 1, 8))
        rd4 = relativedelta(years=+1, months=+2, days=+1)
        rd5 = relativedelta(years=+12, months=-5, bdays=+11, days=-2,
                            bhours=+11, bminutes=+1, bseconds=+11,
                            hours=+5, minutes=+11, seconds=+9)
        self.assertEqual(rd3 + rd4, rd5)
        self.assertEqual("2014-01-01" + relativedelta(weekday=FR),
                         datetime(2014, 1, 3))
        self.assertEqual("2014-11-15" + relativedelta(bdays=1),
                         datetime(2014, 11, 18))

    def test_add_time(self):
        self.assertEqual("2015-01-02 16:45" + relativedelta(bminutes=+30),
                         datetime(2015, 1, 5, 9, 15))
        self.assertEqual(date(2015, 1, 2) + relativedelta(bminutes=+30),
                         datetime(2015, 1, 2, 9, 30))

    def test_bdays_zero(self):
        self.assertEqual("2014-11-15" + relativedelta(bdays=0),
                         datetime(2014, 11, 17))
        self.assertEqual("2014-11-17" + relativedelta(bdays=0),
                         datetime(2014, 11, 17))
        self.assertEqual("2014-11-15" - relativedelta(bdays=0),
                         datetime(2014, 11, 14))
        self.assertEqual("2014-11-14" - relativedelta(bdays=0),
                         datetime(2014, 11, 14))

    def test_radd(self):
        self.assertEqual(date(2014, 1, 3) + relativedelta(bdays=2),
                         date(2014, 1, 7))
        self.assertEqual(date(2014, 1, 7) + relativedelta(bdays=-2),
                         date(2014, 1, 3))
        self.assertEqual(date(2014, 2, 3) + relativedelta(bdays=-19),
                         date(2014, 1, 7))

    def test_sub(self):
        rd1 = relativedelta(years=+1, months=+2, bdays=+3, days=+4,
                            bhours=+5, bminutes=+6, bseconds=+7,
                            hours=+8, minutes=+9, seconds=+10)
        rd2 = relativedelta(years=+10, months=-9, bdays=+8, days=-7,
                            bhours=+6, bminutes=-5, bseconds=+4,
                            hours=-3, minutes=+2, seconds=-1)
        rd3 = relativedelta(years=-9, months=+11, bdays=-5, days=+11,
                            bhours=-1, bminutes=+11, bseconds=+3,
                            hours=+11, minutes=+7, seconds=+11)
        self.assertEqual(rd1 - rd2, rd3)

    def test_rsub(self):
        self.assertEqual(date(2014, 1, 7) - relativedelta(bdays=2),
                         date(2014, 1, 3))
        self.assertEqual(date(2014, 1, 3) - relativedelta(bdays=-2),
                         date(2014, 1, 7))
        self.assertEqual(date(2014, 2, 3) - relativedelta(bdays=19),
                         date(2014, 1, 7))
        self.assertEqual("2014-11-15" - relativedelta(bdays=1),
                         datetime(2014, 11, 13))

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


class TestDateTime(unittest.TestCase):

    def test_date(self):
        self.assertEqual(date("2015-03-25"), dt.date(2015, 3, 25))
        self.assertEqual(date("1/2/2014"), dt.date(2014, 1, 2))
        self.assertEqual(date(1388577600), dt.date(2014, 1, 1))
        self.assertRaises(ValueError, lambda: date("abc"))
        self.assertRaises(TypeError, lambda: date(['a', 'b', 'c']))
        self.assertEqual(date(2015, 2, 99), date(2015, 2, 28))
        self.assertEqual(date.today(), dt.date.today())

    def test_datetime(self):
        self.assertEqual(datetime("2015-03-25 12:34"),
                         dt.datetime(2015, 3, 25, 12, 34))
        self.assertEqual(datetime(2015, 3, 99, 23, 45),
                         datetime(2015, 3, 31, 23, 45))
        self.assertEqual(datetime.now().date(), dt.datetime.now().date())

    def test_eomday(self):
        self.assertEqual(date("2015-02-15").eomday, dt.date(2015, 2, 28))
        self.assertEqual(datetime("2015-03-01 12:34").eomday,
                         dt.datetime(2015, 3, 31, 12, 34))


if __name__ == "__main__":
    unittest.main()
