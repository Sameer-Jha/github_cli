
from setuptools import setup, find_packages
from github.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='github',
    version=VERSION,
    description='A cli based tools for basic github platform operation like creating a new repo, branch etc.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Sameer Jha',
    author_email='sameer.btech.cs17@iiitranchi.ac.in',
    url='https://github.com/Sameer-Jha/github_cli',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'github': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        github = github.main:main
    """,
)
