import logging

_logger = logging.getLogger(__name__)

class Graph(dict):
    def add_node(self, name, info):
        pass

    def update_from_db(self, cr):
        pass

    def add_module(self, cr, module, force=None):
        pass

    def add_modules(self, cr, module_list, force=None):
        pass

    def __iter__(self):
        pass

    def __str__(self):
        pass

class Node(object):
    def __new__(cls, name, graph, info):
        pass

    def __init__(self, name, graph, info):
        pass

    @property
    def data(self):
        pass

    def add_child(self, name, info):
        pass

    def __setattr__(self, key, value):
        pass

    def __iter__(self):
        pass

    def __str__(self):
        pass

    @property
    def parents(self):
        pass