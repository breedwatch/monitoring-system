import logging
import mapping


class ErrorHandler():
    def __init__(self):
        logging.basicConfig(filename=mapping.error_log, level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(name)s %(message)s')
        self.log = logging.getLogger(__name__)
