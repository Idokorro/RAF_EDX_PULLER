from grader.grader import working_directory
from grader.grader import runner
from grader.grader import utils

DEFAULT_TEST_SETTINGS = {
    # hooks that run before tests
    "pre-hooks": (),
    # hooks that run after tests
    "post-hooks": (),
    # timeout for function run
    "timeout": 1.0
}

testcases = utils.OrderedDictionary()



def test_solution(lang, tester_path, solution_path):

    with working_directory.WorkingDirectory(tester_path, solution_path) as directory:

        try:
            testcases.load_from(tester_path)
        except Exception as e:
            return _test_load_failure(e)

        if len(testcases) == 0:
            return _fail_result("No tests found in tester")

        test_results = [runner.run_testcase(lang, directory.tester_path, directory.solution_path, test_name, {}) for test_name in testcases]

    results = {"results": test_results, "success": True}
    return results

def _fail_result(reason, **extra_info):
    result = {
        "success": False,
        "reason": reason,
        "extra_info": extra_info
    }
    return result

def _test_load_failure(exception):
    from . import utils
    return _fail_result(
        "Load tests failure",
        error_message=utils.get_error_message(exception),
        traceback=utils.get_traceback(exception))

def get_test_name(function):
    """ Returns the test name as it is used by the grader. Used internally. """
    name = function.__name__
    # if inspect.getdoc(function):
    #     name = utils.beautifyDescription(inspect.getdoc(function))
    return name

def get_setting(test_function, setting_name):
    """ Returns a test setting. Used internally. """
    if isinstance(test_function, str):
        test_function = testcases[test_function]
    if not hasattr(test_function, "_grader_settings_"):
        # copy default settings
        test_function._grader_settings_ = DEFAULT_TEST_SETTINGS.copy()
    return test_function._grader_settings_[setting_name]