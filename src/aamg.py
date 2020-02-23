#!/usr/bin/env python3

import argparse
import sys
import typing

import model
import log


def parse_grammar(grammar_file: str) -> typing.Dict[str, typing.List[str]]:
    '''Parse grammar file'''
    try:
        with open(grammar_file, 'r') as f:
            lines = (line.strip().split('=') for line in f.readlines())
    except OSError as e:
        log.die(f'{asset_list}: {e.strerror}')
    grammar: typing.Dict[str, str] = dict()
    for line in lines:
        if len(line) == 1 or line[0].lstrip()[0] == '#':
            continue
        elif line[0] not in grammar.keys():
            grammar[line[0]] = '='.join(line[1:]).split()
        else:
            log.warn(f'ignoring duplicate rule file: "{" ".join(line)}"')
    if 'model' not in grammar.keys():
        log.die('you must define a rule called \'model\' in your grammar file')
    return grammar

def load_assets(asset_list: str) -> typing.Dict[str, typing.List[str]]:
    '''Load assets from the asset list file'''
    try:
        with open(asset_list, 'r') as f:
            lines = (line.strip().split('=') for line in f.readlines())
    except OSError as e:
        log.die(f'{asset_list}: {e.strerror}')

    assets: typing.Dict[str, typing.List[str]] = dict()
    for line in lines:
        if len(line) < 2:
            log.die(f'empty value for asset file')
        elif line[0] not in assets.keys():
            try:
                with open(line[1], 'r') as f:
                    assets[line[0]] = list(line.strip()
                            for line in f.readlines())
                    if (len(assets[line[0]]) == 0):
                        log.die('empty asset key')
            except OSError as e:
                log.die(f'{line[1]}: {e.strerror}')
        else:
            log.warn(f'ignoring duplicate asset file: "{" ".join(line)}"')

    return assets

def aamg() -> None:
    '''This is the main entrypoint for our program.'''
    parser = argparse.ArgumentParser(description=
            'Get an automatically generated astrophysical model')
    parser.add_argument('--grammar', '-g', dest='grammar', default='grammar',
            type=str, help='the file to use as grammar input')
    parser.add_argument('--assets', '-a', dest='assets', default='assets',
            type=str, help='the file to use as the asset list')
    args = parser.parse_args()

    log.info(f'using \'{args.grammar}\' as a grammar')
    log.info(f'using \'{args.assets}\' as an asset list file')

    grammar = parse_grammar(args.grammar)
    log.info('parsed grammar')

    assets: typing.Dict[str, typing.List[str]] = load_assets(args.assets)
    log.info('loaded assets')

    print(model.generate_model(grammar, assets))

if __name__ == '__main__':
    aamg()
