from setuptools import setup, find_packages
import os

version = '0.8.2'

setup(name='izug.seantis.reservation',
      version=version,
      description="iZug theme adjustments for seantis.reservation",
      long_description='\n'.join((
          open("README.md").read(),
          open(os.path.join("docs", "HISTORY.txt")).read()
      )),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          'Programming Language :: Python',
      ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['izug', 'izug.seantis'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Plone>=4.1'
          'setuptools',
          'seantis.dir.base>=1.10',
          'seantis.dir.facility',
          'seantis.reservation',
          'izug.basetheme',
          'collective.geo.zugmap'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
