#  bdateutil
#  -----------
#  Adds business day logic and improved data type flexibility to
#  python-dateutil. 100% backwards compatible with python-dateutil,
#  simply replace dateutil imports with bdateutil.
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/bdateutil
#  License: MIT (see LICENSE file)


from dateutil.rrule import *
from dateutil.rrule import rrule as rrulebase
from dateutil.rrule import _rrulestr as rrulestrbase

from bdateutil import parse


BDAILY = 8


class rrule(rrulebase):

    def __init__(self, freq, holidays=None, **kwargs):
        self.holidays = holidays
        if self.holidays is None:
            self.holidays = getattr(rrule, 'holidays', ())
        if 'dtstart' in kwargs:
            kwargs['dtstart'] = parse(kwargs['dtstart'])
        if 'until' in kwargs:
            kwargs['until'] = parse(kwargs['until'])
        if freq == BDAILY:
            rrulebase.__init__(self, DAILY, **kwargs)
            self._bdaily = True
            if self._count:
                self._count *= 2
        else:
            rrulebase.__init__(self, freq, **kwargs)
            self._bdaily = False

    def _iter(self):
        total = 0
        for i in rrulebase._iter(self):
            if self._bdaily:
                if i.weekday() < 5 and i not in self.holidays:
                    total += 1
                    if self._count and total > self._count / 2:
                        self._len = total
                        return
                    elif self._until and i > self._until:
                        self._len = total
                        return
                    yield i
            else:
                yield i
        return


# dateutil.rrule.rrulestr returns a dateutil.rrule.rrule object
# RRuleTest.testStrType() from the original dateutil tests fails
# because dateutil.rrule.rrule is not an instance of bdateutil.rrule.rrule
# so we need to redefine rrulestr to return a bdateutil rrule object
class _rrulestr(rrulestrbase):

    def _parse_rfc_rrule(self, line, **kwargs):
        ret = rrulestrbase._parse_rfc_rrule(self, line, **kwargs)
        ret.__class__ = rrule
        ret._bdaily = False
        return ret


rrulestr = _rrulestr()
