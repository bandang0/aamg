import argparse
import random
import typing

from . import log


class ModelGenerator:
    '''This is the main handle for our generator'''

    def __init__(self, args: argparse.Namespace) -> None:
        '''Initialize our handle'''
        self.args = args
        self.parse_grammar()
        self.load_assets()

    def parse_grammar(self) -> None:
        '''Parse grammar file'''
        if self.args.verbose:
            log.info(f'loading grammar file: {self.args.grammar}')
        try:
            with open(self.args.grammar, 'r') as f:
                lines = (line.strip().split('=') for line in f.readlines())
        except OSError as e:
            log.die(f'{self.args.grammar}: {e.strerror}')
        self.grammar: typing.Dict[str, typing.List[str]] = dict()
        for line in lines:
            if len(line) == 1 or line[0].lstrip()[0] == '#':
                continue
            elif line[0] not in self.grammar.keys():
                self.grammar[line[0]] = '='.join(line[1:]).split()
            else:
                if self.args.verbose:
                    log.warn('ignoring duplicate rule file: '
                             f'"{" ".join(line)}"')
        if 'model' not in self.grammar.keys():
            log.die('you must define a rule called \'model\' '
                    'in your grammar file')

        return

    def load_assets(self) -> None:
        '''Load assets from the asset list file'''
        if self.args.verbose:
            log.info(f'loading asset list file: {self.args.assets}')
        try:
            with open(self.args.assets, 'r') as f:
                lines = (line.strip().split('=') for line in f.readlines())
        except OSError as e:
            log.die(f'{asset_list}: {e.strerror}')

        self.assets: typing.Dict[str, typing.List[str]] = dict()
        for line in lines:
            if len(line) < 2:
                log.die(f'empty value for asset file')
            elif line[0] not in self.assets.keys():
                if self.args.verbose:
                    log.info(f'loading asset file: {line[0]}')
                try:
                    with open(line[1], 'r') as f:
                        self.assets[line[0]] = list(line.strip()
                                                    for line in f.readlines())
                        if (len(self.assets[line[0]]) == 0):
                            log.die('empty asset key')
                except OSError as e:
                    log.die(f'{line[1]}: {e.strerror}')
            else:
                if self.args.verbose:
                    log.warn(f'ignoring duplicate asset file: '
                             f'"{" ".join(line)}"')

        return

    def generate_model(self) -> str:
        '''Let's generate a model by producing a string for the rule `model`'''

        return self.generate_rule(self.grammar['model'])

    def generate_rule(self, rule_value: typing.List[str]) -> str:
        '''Get the string for a rule'''

        if self.args.verbose:
            log.info(f'generating string for rule: {" ".join(rule_value)}')

        out: typing.List[str] = list()
        i: int = 0
        while i < len(rule_value):
            e = rule_value[i]

            # This is a string litteral
            if e[0] == '\'' or e[0] == '"':

                # XXX: handle this better
                if e[-1] != '\'' and e[-1] != '"':
                    log.die('unclosed string litteral')
                else:
                    if self.args.verbose:
                        log.info(f'found string litteral: {e}')
                    out.append(e[1:-1])
            # Check if this another rule first
            elif e in self.grammar.keys():
                if self.args.verbose:
                    log.info(f'found rule: {e}')
                out.append(self.generate_rule(self.grammar[e]))
            # Then check if it is an asset
            elif e in self.assets.keys():
                if self.args.verbose:
                    log.info(f'found asset: {e}')
                out.append(random.choice(self.assets[e]))
            # Parse parenthesis and call subfunction
            elif e == '(':
                if self.args.verbose:
                    log.info(f'found (: {e}')
                choices: typing.List[typing.List[str]] = list([[]])
                par_count: int = 0
                while i < len(rule_value):
                    if rule_value[i] == ')':
                        if par_count == 1:
                            break
                        par_count -= 1
                    elif rule_value[i] == '(':
                        par_count += 1
                    elif rule_value[i] == '|':
                        choices.append([])
                    else:
                        choices[-1].append(rule_value[i])
                    i += 1

                if i < len(rule_value):
                    if self.args.verbose:
                        log.info(f'choices: {[" ".join(c) for c in choices]}')
                    out.append(self.generate_rule(random.choice(choices)))
                else:
                    log.die(f'unclosed parenthesis')

            elif e == ')':
                log.die(f'unmatched ) in rule:\n\t{" ".join(rule_value)}')
            else:
                log.die(f'unknown token:\n\t{e}')
            i += 1

        return ' '.join(out)
