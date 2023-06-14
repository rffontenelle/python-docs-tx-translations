===========================
python-docs-tx-translations
===========================

.. image:: https://github.com/rffontenelle/python-docs-tx-translations/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/rffontenelle/python-docs-tx-translations/actions/workflows/ci.yml

Scripts and procedures for maintaining Python_ documentation translation infrastructure under python-doc_ organization in Transifex_.

Source strings are updated using continuous integration workflow under *.github/workflows*. Details:

- Run weekly
- Run for releases in beta, release candidate, stable, bugfixes and security-fixes status; alpha or EOL are excluded;
- It DOES NOT store translations to be used by the published documentation;

See docs_ directory for more information on this project maintenance.

See Translating_ in Python Developer's Guide for more information.

.. _Python: https://www.python.org
.. _python-doc: https://app.transifex.com/python-doc/
.. _Transifex: https://www.transifex.com
.. _docs: https://github.com/rffontenelle/docspush-transifex/blob/main/docs/
.. _Translating: https://devguide.python.org/documentation/translating/
