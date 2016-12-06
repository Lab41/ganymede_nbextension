from notebook.services.kernels.handlers import ZMQChannelsHandler
import json
import logging
import sys

class GanymedeHandler(ZMQChannelsHandler):
    handlers = [logging.StreamHandler(stream=sys.stdout),]
    include_filepath = False

    def initialize(self, g_loggr=None):
        super(GanymedeHandler, self).initialize()
        self.g_loggr = g_loggr
        self.log.info("Loading Ganymede logging extension.")
        for handler in self.handlers:
            self.log.info("Adding handler: %s" % handler)
            self.g_loggr.addHandler(handler)

    def log_msg(self, msg):
        json_msg = json.loads(msg)
        msg_type = json_msg['msg_type']
        if self.include_filepath:
            json_msg["filepath"] = self.get_notebook_filepath()
        if msg_type in ["execute_input", "execute_result", "stream", "error"]:
            self.g_loggr.info("%s" % json.dumps(json_msg))

    def get_notebook_filepath(self):
        # List the sessions and return the notebook path from the one matching the current kernel_id.
        sessions = self.session_manager.list_sessions()
        for session in sessions:
            if session["kernel"]["id"] == self.kernel_id:
                return session["notebook"]["path"]
        raise Exception("Kernel ID not found in active session list.")

    """
    Log a message sent from the Jupyter client. This function, on_message, only triggers on one direction of communication (i.e. sending), while _on_zmq_reply triggers on both sending+receiving. We don't want to trigger on sending twice, which is why we are only relying on _on_zmq_reply.
    """
    """
    # def on_message(self, msg):
    #    #self.logger.info("Sending message: %s" % msg)
    #    super(GanymedeHandler, self).on_message(msg)
    """

    """
    # Log a message sent from the kernel. This triggers on both sending+receiving messages.
    # NOTE: This is an exact copy of _on_zmq_reply from ZMQStreamHandler in base/zmqhandlers.py in v4.1.0 of notebook.
    #   This code is brittle and should be updated if the superclass _on_zmq_reply changes.
    #   Ideally, we would log either immediately before or after calling the superclass method directly.
    #   However, _on_zmq_reply doesn't provide any hooks at the actual message, we are forced to reproduce the entire source code.
    """
    def _on_zmq_reply(self, stream, msg_list):
        if self.stream.closed() or stream.closed():
            self.log.warn("zmq message arrived on closed channel")
            self.close()
            return
        channel = getattr(stream, 'channel', None)
        try:
            msg = self._reserialize_reply(msg_list, channel=channel)
        except Exception:
            self.log.critical("Malformed message: %r" % msg_list, exc_info=True)
        else:
            self.write_message(msg, binary=isinstance(msg, bytes))
        # Call Ganymede custom logging function.
        self.log_msg(msg)

def load_jupyter_server_extension(nb_server_app):
    web_app = nb_server_app.web_app
    base_url = web_app.settings['base_url']

    # Construct a mapping of all URL patterns -> URLSpecs
    handlers = {}
    for handler in web_app.handlers:
        urlspecs = handler[1]
        for urlspec in urlspecs:
            handlers[str(urlspec.regex.pattern)] = urlspec

    # Create a separate logger for Ganymede at INFO level.
    g_loggr = logging.getLogger('ganymede-logger')
    g_loggr.setLevel(logging.INFO)

    # Inject GanymedeRequestHandler into the /api/kernels/<kernel_id>/channels URLSpec mapping
    api_kernel_channels_pattern = "%s/api/kernels/(?P<kernel_id>\w+-\w+-\w+-\w+-\w+)/channels$" % base_url.rstrip("/")
    channelspec = handlers[api_kernel_channels_pattern]
    channelspec.kwargs = {'g_loggr': g_loggr,}
    channelspec.handler_class = GanymedeHandler

