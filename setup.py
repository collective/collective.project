from setuptools import setup, find_packages
import os

version = '0.9.4'

setup(name='collective.project',
      version=version,
      description="""Dexterity demo: this package aims for "simple" project management by adding four new Dexterity content types: Client, Project, Iteration, and Task.""",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "INSTALL.txt")).read() +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='"project management"',
      author='Alex Clark',
      author_email='aclark@aclark.net',
      url='https://svn.plone.org/svn/collective/collective.project/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.dexterity',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
