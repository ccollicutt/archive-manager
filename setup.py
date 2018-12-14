from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='archive-manager',
    version='0.1.3',
    author='Curtis Collicutt',
    author_email='curtis@serverascode.com',
    description='Manage backup archive files',
    url="https://github.com/ccollicutt/archive-manager",
    download_url="https://github.com/ccollicutt/archive-manager/archive/v0.1.2.tar.gz",
    long_description=long_description,
    long_description_content_type='text/markdown'
    python_requires='>=2.7, !=3.*',
    license="Apache License, Version 2.0",
    keywords = ['backup', 'file manager', 'archive', 'archive manager'],
    test_suite='archive_manager.test_archive_manager',
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