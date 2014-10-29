#  bdateutil
#  -----------
#  Adds business day logic and improved data type flexibility to
#  python-dateutil. 100% backwards compatible with python-dateutil,
#  simply replace dateutil imports with bdateutil.
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/bdateutil
#  License: MIT (see LICENSE file)

__version__ = '0.1-dev'


from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU

from bdateutil.relativedelta import relativedelta


__all__ = ['relativedelta', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
