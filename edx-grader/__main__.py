"""
Executed when using `python -m grader <tester_path> <solution_path> [<other_files>...]`.

Tests the module and prints the results (json) to console.
"""
import os
import argparse

from grader.utils import dump_json
from grader.grader import test_submission

def is_valid_path(path, raiseError=True):
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        if raiseError:
            raise argparse.ArgumentTypeError("{0} does not exist".format(abs_path))
        return None
    return abs_path


parser = argparse.ArgumentParser(description='Test a program.')
parser.add_argument('language')
parser.add_argument('tester_path', type=is_valid_path)
parser.add_argument('solution_path', type=is_valid_path)
parser.add_argument('assets', type=is_valid_path, nargs="*")


args = parser.parse_args()

result = test_submission(
    args.language,
    args.tester_path,
    args.solution_path,
    args.assets
)

print(dump_json(result))
