import unittest


def aamg_test_suite():
    '''This discovers tests automatically for us and is called by `setup.py`'''
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='*_test.py')
    return test_suite
