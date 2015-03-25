#  bdateutil
#  -----------
#  Adds business day logic and improved data type flexibility to
#  python-dateutil. 100% backwards compatible with python-dateutil,
#  simply replace dateutil imports with bdateutil.
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/bdateutil
#  License: MIT (see LICENSE file)

__version__ = '0.2-dev'


from bdateutil.parser import parse
from bdateutil.relativedelta import relativedelta
from bdateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from bdateutil.rrule import *
from bdateutil.dt import date, datetime


def isbday(dt, holidays=()):
    dt = parse(dt)
    return not (dt.weekday() in (5, 6) or dt in holidays)
