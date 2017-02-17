#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import decisionTable

with open('README.md') as readme_file:
	readme = readme_file.read()

requirements = [
]

test_requirements = [
]

setup(
	name='decisionTable',
	version=decisionTable.__version__,
	description=decisionTable.__description__,
	long_description=readme,
	author=decisionTable.__author__,
	author_email=decisionTable.__email__,
	url='https://github.com/urosjarc/decisionTable.py',
	packages=[
		'decisionTable',
	],
	package_dir={
		'decisionTable': 'decisionTable'
	},
	include_package_data=False,
	install_requires=requirements,
	license="MIT license",
	zip_safe=True,
	keywords='decision table if else elif',
	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		"Programming Language :: Python :: 2",
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
	],
	test_suite='test',
	tests_require=test_requirements
)
