from abc import abstractmethod
from threading import Thread

from service_sys.abstract_service import AbstractService


class DeamonService(AbstractService):
    def __init__(self):
        super().__init__()
        self._is_active = False
        self._service_thread = None

        self._default_help["content"] += "run - start service thread\nkill - stop service thread\n"

        self.register_cmd("run", self.run)
        self.register_cmd("kill", self.kill)

    @abstractmethod
    def help(self):
        pass

    @abstractmethod
    def service_func(self, is_active: bool):
        pass

    def run(self):
        if not self._is_active:
            self._service_thread = Thread(target=self.service_func, name=f"{self.name}-ServiceThread")
            self._service_thread.start()
            self._is_active = True

    def kill(self):
        self._is_active = False
