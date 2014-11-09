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

from dateutil.parser import *
from dateutil.parser import parser
import six


def parse(timestr, parserinfo=None, **kwargs):
    if isinstance(timestr, six.binary_type):
        timestr = timestr.decode()
    if isinstance(timestr, six.string_types):
        try:
            if parserinfo:
                ret = parser(parserinfo).parse(timestr, **kwargs)
            else:
                ret = parser().parse(timestr, **kwargs)
        except TypeError:
            raise ValueError("Can't parse date from string '%s'" % timestr)
    elif isinstance(timestr, int) or isinstance(timestr, float):
        ret = datetime.fromtimestamp(timestr)
    elif isinstance(timestr, datetime) or isinstance(timestr, date):
        ret = timestr
    else:
        raise TypeError("Can't convert %s to date." % type(timestr))
    return ret
