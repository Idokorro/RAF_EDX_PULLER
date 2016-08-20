from grader import grader
from functools import wraps

def test(test_function):
    """ Decorator for a test. The function should take a single argument which
        is the object containing stdin, stdout and module (the globals of users program).

        The function name is used as the test name, which is a description for the test
        that is shown to the user. If the function has a docstring, that is used instead.

        Raising an exception causes the test to fail, the resulting stack trace is
        passed to the user. """
    assert hasattr(test_function, '__call__'), "test_function should be a function, got " + repr(test_function)

    @wraps(test_function)
    def wrapper(module, *args, **kwargs):
        if module.caughtException:
            raise module.caughtException
        result = test_function(module, *args, **kwargs)
        if module.caughtException:
            raise module.caughtException
        return result

    name = grader.get_test_name(test_function)
    grader.testcases[name] = wrapper
    return wrapper