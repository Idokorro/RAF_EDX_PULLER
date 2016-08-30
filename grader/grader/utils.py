import json
import traceback
from collections import OrderedDict


def get_error_message(exception):
    type_ = type(exception)
    return "{}: {}".format(type_.__name__, str(exception))


def get_traceback(exception):
    type_, value, tb = type(exception), exception, exception.__traceback__
    return "".join(traceback.format_exception(type_, value, tb))


def load_json(json_string):
    " Loads json_string into an dict "
    return json.loads(json_string)


def dump_json(ordered_dict):
    " Dumps the dict to a string, indented "
    return json.dumps(ordered_dict, indent=4)


def import_module(path, name=None):
    if name is None:
        name = path
    import importlib.machinery
    loader = importlib.machinery.SourceFileLoader(name, path)
    module = loader.load_module(name)
    return module


class OrderedDictionary(OrderedDict):

    def load_from(self, module_path):
        self.clear()
        import_module(module_path)


def call_all(function_list, *args, **kwargs):
    for fun in function_list:
        fun(*args)
