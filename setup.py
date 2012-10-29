from setuptools import find_packages
from setuptools import setup
import os

VERSION = '1.0.1'


setup(
    author='Alex Clark',
    author_email='aclark@aclark.net',
    description='Demo app: project management with dexterity content types.',
    entry_points={
        'z3c.autoinclude.plugin': 'target = plone',
    },
    extras_require = {
        'test': [
            'plone.app.testing',
            'unittest2'
            ],
        'grok': [
            'five.grok',
            'plone.directives.dexterity',
            'plone.directives.form >=1.1dev',
            ],
        'relations': [
            'plone.app.relationfield',
            'plone.app.intid',
            'z3c.relationfield',
            ]
    },
    classifiers=[
      "Framework :: Plone",
      "Framework :: Plone :: 4.0",
      "Framework :: Plone :: 4.1",
      "Framework :: Plone :: 4.2",
      "Framework :: Plone :: 4.3",
      "Programming Language :: Python",
      "Topic :: Software Development :: Libraries :: Python Modules",
      ],
    include_package_data=True,
    install_requires=[
        'setuptools',
        'plone.app.dexterity',
    ],
    keywords='add-on plone dexterity example package',
    license='ZPL',
    long_description=(
        open("README.rst").read() +
        open(os.path.join("docs", "HISTORY.txt")).read()
    ),
    namespace_packages=[
        'collective'
    ],
    packages=find_packages(),
    url='http://collective.github.com/collective.project/',
    name='collective.project',
    version=VERSION,
    zip_safe=False,
)
