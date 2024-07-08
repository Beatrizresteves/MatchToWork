import logging
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def process_log_record(self, log_record):
        log_record['timestamp'] = log_record.get('asctime')
        log_record['agent'] = log_record.pop('agent', 'Unknown')
        log_record['client'] = log_record.pop('client', 'Unknown')
        log_record['compression'] = log_record.pop('compression', 'Unknown')
        log_record['referer'] = log_record.pop('referer', 'Unknown')
        log_record['request'] = log_record.pop('message')
        log_record['size'] = log_record.pop('size', 'Unknown')
        log_record['status'] = log_record.pop('status', 'Unknown')
        log_record['user'] = log_record.pop('user', 'Unknown')
        return super(CustomJsonFormatter, self).process_log_record(log_record)

def configure_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = logging.FileHandler("app.log")
    stream_handler = logging.StreamHandler()

    # Create formatter and add it to handlers
    json_formatter = CustomJsonFormatter()
    file_handler.setFormatter(json_formatter)
    stream_handler.setFormatter(json_formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
