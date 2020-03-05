# AAMG : Automatic Astrophysical Model Generator

Automatically generate random sentences from a given grammar and lists of words.

## Usage

`aamg-gen [(--grammar | -g) GRAMMARFILE] [(--assets | -a) ASSETSFILE]`

See examples in the `examples/` folder.

## Installation

To install the aamg library and the aamg-gen script run:

```
    $ python setup.py install
```

The previous command might need administrative privileges if you are not in a
virtual environment.

##  Development setup

To fetch all dependencies just use:

```
    $ pip install -r requirements.txt
```

The previous command might need administrative privileges if you are not in a
virtual environment.

## Running our tests

If you want to run our tests you can simply clone the repository and run the
following command:

```
    $ tox
```

This requires to have the `tox` program installed. This can be done from the PyPI.
## Writing tests

There are comments and template tests you can copy/paste and edit in most
files.
