c.NotebookApp.server_extensions = [
    'ganymede.ganymede',
]

"""
# To include custom logging handlers on the GanymedeHandler request handler.
from ganymede.ganymede import GanymedeHandler
import logging
GanymedeHandler.handlers = [
    logging.NullHandler(),
]
"""
