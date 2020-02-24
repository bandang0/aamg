#!/usr/bin/env python3

import sys
import typing
import unittest
import unittest.mock

sys.path.insert(0, 'src')

import generator


def launch_test_with_mock_file(func: typing.Callable,
    file_content: str) -> unittest.mock.Mock:
    '''Takes a function and a file content and returns a Mock object
    which mimics our ModelGenerator's behaviour when calling the function with
    that filename in the correct `args` member.'''

    mock: unittest.mock.Mock = unittest.mock.Mock()
    mock.args.grammar: str = str()
    mock.args.assets: str = str()
    mock.args.verbose: bool = False
    mock.grammar: typing.Dict[str, typing.List(str)] = dict()
    mock.assets: typing.Dict[str, typing.List(str)] = dict()

    # Patch the `open` function so we can mock the file opening in `func`
    with unittest.mock.patch(f'builtins.open',
            unittest.mock.mock_open(read_data=file_content), create=True):

        # Give the mock as the `self` parameter to our function
        func(mock)

    return mock

class TestGrammarLexer(unittest.TestCase):
    '''This tests grammar lexing'''

    def test_function_call_template(self) -> None:
        '''Easiest test ever. You can use this as a copy/paste template.'''

        # This represents the `dict` you expect your `mock` after the function
        # call.
        # The keys are rule names and the value is the list of tokens
        # associated with that rule.
        expected_dict = dict()
        expected_dict['model'] = ['test']

        # This is the content of the input file you want to mock during this
        # test.
        file_content: str = 'model=test\n'

        # Here is the call to the function defined earlier with the function we
        # want to test and our wanted file content as parameters.
        mock = launch_test_with_mock_file(
                generator.ModelGenerator.parse_grammar,
                file_content)

        # Our `mock` object now has the data our ModelGenerator would usually
        # have so we can assert it is what we expected.
        self.assertEqual(mock.grammar, expected_dict)

    def test_random(self) -> None:
        '''This is just the first thing I tried so it stayed here'''

        expected_dict: typing.Dict[str, typing.List[str]] = dict()
        expected_dict['model'] =   ['\'The\'', 'subject', '(', 'adv', '|', 
                'adv', '\'and\'', 'adv', ')', 'verb', '(', '\'a\'', '|',
                '\'theonly\'', ')', 'object']
        expected_dict['subject'] = ['"The"', '\'sdf\''] 

        file_content: str = str()
        file_content += "model='The' subject ( adv | adv 'and' adv )  verb "
        file_content += "( 'a' | 'theonly' ) object\n"
        file_content += "model='The' subject ( animal | adv ) verb \"ffds\"\n"
        file_content += "subject=\"The\" 'sdf'\n"
        file_content += "\n"
        file_content += "### asdf\n"
        file_content += "\n"
        file_content += "# ignored\n"
        file_content += "model='The' subject [ ( adv | adv 'and' adv ) ] verb "
        file_content += "|( 'a' | 'the only' ) object\n"
        file_content += "\n"
        file_content += "\n"
        file_content += "subject=( animal | num animals )\n"
        file_content += "\n"
        file_content += "\n"

        mock = launch_test_with_mock_file(
                generator.ModelGenerator.parse_grammar,
                file_content)

        self.assertEqual(mock.grammar, expected_dict)


if __name__ == '__main__':
    unittest.main()
