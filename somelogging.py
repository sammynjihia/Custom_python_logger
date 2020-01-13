 
import logging
import json
from gmailApi import GmailApi 
import datetime
from utility import validateEmail

class JsonFomatter(logging.Formatter):
    def format(self, log_record):

        myjson = {
            "message": log_record.getMessage(),
            "line_number": log_record.lineno,
            "path_name": log_record.pathname,
            "env": log_record.environment
        }

        return json.dumps(myjson)

class MyFilter(logging.Filter):
    def filter(self, log_record):
        log_record.environment = "Local"

        return True

class MyHandler(logging.Handler):
    def loadUserInput(self, user_id, recipient_email):
        self.userId = user_id
        self.recipient_email = recipient_email
    def emit(self, log_record):
        try:
            msg = self.format(log_record)
            
            print("***************")
            print(msg )

            log_event_time = datetime.datetime.now()

            # Send logs via email
            gmailapi = GmailApi()
            
            # Create message
            message_to_send = gmailapi.create_message(self.userId, self.recipient_email, "Log event of {}".format(log_event_time), msg)

            # gmail service instance
            service  = gmailapi.instantiateService()

            # Send logs via email
            gmailapi.send_message(service, self.userId, message_to_send)


            self.flush()
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(log_record)

def logInfo():

    # Get user input
    recipient_email = input("Enter your email address: ")
    user_id = input("Enter user id as shared by you via slack: ")
    log_data = input("Enter data you want to log: ")

    # Validate email
    validateEmail(recipient_email)

    logger = logging.getLogger("my_logger")

    # Create an instance of your custom logger
    myfilter = MyFilter()

    # The addFilter method takes an instance of a Filter class
    logger.addFilter(myfilter)

    print(type(logger))

    # create a handler instance
    # handler = logging.StreamHandler()

    # Create custom handler
    handler = MyHandler()

    # Load user input to the custom handler
    handler.loadUserInput(user_id, recipient_email)

    myfomatter = JsonFomatter()

    # The Handler base class has the setFormatter method where you can add a formatter
    # The setFormatter() method takes an instance of a Fomatter class
    handler.setFormatter(myfomatter)

    # setLevel() is a method of both the Handler and Logger base classes. 
    # It should be noted that 
    handler.setLevel("INFO")

    # The handler base class implements the actual logging via the emit() method
    # The addHandler() method from the base Logger base class is used to add a custom handler
    logger.addHandler(handler)

    # setLevel() method from both the Logger and Handler base classes are used to set the log level
    # of either the logger or the handler
    # You can have many handlers with different loglevels
    logger.setLevel("INFO")

    logger.info(log_data)
    
logInfo()
