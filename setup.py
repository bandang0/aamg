import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(

    # Project info
    name='aamg',
    url='https://github.com/bandang0/aamg',
    description='Automatic Astrophysical Model Generator',
    long_description_content_type="text/markdown",
    long_description=long_description,
    license="MIT",

    # Scripts and packages.
    scripts=['bin/aamg-gen'],
    packages=['aamg'],

    # Set our test suite so we can use `python3 setup.py test` to run tests.
    test_suite='tests.suite.aamg_test_suite',

    # Load requirements from file in project root.
    install_requires=required
)
