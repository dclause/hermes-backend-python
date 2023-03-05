""" setup.py script """

from setuptools import setup

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()

with open('dev_requirements.txt', 'r', encoding='utf-8') as f:
    dev_requirements = f.read().splitlines()

setup(
    name='hermes',
    version='1.0.0-alpha1',
    url='https://github.com/dclause/hermes',
    license='GNU-GPLv3',
    author='Dominique CLAUSE',
    author_email='contact@acino.fr',
    description='HERMES - a Robot Management System (RMS)',
    scripts=['hermes', 'documentation'],

    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
    }
)
