from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='archive-manager',
    version='0.1.1',
    author='Curtis Collicutt',
    author_email='Curtis Collicutt',
    description='Manage backup archive files',
    url="https://github.com/ccollicutt/archive-manager",
    long_description=readme,
    python_requires='>=2.7, !=3.*',
    license="Apache License, Version 2.0",
    packages=['archive_manager'],
    install_requires=[
        'click',
        'pyyaml'
    ],
    tests_require=[
        'fallocate',
        'coverage'
    ],
    entry_points={
        'console_scripts': [
            'archive-manager=archive_manager.interface:cli',
        ],
    },
)