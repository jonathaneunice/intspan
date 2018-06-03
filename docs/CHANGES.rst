Change Log
==========

**1.5.13**  (June 3, 2018)

    Documentation tweaks.


**1.5.12**  (June 2, 2018)

    Updated testing matrix. Now includes Python 3.7 pre-release.

    Tox tests trimmed in favor of Travis CI.


**1.5.11**  (October 13, 2017)

    Add pyproject.toml for PEP 508 conformance


**1.5.10**  (May 30, 2017)

    Update Python version compatibility strategy. Now Python 3
    centric. More future-proofed.

    Updated testing matrix. Tweaked docs.


**1.5.8**  (February 9, 2017)

    Changed from module to package builds.


**1.5.5**  (February 1, 2017)

    Documentation upgrades.


**1.5.4**  (January 31, 2017)

    Tested and certified for all early 2017 versions of Python
    including latest builds of 2.6, 2.7, 3.3, 3.4, 3.5, and 3.6, as
    well as latest PyPy and PyPy3.


**1.5.3**  (June 21, 2016)

    Tested and certified for Python 2.7.11, 3.4.4, 3.5.1, 3.6.0a2,
    PyPy 3.5.1 (based on Python 2.7.10), and PyPy3 5.2.0-alpha0 (based
    on Python 3.3.5). Python 3.2 is deprecated due to its advancing
    age and now-limited compatibility with my test rig. It still
    passes Travis CI tests--but as soon as it does not, it will be
    withdrawn from support.


**1.5.2**  (September 23, 2015)

    Tested and certified for PyPy 2.6.1 (based on Python 2.7.10)


**1.5.1**  (September 14, 2015)

    Updated testing for Python 3.5.0 final.


**1.5.0**  (August 27, 2015)

    Added ``universe`` method. Extended tests. Continuing to extend
    docs.


**1.4.4**  (August 27, 2015)

    Improving documentation, especially around API details. Will
    probably require a handful of incremental passes to get the API
    reference ship-shape.


**1.4.2**  (August 26, 2015)

    Reorganied documentation. Added API details and moved full docs to
    Read The Docs.


**1.4.1** 

    Achieves 100% *branch* coverage. *Hooah!*


**1.4.0** 

    Achieves 100% test coverage and integrated coverage testing across
    multiple versions with ``tox``.


**1.3.10** 

    Improved test coverage and explicit coverage testing. Also tweaked
    docs.


**1.3.9** 

    Simplified ``setup.py`` and packaging.


**1.3.7** 

    Adds ``bdist_wheel`` packaging support.


**1.3.6** 

    Switches from BSD to Apache License 2.0 and integrates ``tox``
    testing with ``setup.py``


**1.3.0** 

    Adds ``*`` notation for abstract "the rest of the items" in an
    ``intspanlist``.


**1.2.6** 

    Inaugurates continuous integration with Travis CI.


**1.2.0** 

    Adds an experimental ``spanlist`` constructor and ``intspanlist``
    type.


**1.1.0** 

    Adds ``from_range`` and ``complement`` methods; improves error
    handling of ``pop`` on an empty set), and tweaks testing.


**1.0.0** 

    Immediately follows 0.73. Bumped to institute a cleaner "semantic
    versioning" scheme. Upgraded from "beta" to "production" status.


**0.73.0** 

    Updates testing to include the latest Python 3.4


**0.7.0** 

    Fixed parsing of spans including negative numbers, and added the
    ``ranges()`` method. As of 0.71, the ``from_ranges()`` constructor
    appeared.



