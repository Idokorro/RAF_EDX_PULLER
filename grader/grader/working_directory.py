import os
from shutil import copy, rmtree
from tempfile import NamedTemporaryFile, mkdtemp

class WorkingDirectory(object):
    def __init__(self, tester_path, solution_path):
        self.path = mkdtemp()
        self.tester_path = self._copy(tester_path)
        self.solution_path = self._copy(solution_path)


    def _copy(self, file_path):
        if os.path.isdir(file_path):
            files = os.listdir(file_path)
            return [self._copy(os.path.join(file_path, name)) for name in files]
        return copy(file_path, self.path)

    def remove(self):
        if not os.path.exists(self.path):
            raise IOError("{} already doesn't exist".format(self.path))
        rmtree(self.path)

    def files_in_path(self):
        return os.listdir(self.path)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.remove()

    def __str__(self):
        return "<Assets: %s %s>" % (self.tester_path, self.solution_path)