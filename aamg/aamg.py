#!/usr/bin/env python3

import argparse

from . import generator


def aamg() -> None:
    '''This is the main entrypoint for our program.'''
    parser = argparse.ArgumentParser(description='Get an automatically '
                                     'generated astrophysical model')
    parser.add_argument('--grammar', '-g', dest='grammar', default='GRAMMAR',
                        type=str, help='the file to use as grammar input')
    parser.add_argument('--assets', '-a', dest='assets', default='ASSETS',
                        type=str, help='the file to use as the asset list')
    parser.add_argument('--verbose', '-v', dest='verbose', default=False,
                        action='store_true', help='enable verbose')
    args = parser.parse_args()

    # This initializes our handle
    model_generator = generator.ModelGenerator(args)

    # This is where the magic happens
    print(model_generator.generate_model())


if __name__ == '__main__':
    aamg()
