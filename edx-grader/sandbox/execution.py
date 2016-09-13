from time import sleep

from grader.grader import testcases
from grader.utils import import_module, get_error_message, get_traceback, dump_json
from sandbox.program_container import ProgramContainer

RESULT_DEFAULTS = {
    "log": [],
    "error_message": "",
    "traceback": ""
}

def call_all(function_list, *args, **kwargs):
    for fun in function_list:
        fun(*args)

def call_test_function(test_index, language, tester_path, solution_path):
    """ Called in another process. Finds the test `test_name`,  calls the
        pre-test hooks and tries to execute it.

        If an exception was raised by call, prints it to stdout """

    import_module(tester_path)

    test_name = list(testcases.keys())[test_index]
    testcase = testcases[test_name]

    # pre-test hooks
    pre_hook_info = {
        "test_name": test_name,
        "tester_path": tester_path,
        "solution_path": solution_path,
        "extra_args": [],
        "extra_kwargs": {}
    }
    call_all(testcase._options["pre-hooks"], pre_hook_info)

    results = RESULT_DEFAULTS.copy()

    module = None
    # start users program
    try:
        module = ProgramContainer(language, solution_path, results)
        while not hasattr(module, "module"):
            sleep(0.001)
        module.condition.acquire()
        testcase._function(
            module,
            *pre_hook_info["extra_args"],
            **pre_hook_info["extra_kwargs"]
        )
    except Exception as e:
        if module.caughtException is not None:
            e = module.caughtException
        results["error_message"] = get_error_message(e)
        results["traceback"] = get_traceback(e)
        raise
    finally:
        module.restore_io()
        print(dump_json(results))