from setuptools import find_packages
from setuptools import setup


VERSION = '2.0.0'


setup(
    author='Alex Clark',
    author_email='aclark@aclark.net',
    description='Project Management in Plone with Dexterity Content Types',
    entry_points={
        'z3c.autoinclude.plugin': 'target = plone',
    },
    extras_require={},
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    include_package_data=True,
    install_requires=[
        'setuptools',
        'plone.app.dexterity',
    ],
    keywords='dexterity plone project management',
    license='ZPL',
    long_description=(
        open("README.rst").read() + '\n' +
        open("CHANGES.rst").read()
    ),
    namespace_packages=[
        'collective'
    ],
    packages=find_packages(),
    url='https://github.com/collective/collective.project',
    name='collective.project',
    version=VERSION,
    zip_safe=False,
)
