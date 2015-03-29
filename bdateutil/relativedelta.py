#  bdateutil
#  -----------
#  Adds business day logic and improved data type flexibility to
#  python-dateutil. 100% backwards compatible with python-dateutil,
#  simply replace dateutil imports with bdateutil.
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/bdateutil
#  License: MIT (see LICENSE file)


from collections import defaultdict
from datetime import date, datetime

from dateutil.relativedelta import relativedelta as rd
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
import six

from bdateutil.parser import parse


class relativedelta(rd):

    def __init__(self, dt1=None, dt2=None, bdays=None, holidays=None,
                 bhours=None, bminutes=None, bseconds=None,
                 *args, **kwargs):
        self.holidays = holidays
        if self.holidays is None:
            self.holidays = getattr(relativedelta, 'holidays', ())
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
            c = defaultdict(int)
            d1 = max(dt1, dt2)
            d2 = min(dt1, dt2)
            if d1.weekday() in (5, 6) or d1 in self.holidays:
                c['bdays'] += 1
            for attr in ('bhours', 'bminutes', 'bseconds'):
                while getattr(d1, attr[1:-1]) != getattr(d2, attr[1:-1]):
                    d2 += rd(**{attr[1:]: +1})
                    if d2.hour >= 9 and d2.hour < 17:
                        c[attr] += 1
            while d1 > d2:
                d2 += rd(days=+1)
                if d2.weekday() not in (5, 6) and d2 not in self.holidays:
                    c['bdays'] += 1
            self.bdays = c['bdays']
            self.bhours = c['bhours']
            self.bminutes = c['bminutes']
            self.bseconds = c['bseconds']
            if dt2 > dt1:
                self.bdays *= -1
                self.bhours *= -1
                self.bminutes *= -1
                self.bseconds *= -1
        else:
            self.bdays = bdays
            self.bhours = bhours
            self.bminutes = bminutes
            self.bseconds = bseconds
            rd.__init__(self, dt1, dt2, *args, **kwargs)

    def __add__(self, other):
        if isinstance(other, relativedelta):
            ret = rd.__add__(self, other)
            ret.__class__ = relativedelta
            for attr in ('bdays', 'bhours', 'bminutes', 'bseconds'):
                if getattr(self, attr, None) is not None:
                    if getattr(other, attr, None) is not None:
                        setattr(ret, attr,
                                getattr(self, attr) + getattr(other, attr))
                    else:
                        setattr(ret, attr, getattr(self, attr))
                elif getattr(other, attr, None) is not None:
                    setattr(ret, attr, getattr(other, attr))
            return ret
        ret = parse(other)
        # If we are adding any time (not just dates) the ret object to return
        # must be a datetime object; a date object will not work
        if not isinstance(ret, datetime) \
                and (self.bhours or self.bminutes or self.bseconds):
            ret = datetime.combine(ret, datetime.min.time())
        for attr in ('bseconds', 'bminutes', 'bhours', 'bdays'):
            if getattr(self, attr, None) is not None:
                while ret.weekday() in (5, 6) or ret in self.holidays:
                    ret += rd(days=+1)
                while attr != "bdays" and (ret.hour < 9 or ret.hour >= 17):
                    ret += rd(**{attr[1:]: +1})
                i = getattr(self, attr)
                a = +1 if i > 0 else -1
                while i != 0:
                    ret += rd(**{attr[1:]: a})
                    while ret.weekday() in (5, 6) or ret in self.holidays:
                        ret += rd(days=a)
                    while attr != "bdays" and (ret.hour < 9 or ret.hour >= 17):
                        ret += rd(**{attr[1:]: a})
                    i -= a
        return rd.__add__(self, ret)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        ret = rd.__sub__(self, other)
        ret.__class__ = relativedelta
        for attr in ('bdays', 'bhours', 'bminutes', 'bseconds'):
            if getattr(self, attr, None) is not None:
                setattr(ret, attr, getattr(self, attr))
                if getattr(other, attr, None) is not None:
                    setattr(ret, attr,
                            getattr(ret, attr) - getattr(other, attr))
        return ret

    def __rsub__(self, other):
        if getattr(self, 'bdays', None) is not None:
            other = parse(other)
            if self.bdays == 0:
                while other.weekday() in (5, 6) or other in self.holidays:
                    other += rd(days=-1)
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
        for attr in ('bdays', 'bhours', 'bminutes', 'bseconds'):
            if getattr(self, attr, None) is not None and \
                    getattr(other, attr, None) is not None and \
                    getattr(self, attr, None) != getattr(other, attr, None):
                return False
        return rd.__eq__(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        l = []
        for attr in ["years", "months", "days", "leapdays", "bdays",
                     "hours", "minutes", "seconds", "microseconds",
                     "bhours", "bminutes", "bseconds"]:
            value = getattr(self, attr, None)
            if value:
                l.append("%s=%+d" % (attr, value))
        for attr in ["year", "month", "day", "weekday",
                     "hour", "minute", "second", "microsecond"]:
            value = getattr(self, attr)
            if value is not None:
                l.append("%s=%s" % (attr, repr(value)))
        return "%s(%s)" % (self.__class__.__name__, ", ".join(l))
