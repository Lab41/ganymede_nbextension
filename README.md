# Ganymede NBExtension

This project is an extension for Jupyter Notebook that provides logging of code input and output. This is done by placing a hook onto the messages which are sent and received to the underlying Jupyter protocol.
The goal is to accurately reconstruct a user's interactive session by logging the inputs and outputs for each cell in a Jupyter notebook,

The generated logs are in JSON format. By default, they are logged to STDOUT, but can be configured to log to a file or to a Logstash server directly. 

## Install

After cloning the repository, cd inside of ganymede_nbextension/ then use pip to install the requirements and the actual extension itself.

`
pip install -r requirements.txt .
`

Depending on your version of Jupyter, you may also have to install the extension with this command:

`
jupyter serverextension enable --py ganymede
`

The file jupyter_notebook_config.py is an example configuration file for starting up Jupyter notebook which activates the extension.
If you already have a configuration file that you are using, append the contents of jupyter_notebook_config.py to your configuration file.
If your configuration file already contains a list for c.NotebookApp.server_extensions, simply add 'ganymede.ganymede' to that list.