# Min python version (3.6)
import os
import sys

from setuptools import setup, find_packages

CURRENT_PYTHON_VERSION = sys.version_info[:2]
REQUIRED_PYTHON_VERSION = (3,6)

# Validating python version before the setup run
if REQUIRED_PYTHON_VERSION > CURRENT_PYTHON_VERSION:
    sys.stderr.write("""
    Unsupported python version found.

    Current Python: {}.
    Required Python: {}.
    
    """.format(CURRENT_PYTHON_VERSION, REQUIRED_PYTHON_VERSION))
    sys.exit(64)


setup(
    name='pypaypal',
    version='0.8.15',
    python_requires='>=3.6',
    author='ivcuello',
    author_email='ivcuello@gmail.com',
    description='Paypal API integration supporting some v1 & most of the current v2 rest APIs calls',
    packages = find_packages(exclude=['docs', 'tests']),
    install_requires = [ 
        'python-dateutil',
        'requests'
    ]
)