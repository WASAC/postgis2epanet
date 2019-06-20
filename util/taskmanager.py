from light_progress.commandline import ProgressBar
from light_progress import widget
import threading


class TaskManager(object):
    def __init__(self, tasks, no_threads=10):
        self.tasks = tasks
        self.no_threads = no_threads
        widgets = [widget.Bar(bar='*', tip='>'),
                   widget.Percentage(),
                   widget.Num(),
                   widget.ElapsedSeconds(),
                   widget.FinishedAt()]
        self.pb = ProgressBar(len(self.tasks), widgets=widgets)

    def start(self):
        self.pb.start()
        for i in range(0, self.no_threads):
            self.thread_start()

    def pop(self):
        if len(self.tasks) == 0:
            return
        task = self.tasks.pop()
        self.pb.forward()
        if len(self.tasks) == 0:
            self.pb.finish()
        return task

    def thread_start(self):
        if len(self.tasks) > 0:
            thread = threading.Thread(target=self.execute)
            thread.start()

    def execute(self):
        t = self.pop()
        if not t:
            return
        t.execute()
        self.thread_start()
