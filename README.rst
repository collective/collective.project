Introduction
============

This add-on demonstrates how to create a project management application in Plone with four Dexterity content types: Client, Project, Iteration, and Task. It also includes a tool to automate the creation of iterations, and a custom workflow for the Client, Project and Iteration types that contains active/inactive states.

.. image:: https://github.com/collective/collective.project/raw/master/screenshot.png

Installation
============

**Plone < 4.3**

For Plone versions earlier than 4.3, extend the Dexterity Known Good Set of packages e.g.::

    [buildout]
    extends = http://good-py.appspot.com/release/dexterity/1.2.1
    versions = versions

.. Note:: 
    You must extend the Dexterity Known Good Set provided by http://good-py.appspot.com/release/dexterity/1.2.1 to avoid Buildout conflict errors.

**Plone 4.x**

Add ``collective.project`` to ``plone.recipe.zope2instance`` section ``eggs`` parameter e.g.::

    [plone]
    recipe = plone.recipe.zope2instance
    eggs =
        …
        collective.project

For more information about Dexterity, please see:

- http://plone.org/products/dexterity/documentation
