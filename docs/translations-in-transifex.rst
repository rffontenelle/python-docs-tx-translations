====================================
Translating Python Docs in Transifex
====================================

The target of this document is the language teams that use python-doc_ organization in Transifex_

.. _python-doc: https://www.transifex.com/python-doc
.. _Transifex: https://www.transifex.com/


Get to know Python Docs translation project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are new to Python documentation translation, please read Translating_ on `Python Developer's Guide`_ (a.k.a. devguide), join contact channels and take a time to read `PEP 545`_.

If exists a repository for your language team, then please join/introduce yourself to that team.

If there is no repository neither language team for your language, then first you have to create it. Translating in Transifex is not enough for having python docs published with your language. Please follow instructions in Translating_ on starting a new translating.  

.. _Translating: https://devguide.python.org/documentation/translating/
.. _Python Developer's Guide: https://devguide.python.org
.. _PEP 545: https://peps.python.org/pep-0545/

Get to know Transifex
~~~~~~~~~~~~~~~~~~~~~

If you are new to Transifex, I recommend some reading from Transifex docs:

- `Getting started as a translator <https://help.transifex.com/en/articles/6248698-getting-started-as-a-translator>`_: Signing up for an account, joining translation team
- `Translating with the Web Editor <https://help.transifex.com/en/articles/6318216-translating-with-the-web-editor>`_: Getting to the Editor, Searching and filtering for strings, Translating strings
- `Other Tools in the Editor <https://help.transifex.com/en/articles/6318944-other-tools-in-the-editor>`_: History, Glossary, Comments, Keyboard Shortcuts and more.
- `Starting with the basics <https://help.transifex.com/en/collections/3441044-starting-with-the-basics>`_: Group of documents with several basic information.

Projects in python-doc
~~~~~~~~~~~~~~~~~~~~~~

The python-doc organization contains several projects. Each project is the Python documentation for a specific Python version (3.10, etc.).

"Python" project (slug "python-newest") is the latest Python version available for translation (which might be the latest beta or stable release). All other projects are named "Python <version>".

Translate latest Python version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

Translations are propagated across projects for the same string. This means you translate once, and the docs for all Python versions receive the contribution if the string is the same. However, if the string has changed between versions, the contribution will not apply to those similar strings. 

Consider directing your translation efforts in the "Python" project (which is the newest version).

Take in consideration that Python Docs has an huge amount of strings and that contributed translations are propagated, so older versions will receive most of the contributions. At least, newer versions will receive more contributions due to less string differences, and newer are more important than older versions.

Placeholders
~~~~~~~~~~~~

You will notice that strings have Shinx roles (e.g. \:class:\`turtle`) set with custom placeholders (See `placeholders <placeholders.rst>`_).

This is useful for highlighting a role, which easies to properly translate it, and to have warning poping up in case that role has been incorrectly translated.

For instance, if there is a ``:class:`turtle``` in the source string, there should be one as well in the translation string. If it is missing, then Transifex will show a warning message.

Hopefully, there is no false-positives. Keep an eye on it, don't simply ignore these warnings.

Python docs is not updated by Transifex
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Transifex is only used as a web-based translation interface. Language teams have to download and store translation files in the language team's repository. This repository will be used by python-docs infrastructure to fetch translations, build the translated docs and publish in docs.python.org.
