#  bdateutil
#  -----------
#  Adds business day logic and improved data type flexibility to
#  python-dateutil. 100% backwards compatible with python-dateutil,
#  simply replace dateutil imports with bdateutil.
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/bdateutil
#  License: MIT (see LICENSE file)


from datetime import date, datetime

from dateutil.relativedelta import relativedelta as rd
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
import six

from bdateutil.parser import parse


class relativedelta(rd):

    def __init__(self, dt1=None, dt2=None, bdays=None,
                 holidays=(), *args, **kwargs):
        self.holidays = holidays
        if dt1 and dt2:
            # Convert to datetime objects
            dt1 = parse(dt1)
            dt2 = parse(dt2)
            if isinstance(dt1, date) and not isinstance(dt1, datetime):
                dt1 = datetime.combine(dt1, datetime.min.time())
            if isinstance(dt2, date) and not isinstance(dt2, datetime):
                dt2 = datetime.combine(dt2, datetime.min.time())
            # Call super init before setting self.bdays to avoid base __radd__
            # from calling child __add__ and creating infinite loop
            rd.__init__(self, dt1, dt2, *args, **kwargs)
            bdays = 0
            d1 = max(dt1, dt2)
            d2 = min(dt1, dt2)
            if d1.weekday() in (5, 6) or d1 in self.holidays:
                bdays += 1
            while d1 > d2:
                d2 = rd(days=+1) + d2
                if d2.weekday() not in (5, 6) and d2 not in self.holidays:
                    bdays += 1
            self.bdays = bdays
            if dt2 > dt1:
                self.bdays *= -1
        else:
            self.bdays = bdays
            rd.__init__(self, dt1, dt2, *args, **kwargs)

    def __add__(self, other):
        if isinstance(other, relativedelta):
            ret = rd.__add__(self, other)
            if self.bdays is None:
                ret.bdays = None
            elif getattr(other, 'bdays', None) is None:
                ret.bdays = self.bdays
            else:
                ret.bdays = self.bdays + other.bdays
            return ret
        ret = parse(other)
        if getattr(self, 'bdays', None) is not None:
            bdays = self.bdays
            a = +1 if bdays > 0 else -1
            while bdays != 0:
                ret += rd(days=a)
                while ret.weekday() in (5, 6) or ret in self.holidays:
                    ret += rd(days=a)
                bdays -= a
        return rd.__add__(self, ret)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        ret = rd.__sub__(self, other)
        if getattr(self, 'bdays', None) is not None:
            ret.bdays = self.bdays
            if getattr(other, 'bdays', None) is not None:
                ret.bdays -= other.bdays
        return ret

    def __rsub__(self, other):
        return self.__neg__().__radd__(other)

    def __neg__(self):
        bdays = -self.bdays if self.bdays is not None else None
        return relativedelta(years=-self.years,
                             months=-self.months,
                             days=-self.days,
                             bdays=bdays,
                             hours=-self.hours,
                             minutes=-self.minutes,
                             seconds=-self.seconds,
                             microseconds=-self.microseconds,
                             leapdays=self.leapdays,
                             year=self.year,
                             month=self.month,
                             day=self.day,
                             weekday=self.weekday,
                             hour=self.hour,
                             minute=self.minute,
                             second=self.second,
                             microsecond=self.microsecond)

    def __bool__(self):
        if self.bdays is None:
            return rd.__bool__(self)
        return rd.__bool__(self) or bool(self.bdays)

    __nonzero__ = __bool__

    def __mul__(self, other):
        f = float(other)
        bdays = int(self.bdays * f) if self.bdays is not None else None
        return relativedelta(years=int(self.years * f),
                             months=int(self.months * f),
                             days=int(self.days * f),
                             bdays=bdays,
                             hours=int(self.hours * f),
                             minutes=int(self.minutes * f),
                             seconds=int(self.seconds * f),
                             microseconds=int(self.microseconds * f),
                             leapdays=self.leapdays,
                             year=self.year,
                             month=self.month,
                             day=self.day,
                             weekday=self.weekday,
                             hour=self.hour,
                             minute=self.minute,
                             second=self.second,
                             microsecond=self.microsecond)

    def __eq__(self, other):
        if self.bdays is not None:
            if getattr(other, 'bdays', None) is not None:
                return rd.__eq__(self, other) and self.bdays == other.bdays
        return rd.__eq__(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        l = []
        for attr in ["years", "months", "days", "leapdays", "bdays",
                     "hours", "minutes", "seconds", "microseconds"]:
            value = getattr(self, attr)
            if value:
                l.append("%s=%+d" % (attr, value))
        for attr in ["year", "month", "day", "weekday",
                     "hour", "minute", "second", "microsecond"]:
            value = getattr(self, attr)
            if value is not None:
                l.append("%s=%s" % (attr, repr(value)))
        return "%s(%s)" % (self.__class__.__name__, ", ".join(l))
