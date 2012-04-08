Introduction
============

This add-on demonstrates how to create a project management application in Plone with four Dexterity content types: Client, Project, Iteration, and Task. It also includes a tool to automate the creation of iterations, and a custom workflow for the Client, Project and Iteration types that contains active/inactive states.

.. image:: https://github.com/collective/collective.project/raw/master/screenshot.png

Installation
============

Extend the Dexterity KGS::

    [buildout]
    extends = http://good-py.appspot.com/release/dexterity/1.2
    versions = versions

.. Note:: 
    You must extend the Dexterity KGS (known good set) provided by
    http://good-py.appspot.com/release/dexterity/1.2 otherwise you will get
    conflict errors in Buildout.

Add ``collective.project`` to instance eggs::

    [plone]
    recipe = plone.recipe.zope2instance
    eggs =
        …
        collective.project

For more information about installing Dexterity, please see:

- http://plone.org/products/dexterity/documentation/how-to/install

