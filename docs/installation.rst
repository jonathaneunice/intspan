Installation
============

To install or upgrade to the latest version::

    pip install -U intspan

To ``easy_install`` under a specific Python version (3.3 in this example)::

    python3.3 -m easy_install --upgrade intspan

(You may need to prefix these with ``sudo`` to authorize
installation. In environments without super-user privileges, you may want to
use ``pip``'s ``--user`` option, to install only for a single user, rather
than system-wide.)


Testing
-------

If you wish to run the module tests locally, you'll need to install
``pytest`` and ``tox``.  For full testing, you will also need ``pytest-cov``
and ``coverage``. Then run one of these commands::

    tox                # normal run - speed optimized
    tox -e py27        # run for a specific version only (e.g. py27, py34)
    tox -c toxcov.ini  # run full coverage tests
