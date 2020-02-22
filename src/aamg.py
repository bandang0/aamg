#!/usr/bin/env python3

import argparse
import sys


def log(msg: str) -> None:
    '''Log a message'''
    print(f'[\033[0;32m*\033[0m] {msg}', file=sys.stderr)

def warn(msg: str) -> None:
    '''Log a warning'''
    print(f'[\033[0;33m*\033[0m] {msg}', file=sys.stderr)

def die(msg: str) -> None:
    '''Log an error and exit'''
    print(f'[\033[0;31m*\033[0m] {msg}', file=sys.stderr)
    sys.exit(1)

def parse_grammar(grammar_file: str) -> None:
    '''Parse grammar file'''
    pass

def load_assets(asset_list: str) -> dict:
    '''Load assets from the asset list file'''
    try:
        with open(asset_list, 'r') as f:
            lines = (line.strip().split('=') for line in f.readlines())
    except OSError as e:
        die(f'{asset_list}: {e.strerror}')

    assets = dict()
    for line in lines:
        if line[0] not in assets.keys():
            try:
                with open(line[1], 'r') as f:
                    assets[line[0]] = list(line.strip()
                            for line in f.readlines())
            except OSError as e:
                die(f'{line[1]}: {e.strerror}')
        else:
            warn(f'ignoring duplicate asset file: {" ".join(line)}')
    return assets

def check_assets(grammar: None, assets: dict) -> bool:
    '''Check we have all the assets we need to respect our grammar'''
    return True

def generate_model(grammar: None, assets: dict) -> str:
    '''Generate a new model'''
    return ''

def aamg() -> None:
    '''This is the main entrypoint for our program.'''
    parser = argparse.ArgumentParser(description=
            'Get an automatically generated astrophysical model')
    parser.add_argument('--grammar', '-g', dest='grammar', default='grammar',
            type=str, help='the file to use as grammar input')
    parser.add_argument('--assets', '-a', dest='assets', default='assets',
            type=str, help='the file to use as the asset list')
    args = parser.parse_args()

    log(f'using \'{args.grammar}\' as a grammar')
    log(f'using \'{args.assets}\' as an asset list file')

    grammar = parse_grammar(args.grammar)
    log('parsed grammar')

    assets = load_assets(args.assets)
    log('loaded assets')

    if not check_assets(grammar, assets):
        die('asset check failed')

    print(generate_model(grammar, assets))

if __name__ == '__main__':
    aamg()
