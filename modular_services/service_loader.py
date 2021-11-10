import os
import importlib
import inspect
import json
import logging


class ServiceLoader:
    def __init__(self, service_dir):
        self.has_loaded = False
        self.module_root = service_dir
        self.unnamed_count = 0
        self.services = {}

    def load(self, dependencies: dict = None):
        logger = logging.getLogger("ServiceSystem")

        for file in os.listdir(self.module_root):
            if file == "__pycache__":
                continue

            try:
                with open(self.module_root + "/" + file + "/index.json") as index_file:
                    index = json.load(index_file)
                    main_file = index["main_file"]
            except FileNotFoundError:
                logger.error("index.json for " + file + " not found")
                continue

            imported = importlib.import_module(self.module_root + "." + file + "." + main_file.split(".")[0])
            class_obj = inspect.getmembers(imported)[1][1]

            instance = class_obj.get_instance()

            if not instance:
                logger.error("class could not be instantiated for file: " + file)
                continue

            try:
                instance.set_info(index["module_name"], index["author"], index["last_update"], index["version"])
            except KeyError:
                logger.error("index file for " + file + " may be corrupted")
                continue

            if instance.name is None:
                instance.name = "unnamed_service_" + str(self.unnamed_count + 1)

            instance.inject_dependencies(dependencies)  # inject dependencies needed by services

            self.services.update({instance.name: instance})
        self.has_loaded = True

    def get_service(self, name):
        try:
            module = self.services[name]
        except KeyError as err:
            logger = logging.getLogger("ServiceSystem")
            logger.warning(err)
            return None
        return module

    def list_services(self):
        for mod_name in self.services:
            print("- ", mod_name, " loaded")
