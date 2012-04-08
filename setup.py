from setuptools import find_packages
from setuptools import setup
import os

VERSION = '1.0.0'


setup(
    author='Alex Clark',
    author_email='aclark@aclark.net',
    description='Demo app: project management with dexterity content types.',
    entry_points={
        'z3c.autoinclude.plugin': 'target = plone',
    },
    classifiers=[
      "Framework :: Plone",
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
