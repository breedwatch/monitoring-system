import logging


class ErrorHandler():
    def __init__(self):
        logging.basicConfig(filename='error.log', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(name)s %(message)s')
        self.log = logging.getLogger(__name__)
