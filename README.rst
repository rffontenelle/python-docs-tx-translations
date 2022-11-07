==================
docspush-transifex
==================

Scripts and procedures for maintaining Python_ documentation translation infrastructure under python-doc_ organization in Transifex_.

Source strings are updated using continuous integration workflow under *.github/workflows*. Details:

- Run every 12h
- Run for releases in beta, stable and security-fixes (not EOL) status
- It DOES NOT download translations nor update the published translated documentation

See MAINTENANCE_ for documented procedures.

See Translating_ in Python Developer's Guide for more information.

.. _Python: https://www.python.org
.. _python-doc: https://www.transifex.com/python-doc
.. _Transifex: https://www.transifex.com
.. _MAINTENANCE: https://github.com/rffontenelle/docspush-transifex/blob/main/MAINTENANCE.rst
.. _Translating: https://devguide.python.org/documentation/translating/
