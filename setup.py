from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='archive-manager',
    version='0.1',
    author='Curtis Collicutt',
    author_email='Curtis Collicutt',
    description='Manager files in a directory',
    long_description=readme,
    license="Apache License, Version 2.0",
    packages=['archive_manager'],
    install_requires=[
        'click',
        'pyyaml'
    ],
    tests_require=[
        'fallocate'
    ],
    entry_points={
        'console_scripts': [
            'archive-manager=archive_manager.interface:cli',
        ],
    },
)