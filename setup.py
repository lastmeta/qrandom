# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

setup(
    name='qrandom',
    version='0.0.1',
    packages=find_packages(),
    url='',
    author='Jordan Miller',
    author_email='jordan.kay@gmail.com',
    install_requires=['pyserial', 'bitstring'],
    description='wrapper for any quantum random number generator',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='Do whatsoever thou wilt.',
    classifiers=[],
    entry_points={},
)
