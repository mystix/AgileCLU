#!/usr/bin/env python
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here,"README")).read()

setup(  
	name="AgileCLU",
	version="0.3.2",
   install_requires=['poster','progressbar','pydes','jsonrpclib'],
	packages=['AgileCLU'],
	package_data={'': ['LICENSE','README.md']},
	include_package_data=True,
	scripts=['bin/agilels', 'bin/agilefetch', 'bin/agilemkdir', 'bin/agilepost', 'bin/agileprofile', 'bin/agilerm'],

	description="Agile Command Line Utilities",
	long_description=readme,
	author="Wylie Swanson",
	author_email="wylie@pingzero.net",
	url="http://www.pingzero.net",
	download_url = "https://github.com/wylieswanson/AgileCLU/raw/master/dist/AgileCLU-0.3.2.tar.gz",

	platforms = ("Any",),
	keywords = ("agile", "storage", "limelight", "cloud", "object" ),

	classifiers = [	'Development Status :: 4 - Beta',
							'License :: OSI Approved :: BSD License',
							'Programming Language :: Python',
							'Intended Audience :: End Users/Desktop',
							'Environment :: Console',
							'Topic :: Utilities',
							]
	)
