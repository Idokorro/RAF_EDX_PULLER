from time import time, sleep

from grader import grader
from grader import utils
from grader import program_container

RESULT_DEFAULTS = {
    "log": [],
    "error_message": "",
    "traceback": ""
}

def call_all(function_list, *args, **kwargs):
    for fun in function_list:
        fun(*args)

def run_testcase(lang, tester_path, solution_path, test_name, options):
    """ Calls the test, checking if it doesn't raise an Exception.
        Returns a dictionary in the following form::

            {
                "success": boolean,
                "traceback": string ("" if None)
                "error_message: string
                "time": string (execution time, rounded to 3 decimal digits)
                "description": string (test name/its description)
            }

        If the test timeouts, traceback is set to "timeout".

        Post-hooks can manipulate with the test results before returning.
    """
    from grader import terminal

    #TODO: zakucane stvari
    options["timeout"] = 10.0 #grader.get_setting(test_name, "timeout")
    test_index = 0

    start = time()
    success, stdout, stderr = terminal.run_test(lang, tester_path, solution_path, test_index, options)
    end = time()

    result = RESULT_DEFAULTS.copy()
    if (end - start) > options["timeout"]:
        result["error_message"] = "Timeout"
        result["traceback"] = "Timeout"
    else:
        try:
            result = utils.load_json(stdout)
        except Exception as e:
            result["traceback"] = stdout
            result["stderr"] = stderr

    result.update(success=success, description=test_name, time=("%.3f" % (end - start)))
    # after test hooks - cleanup
    utils.call_all(grader.get_setting(test_name, "post-hooks"), result)
    return result

def check_testcase(lang, tester_path, solution_path, test_index):
    """ Called in another process. Finds the test `test_name`,  calls the
        pre-test hooks and tries to execute it.

        If an exception was raised by call, prints it to stdout """
    utils.import_module(tester_path)
    test_name = list(grader.testcases.keys())[test_index]
    test_function = grader.testcases[test_name]

    pre_hook_info = {
        "test_name": test_name,
        "tester_path": tester_path,
        "solution_path": solution_path,
        "extra_args": [],
        "extra_kwargs": {}
    }
    call_all(grader.get_setting(test_name, "pre-hooks"), pre_hook_info)

    results = RESULT_DEFAULTS.copy()

    # start users program
    try:
        module = program_container.ProgramContainer(lang, solution_path, results)
        while not hasattr(module, "response"):
            sleep(0.001)
        module.condition.acquire()
        test_function(module, *pre_hook_info["extra_args"], **pre_hook_info["extra_kwargs"])
    except Exception as e:
        if module.caughtException is not None:
            e = module.caughtException
        results["error_message"] = utils.get_error_message(e)
        results["traceback"] = utils.get_traceback(e)
        raise
    finally:
        module.restore_io()
        print(utils.dump_json(results))