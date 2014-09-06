=========
bdateutil
=========

Adds business day logic and improved data type flexibility to python-dateutil.


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


Development Version
-------------------

The latest development version can be installed directly from GitHub:

.. code-block:: bash

    $ pip install --upgrade https://github.com/ryanss/bdateutil/tarball/master


Running Tests
-------------

.. code-block:: bash

    $ python tests.py


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
