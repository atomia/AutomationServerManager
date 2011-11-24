'''
Created on Nov 10, 2011

@author: Dusan
'''
import os
from setuptools import setup, find_packages

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Atomia Automation Server Manager",
    version = "0.0.1",
    author = "Atomia",
    author_email = "dusan@atomia.com",
    description = ("Command-line app for Atomia Automation Server management."),
    license = "GPL",
    keywords = "atomia automation command-line",
    url = "http://packages.python.org/Atomia Automation Server Manager",
    packages=find_packages(),
    long_description=read('README.md'),
	install_requires=['argparse'],
	setup_requires=['setuptools'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
		"Topic :: Utilities",
		"Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
	entry_points={
        'console_scripts': [
            'atomia = atomia_automation_server_manager.atomia:entry',
		],
	},
	package_data = {
        # If any package contains *.conf.dist files, include them:
        '': ['*.conf.dist']
    }
)