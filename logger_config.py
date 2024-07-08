import logging
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def process_log_record(self, log_record):
        log_record['timestamp'] = log_record.pop('asctime')
        log_record['request'] = f"{log_record['levelname']} - {log_record.pop('message')}"
        log_record['status'] = log_record.pop('status', 'Unknown')

        return super(CustomJsonFormatter, self).process_log_record(log_record)
    
    
def configure_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  

    file_handler = logging.FileHandler("app.log")
    stream_handler = logging.StreamHandler()

    json_formatter = CustomJsonFormatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(json_formatter)
    stream_handler.setFormatter(json_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger