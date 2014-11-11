=========
bdateutil
=========

Adds business day logic and improved data type flexibility to python-dateutil.
100% backwards compatible with python-dateutil, simply replace :code:`dateutil`
imports with :code:`bdateutil`.

.. image:: http://img.shields.io/travis/ryanss/bdateutil.svg
    :target: https://travis-ci.org/ryanss/bdateutil

.. image:: http://img.shields.io/coveralls/ryanss/bdateutil.svg
    :target: https://coveralls.io/r/ryanss/bdateutil


Example Usage
-------------

.. code-block:: python

    # Test if a date is a business day
    >>> from bdateutil import isbday
    >>> isbday(date(2014, 1, 1))
    True

    # Date parameters are no longer limited to datetime objects
    >>> isbday("2014-01-01")
    True
    >>> isbday("1/1/2014")
    True
    >>> isbday(1388577600)  # Unix timestamp = Jan 1, 2014
    True

    # Take into account U.S. statutory holidays
    >>> import holidays
    >>> isbday("2014-01-01", holidays=holidays.US())
    False

    # Increment date by two business days
    >>> from bdateutil import relativedelta
    >>> date(2014, 7, 3) + relativedelta(bdays=+2)
    datetime.date(2014, 7, 7)

    # Any arguments that take a date/datetime object now accept
    # strings/unicode/bytes in any encoding and integer/float timestamps.
    # All dateutil functions now also take an optional `holidays` argument
    # for helping to work with business days.
    >>> "2014-07-03" + relativedelta(bdays=+2, holidays=holidays.US())
    datetime.date(2014, 7, 8)

    # Determine how many business days between two dates
    >>> relativedelta("2014-07-07", date(2014, 7, 3))
    relativedelta(days=+4, bdays=+2)
    # Take into account Canadian statutory holidays
    >>> from holidays import Canada
    >>> relativedelta('2014-07-07', '07/03/2014', holidays=Canada())
    relativedelta(days=+4, bdays=+1)

    # Get a list of the next 10 business days starting 2014-01-01
    >>> from bdateutil import rrule, BDAILY
    >>> list(rrule(BDAILY, count=10, dtstart=date(2014, 1, 1)))
    # Take into account British Columbia, Canada statutory holidays
    >>> list(rrule(BDAILY, count=10, dtstart=date(2014, 1, 1),
                   holidays=Canada(prov='BC')))


Install
-------

The latest stable version can always be installed or updated via pip:

.. code-block:: bash

    $ pip install bdateutil

If the above fails, please use easy_install instead:

.. code-block:: bash

    $ easy_install bdateutil


Documentation
-------------

This section will outline the additional functionality of bdateutil only. For
full documentation on the features provided by python-dateutil please see its
documentation at https://labix.org/python-dateutil.

bdateutil is 100% backwards compatible with python-dateutil. You can replace
:code:`dateutil` with :code:`bdateutil` across your entire project and
everything will continue to work the same but you will have access to the
following additional features:


1. A new, optional, keyword argument :code:`bdays` is available when using
   relativedelta to add or remove time to a datetime object.

.. code-block:: python

    >>> date(2014, 1, 1) + relativedelta(bdays=+5)
    date(2014, 1, 8)

2. When passing two datetime arguments to relativedelta, the resulting
   relativedelta object will contain a :code:`bdays` attribute with the number
   of business days between the datetime arguments.

.. code-block:: python

    >>> relativedelta(date(2014, 7, 7), date(2014, 7, 3))
    relativedelta(days=+4, bdays=+2)

3. Another new, optional, keyword argument :code:`holidays` is available when
   using relativedelta to support the :code:`bdays` feature. Without holidays
   business days are only calculated using weekdays. By passing a list of
   holidays a more accurate and useful business day calculation can be
   performed. The Python package :code:`holidays.py` is installed as a
   requirement with bdateutil and that is the prefered way to generate
   holidays.

.. code-block:: python

    >>> from bdateutil import relativedelta
    >>> from holidays import UnitedStates
    >>> date(2014, 7, 3) + relativedelta(bdays=+2)
    datetime.date(2014, 7, 7)
    >>> date(2014, 7, 3) + relativedelta(bdays=+2, holidays=UnitedStates())
    datetime.date(2014, 7, 8)

4. A new function :code:`isbday` which returns :code:`True` if the argument
   passed to it falls on a business day and :code:`False` if it is a weekend or
   holiday. Option keyword argument :code:`holidays` adds the ability to take
   into account a specific set of holidays.

.. code-block:: python

    >>> from bdateutil import isbday
    >>> isbday(date(2014, 1, 1))
    True
    >>> isbday("2014-01-01")
    True
    >>> isbday("1/1/2014")
    True
    >>> isbday(1388577600)  # Unix timestamp = Jan 1, 2014
    True

    # Take into account U.S. statutory holidays
    >>> import holidays
    >>> isbday("2014-01-01", holidays=holidays.US())
    False

5. In addition to :code:`datetime` and :code:`date` types, relativedelta works
   with all strings/bytes regardless of encoding and integer/float timestamps.
   It does this by running all date/datetime parameters through the
   :code:`parse` function which has been modified to accept many different
   types than strings, including date/datetime which will return without
   modifications. This allows you to call :code:`parse(dt)` on an object
   regardless of type and ensure a datetime object is returned.

.. code-block:: python

    >>> parse(date(2014, 1, 1))
    datetime.date(2014, 1, 1)
    >>> parse(datetime(2014, 1, 1))
    datetime.datetime(2014, 1, 1, 0, 0)
    >>> parse("2014-01-01")
    datetime.datetime(2014, 1, 1, 0, 0)
    >>> parse("1/1/2014")
    datetime.datetime(2014, 1, 1, 0, 0)
    >>> parse(1388577600)
    datetime.datetime(2014, 1, 1, 0, 0)

    >>> relativedelta('2014-07-07', '2014-07-03')
    relativedelta(days=+4, bdays=+2)

    >>> 1388577600 + relativedelta(days=+2)
    date(2014, 1, 3)

6. The :code:`rrule` feature has a new :code:`BDAILY` option for use as the :code:`freq` argument.
   This will create a generator which yields business days. Rrule also will now
   accept an optional :code:`holidays` keyword argument which affects the
   :code:`BDAILY` freq only. The existing :code:`dtstart` and :code:`until`
   arugments can now be passed as any type resembling a date/datetime.

.. code-block:: python

    # Get a list of the next 10 business days starting 2014-01-01
    >>> from bdateutil import rrule, BDAILY
    >>> list(rrule(BDAILY, count=10, dtstart=date(2014, 1, 1)))

    # Get a list of all business days in January 2014, taking into account
    # Canadian statutory holidays
    >>> import holidays
    >>> list(rrule(BDAILY, dtstart="2014-01-01", until="2014-01-31",
                   holidays=holidays.Canada()))

7. Import shortcuts are available that make importing the bdateutil features a
   little easier than python-dateutil. However, importing from bdateutil using
   the longer method used by python-dateutil still works to remain 100%
   backwards compatibility.

.. code-block:: python

    >>> # Importing relativedelta from the original python-dateutil package
    >>> from dateutil.relativedelta import relativedelta

    >>> # This method works with bdateutil
    >>> from bdateutil.relativedelta import relativedelta

    >>> # bdateutil also provides an easier way
    >>> from bdateutil import relativedelta


Development Version
-------------------

The latest development version can be installed directly from GitHub:

.. code-block:: bash

    $ pip install --upgrade https://github.com/ryanss/bdateutil/tarball/master


Running Tests
-------------

.. code-block:: bash

    $ pip install flake8
    $ flake8 bdateutil/*.py tests.py --ignore=F401,F403
    $ python tests.py


Coverage
--------

.. code-block:: bash

    $ pip install coverage
    $ coverage run --omit=*site-packages* tests.py
    $ coverage report


Contributions
-------------

.. _issues: https://github.com/ryanss/bdateutil/issues
.. __: https://github.com/ryanss/bdateutil/pulls

Issues_ and `Pull Requests`__ are always welcome.


License
-------

.. __: https://github.com/ryanss/bdateutil/raw/master/LICENSE

Code and documentation are available according to the MIT License
(see LICENSE__).
