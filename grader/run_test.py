from os import path
from sys import argv, exit
from grader.runner import *
from grader.working_directory import WorkingDirectory


if len(argv) < 5:
    print("Usage: run_test <lang> <tester-path> <solution-path> <test-index>")
    exit(1)

with WorkingDirectory(argv[2], argv[3]) as directory:
    lang = argv[1]
    test_index = int(argv[4])
    # print(directory)
    check_testcase(lang, directory.tester_path, directory.solution_path, test_index)
    #check_testcase(lang, argv[2], directory.solution_path, test_index)
