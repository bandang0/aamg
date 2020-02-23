import typing
import random

import log


def generate_rule(grammar: typing.Dict[str, typing.List[str]],
        assets: typing.Dict[str, typing.List[str]],
        rule_value: typing.List[str]) -> str:
    '''Get the string for a rule'''

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
                out.append(e[1:-1])
        # Check if this another rule first
        elif e in grammar.keys():
            out.append(generate_rule(grammar, assets, grammar[e]))
        # Then check if it is an asset
        elif e in assets.keys():
            out.append(random.choice(assets[e]))
        # Parse parenthesis and call subfunction
        elif e == '(':
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
                out.append(generate_rule(grammar, assets, random.choice(choices)))
                i += 1
            else:
                log.die(f'unclosed parenthesis')

        elif e == ')':
            log.die(f'unmatched ) in rule:\n\t{" ".join(rule_value)}')
        else:
            log.die(f'unknown token:\n\t{e}')
        i += 1

    return ' '.join(out)

def generate_model(grammar: typing.Dict[str, typing.List[str]],
        assets: typing.Dict[str, typing.List[str]]) -> str:
    '''Generate a new model'''

    return generate_rule(grammar, assets, grammar['model'])
