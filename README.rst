=========
bdateutil
=========

Adds business day logic and improved data type flexibility to python-dateutil.
100% backwards compatible with python-dateutil, simply replace dateutil imports
with bdateutil.

.. image:: http://img.shields.io/travis/ryanss/bdateutil.svg
    :target: https://travis-ci.org/ryanss/bdateutil

.. image:: http://img.shields.io/coveralls/ryanss/bdateutil.svg
    :target: https://coveralls.io/r/ryanss/bdateutil


Example Usage
-------------------

.. code-block:: python

    >>> from bdateutil import relativedelta
    >>> from holidays import UnitedStates
    >>> relativedelta(date(2014, 7, 7), date(2014, 7, 3))
    relativedelta(days=+4, bdays=+2)
    >>> relativedelta('2014-07-07', '2014-07-03', holidays=UnitedStates())
    relativedelta(days=+4, bdays=+1)
    >>> date(2014, 7, 3) + relativedelta(bdays=+2)
    datetime.date(2014,7,7)
    >>> date(2014, 7, 3) + relativedelta(bdays=+2, holidays=UnitedStates())
    datetime.date(2014, 7, 8)
    >>> date(2014, 7, 3) + relativedelta(bdays=-4)
    datetime.date(2014, 6, 27)
    >>> date(2014, 7, 3) - relativedelta(bdays=+4)
    datetime.date(2014, 6, 27)


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
:code:`dateutil` with :code:`bdateutil` across your entire project and everything will
continue to work the same but you will have access to the following additional
features:

1. A new, optional, keyword argument :code:`bdays` is available when using
   relativedelta to add or remove time to a datetime object.

.. code-block:: python

    >>> date(2014, 1, 1) + relativedelta(bdays=+5)
    date(2014, 1, 8)

2. When passing two datetime arguments to relativedelta, the resulting
   relativedelta object will contain a :code:`bdays` attribute with the number of
   business days between the datetime arguments.

.. code-block:: python

    >>> relativedelta(date(2014, 7, 7), date(2014, 7, 3))
    relativedelta(days=+4, bdays=+2)

3. Another new, optional, keyword argument :code:`holidays` is available when using
   relativedelta to support the :code:`bdays` feature. Without holidays business days
   are only calculated using weekdays. By passing a list of holidays a more
   accurate and useful business day calculation can be performed. The Python
   package holidays.py is installed as a requirement with bdateutil and that is
   the prefered way to generate holidays.

.. code-block:: python

    >>> from bdateutil import relativedelta
    >>> from holidays import UnitedStates
    >>> date(2014, 7, 3) + relativedelta(bdays=+2)
    datetime.date(2014, 7, 7)
    >>> date(2014, 7, 3) + relativedelta(bdays=+2, holidays=UnitedStates())
    datetime.date(2014, 7, 8)

4. In addition to :code:`datetime` and :code:`date` types, relativedelta works with strings
   and integer/float timestamps.

.. code-block:: python

    >>> relativedelta('2014-07-07', '2014-07-03')
    relativedelta(days=+4, bdays=+2)

    >>> # This example does not work yet
    >>> "2014-01-01" + relativedelta(days=+2)
    date(2014, 1, 3)

5. Import shortcuts are available that make importing the bdateutil features a
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
