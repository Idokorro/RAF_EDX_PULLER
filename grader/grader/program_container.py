import sys
from os import path
from .terminal import *
from .config import *
from threading import Thread
from .stdio import SyncCondition, SpoofedStdin, SpoofedStdout

STATUS = 0
RESULT = 1
EXCEPTION = 2

class ProgramContainer(Thread):
    """ The thread in which the users program runs """

    def __init__(self, lang, module_path, results):
        Thread.__init__(self)

        self.module_path = module_path
        self._results = results
        self.condition = SyncCondition()
        self.lang = lang
        self.caughtException = None
        self.__startProgram()

    def __startProgram(self):
        self.setDaemon(True)
        self.start()
        self._started = False
        #while not self._started:
        #    sleep(0.001)

    def run(self):
        self.stdin = sys.stdin = SpoofedStdin(self.condition)
        self.stdout = sys.stdout = SpoofedStdout()

        self.condition.acquire()
        self._started = True
        self.finished = False

        try:
            self._exec_code()
        except Exception as error:
            self.caughtException = error
        # notify tester of the end of program
        self.condition.notify_release()
        self.condition.finish()
        self.finished = True
        self.response = "Test"

    def _exec_code(self):
        file_path = path.dirname(self.module_path)
        file_name = path.basename(self.module_path)

        response = terminal.call_command(config.calculate_compile_command(self.lang, file_path, file_name))

        if response[STATUS] == 0:
            response = terminal.call_command(config.calculate_run_command(self.lang, file_path, file_name))
            self.stdout.write(response[RESULT])
        else:
            raise Exception(response[EXCEPTION])
        return response

    def log(self, what):
        self._results["log"].append(what)

    @classmethod
    def restore_io(cls):
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__