import logging
import os

_logger = logging.getLogger(__name__)

def find_in_path(name):
    path = os.environ.get('PATH', os.defpath).split(os.pathsep)
    