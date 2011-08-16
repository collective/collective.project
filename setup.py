from setuptools import setup, find_packages
import os

setup(
    name='collective.project',
    version='0.9.5',
    description="""Dexterity demo: "simple" project management via four Dexterity content types: Client, Project, Iteration, and Task.""",
    long_description=open("README.txt").read() + "\n" +
                     open(os.path.join("docs", "HISTORY.txt")).read(),
    classifiers=[
      "Framework :: Plone",
      "Programming Language :: Python",
      "Topic :: Software Development :: Libraries :: Python Modules",
      ],
    keywords='"project management"',
    author='Alex Clark',
    author_email='aclark@aclark.net',
    url='https://github.com/collective/collective.project',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.app.dexterity',
    ],
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
