# server_extensions is deprecated, use nbserver_extensions instead (below).
# c.NotebookApp.server_extensions = [
#     'ganymede.ganymede',
# ]
# This line activates the Ganymede extension.
c.NotebookApp.nbserver_extensions = {
    'ganymede.ganymede':'ganymede.ganymede',
}

"""
# To append the current notebook path in the generated JSON message as a key-value pair:
# K = "filepath", V = relative path to notebook from Jupyter homedir.
from ganymede.ganymede import GanymedeHandler
GanymedeHandler.include_filepath = True
"""

"""
# To overwrite the default logging handler, i.e. logging.StreamHandler(stream=sys.stdout)
import logging
GanymedeHandler.handlers = [
    logging.NullHandler(),
]
"""
