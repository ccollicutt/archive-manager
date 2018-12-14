from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='archive-manager',
    version='0.1.2',
    author='Curtis Collicutt',
    author_email='curtis@serverascode.com',
    description='Manage backup archive files',
    url="https://github.com/ccollicutt/archive-manager",
    download_url="https://github.com/ccollicutt/archive-manager/archive/v0.1.2.tar.gz",
    long_description=readme,
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