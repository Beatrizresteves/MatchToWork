import logging
from flask import request
import json

class CustomJSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'client': request.headers.get('client', 'Unknown'),
            'agent': request.headers.get('agent', 'Unknown'),
            'referer': request.headers.get('referer', 'Unknown'),
            'compression': request.headers.get('compression', 'Unknown'),
            'status': request.headers.get('status', 'Unknown'),
            'user': request.headers.get('user', 'Unknown'),
            'taskName': record.task_name if hasattr(record, 'task_name') else None
        }
        return json.dumps(log_record)

def configure_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    json_formatter = CustomJSONFormatter()

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(json_formatter)
    logger.addHandler(stream_handler)

    return logger
