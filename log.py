import logging

class Logger:

   logging.basicConfig(level=logging.INFO)
   log = logging.getLogger(__name__)

   # create a file handler
   handler = logging.FileHandler('.log')
   handler.setLevel(logging.INFO)

   # create a logging format
   formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   handler.setFormatter(formatter)

   # add the handlers to the logger
   log.addHandler(handler)

   def __init__(self):
      None

   def i(self, message):
   	self.log.info(message)

   def e(self, message):
   	self.log.error(message)

   def d(self, message):
   	self.log.debug(message)

