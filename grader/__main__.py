import os
import argparse

from grader import grader
from grader import config
from grader import utils

def is_valid_path(path, raiseError=True):
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        if raiseError:
            raise argparse.ArgumentTypeError("{0} does not exist".format(abs_path))
        return None
    return abs_path

def is_valid_language(lang, raiseError=True):
    if lang not in config.LANGUAGES:
        if raiseError:
            raise argparse.ArgumentTypeError("This language({0}) is not supported".format(lang))
    return lang

parser = argparse.ArgumentParser(description='Test a program.')

parser.add_argument('lang', type=is_valid_language)
parser.add_argument('tester_path', type=is_valid_path)
parser.add_argument('solution_path', type=is_valid_path)

args = parser.parse_args()

result = grader.test_solution(args.lang, args.tester_path, args.solution_path)

print(utils.dump_json(result))