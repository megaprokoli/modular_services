from abc import ABC, abstractmethod


class AbstractService(ABC):
    instances = []    # list of all instances

    def __init__(self):
        super().__init__()
        self.cmd_map = {}    # (str)name : (func)function
        self.name = None
        self.version = None
        self.author = None
        self.update = None
        self._default_help = {"content": "help - get this help text\ninfo - get info about service\n"}
        self._dependencies = None   # dict containing dependencies like e.g a database interface or GUI component

        AbstractService.instances.append(self)

        self.register_cmd("help", self.help)
        self.register_cmd("info", self.get_info)

    @staticmethod
    def get_instance():
        pass

    @abstractmethod
    def help(self):
        pass

    def inject_dependencies(self, dep: dict):
        self._dependencies = dep

    def get_info(self):
        return {"name": self.name, "author": self.author,
                "last_update": self.update, "version": self.version}

    def set_info(self, name, author, update, version):
        self.name = name
        self.author = author
        self.update = update
        self.version = version

    def set_name(self, name):
        self.name = name

    def register_cmd(self, cmd, func):
        self.cmd_map.update({cmd: func})

    def exec(self, cmd, arg: dict = None):
        func = self.cmd_map[cmd]

        if arg is None:
            return func()
        elif hasattr(arg, "__iter__"):  # is iterable
            return func(**arg)
        else:
            raise ValueError("Service exec: arg must be dict or none")
