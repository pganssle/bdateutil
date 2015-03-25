#  bdateutil
#  -----------
#  Adds business day logic and improved data type flexibility to
#  python-dateutil. 100% backwards compatible with python-dateutil,
#  simply replace dateutil imports with bdateutil.
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/bdateutil
#  License: MIT (see LICENSE file)


import calendar
from datetime import date as basedate
from datetime import datetime as basedatetime

from bdateutil.parser import parse


class date(basedate):

    def __new__(self, *args, **kwargs):
        if len(args) == 1:
            return parse(args[0]).date()
        if len(args) > 2:
            if args[2] == 99:
                args = list(args)
                args[2] = calendar.monthrange(args[0], args[1])[1]
        return basedate.__new__(self, *args, **kwargs)


class datetime(basedatetime):

    def __new__(self, *args, **kwargs):
        if len(args) == 1:
            return parse(args[0])
        if len(args) > 2:
            if args[2] == 99:
                args = list(args)
                args[2] = calendar.monthrange(args[0], args[1])[1]
        return basedatetime.__new__(self, *args, **kwargs)
