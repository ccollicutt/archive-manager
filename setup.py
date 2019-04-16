from setuptools import setup

# read the contents of your README file
from os import path
import io
this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with io.open(path.join(this_directory, 'VERSION'), encoding='utf-8') as f:
    # Just read first line
    version = f.readline()
    version = version.strip()

download_url = "https://github.com/ccollicutt/archive-manager/archive/v%s.tar.gz" % version

# NOTE: package_data...not sure if this is working in all cases, eg. rpm, sdist, etc.
setup(
    name='archive-manager',
    version=version,
    author='Curtis Collicutt',
    author_email='curtis@serverascode.com',
    description='Manage backup archive files',
    url="https://github.com/ccollicutt/archive-manager",
    download_url=download_url,
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6.6',
    license="Apache License, Version 2.0",
    keywords = ['backup', 'file manager', 'archive', 'archive manager'],
    test_suite='archive_manager.test_archive_manager',
    packages=['archive_manager'],
    package_data={'VERSION': ['VERSION']},
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