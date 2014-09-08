#  bdateutil
#  ---------
#  Adds business day logic and improved data type flexibility to
#  python-dateutil.
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/bdateutil
#  License: MIT (see LICENSE file)


import unittest
from datetime import date

from bdateutil import relativedelta
from testdateutil import *


class TestRelativeDelta(unittest.TestCase):

    def test_init(self):
        self.assertEquals(relativedelta(date(2014, 1, 7), date(2014, 1, 3)),
                          relativedelta(days=4, bdays=2))
        self.assertEquals(relativedelta(date(2014, 1, 31), date(2014, 1, 1)),
                          relativedelta(days=30, bdays=22))
        self.assertEquals(relativedelta(date(2014, 2, 1), date(2014, 1, 1)),
                          relativedelta(months=1, bdays=23))
        self.assertEquals(relativedelta(date(2014, 2, 2), date(2014, 1, 1)),
                          relativedelta(months=1, days=1, bdays=23))

    def test_add(self):
        rd1 = relativedelta(years=+1, months=+2, bdays=+3, days=+4)
        rd2 = relativedelta(years=+2, months=-3, bdays=+4, days=+5)
        rd3 = relativedelta(years=+3, months=-1, bdays=+7, days=+9)
        self.assertEquals(rd1 + rd2, rd3)
        self.assertEquals(relativedelta(bdays=3) + date(2014, 1, 3),
                          date(2014, 1, 8))

    def test_radd(self):
        self.assertEquals(date(2014, 1, 3) + relativedelta(bdays=2),
                          date(2014, 1, 7))
        self.assertEquals(date(2014, 1, 7) + relativedelta(bdays=-2),
                          date(2014, 1, 3))
        self.assertEquals(date(2014, 2, 3) + relativedelta(bdays=-19),
                          date(2014, 1, 7))

    def test_sub(self):
        rd1 = relativedelta(years=+1, months=+2, bdays=+3, days=+4)
        rd2 = relativedelta(years=+2, months=-3, bdays=+4, days=+5)
        rd3 = relativedelta(years=-1, months=+5, bdays=-1, days=-1)
        self.assertEquals(rd1 - rd2, rd3)

    def test_rsub(self):
        self.assertEquals(date(2014, 1, 7) - relativedelta(bdays=2),
                          date(2014, 1, 3))
        self.assertEquals(date(2014, 1, 3) - relativedelta(bdays=-2),
                          date(2014, 1, 7))
        self.assertEquals(date(2014, 2, 3) - relativedelta(bdays=19),
                          date(2014, 1, 7))

    def test_neg(self):
        self.assertEquals(-relativedelta(years=+1, bdays=-3),
                          relativedelta(years=-1, bdays=+3))

    def test_bool(self):
        self.assertTrue(relativedelta(bdays=1))
        self.assertTrue(relativedelta(days=1))
        self.assertFalse(relativedelta())

    def test_mul(self):
        self.assertEquals(relativedelta(years=+1, bdays=-3) * 3,
                          relativedelta(years=+3, bdays=-9))
        self.assertEquals(relativedelta(years=+1, bdays=-3) * -3,
                          relativedelta(years=-3, bdays=+9))
        self.assertEquals(relativedelta(years=+1, bdays=-3) * 0,
                          relativedelta(years=0, bdays=0))

    def test_rmul(self):
        self.assertEquals(3 * relativedelta(years=+1, bdays=-3),
                          relativedelta(years=+3, bdays=-9))
        self.assertEquals(-3 * relativedelta(years=+1, bdays=-3),
                          relativedelta(years=-3, bdays=+9))
        self.assertEquals(0 * relativedelta(years=+1, bdays=-3),
                          relativedelta(years=0, bdays=0))

    def test_eq(self):
        r1 = relativedelta(years=1, months=2, days=3, bdays=1,
                           hours=4, minutes=5, seconds=6, microseconds=7)
        r2 = relativedelta(years=1, months=2, days=3, bdays=1,
                           hours=4, minutes=5, seconds=6, microseconds=7)
        self.assertEquals(r1, r2)
        self.assertTrue(r1 == r2)
        r2.days = 4
        self.assertNotEquals(r1, r2)
        self.assertFalse(r1 == r2)
        r2.days = 3
        r2.bdays = 0
        self.assertNotEquals(r1, r2)
        self.assertFalse(r1 == r2)
        self.assertEquals(relativedelta(), relativedelta())
        self.assertTrue(relativedelta() == relativedelta())
        self.assertNotEquals(relativedelta(days=1), relativedelta(bdays=1))
        self.assertFalse(relativedelta() == relativedelta(months=1))
        self.assertNotEquals(relativedelta(days=1), relativedelta(bdays=1))
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
        self.assertEquals(relativedelta(years=+3, bdays=-9) / 3,
                          relativedelta(years=+1, bdays=-3))
        self.assertEquals(relativedelta(years=+3, bdays=-9) / -3,
                          relativedelta(years=-1, bdays=+3))
        self.assertRaises(ZeroDivisionError,
                          lambda: relativedelta(bdays=-3) / 0)

    def test_truediv(self):
        self.assertEquals(relativedelta(years=+4, bdays=-10) / 3.0,
                          relativedelta(years=+1, bdays=-3))


if __name__ == "__main__":
    unittest.main()
