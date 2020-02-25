'''Setup script for the aamg library and the aamg-gen cli tool.'''

import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    required = f.read().splitlines()

setuptools.setup(

    # Project info
    name='aamg',
    url='https://github.com/bandang0/aamg',
    description='Automatic Astrophysical Model Generator',
    long_description_content_type="text/markdown",
    long_description=long_description,
    license="MIT",

    # Environment
    python_requires='>=3.6',

    # Scripts and packages.
    scripts=['bin/aamg-gen'],
    packages=['aamg'],

    # Load requirements from file in project root.
    install_requires=required
)
