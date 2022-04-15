from collections import OrderedDict
from logging import LogRecord
from typing import Dict
from colorama import Fore, Back, Style
from pythonjsonlogger.jsonlogger import JsonFormatter, merge_record_extra, \
    RESERVED_ATTRS


LEVEL_COLORS = {
    'WARNING': Back.YELLOW,
    'INFO': Back.BLUE,
    'DEBUG': Back.LIGHTBLACK_EX,
    'CRITICAL': Back.YELLOW,
    'ERROR': Back.RED
}


class ConsoleDebugFormatter(JsonFormatter):
    """A console debug log format that adds color to log messages and serializes
    the log data to json"""

    def __init__(self, *args, **kwargs):
        if 'reserved_attrs' not in kwargs:
            kwargs['reserved_attrs'] = RESERVED_ATTRS + ('correlation_id',)

        super().__init__(*args, **kwargs)

        

    def colorize(self, color, value):
        """Add color to text for the console"""
        return f'{color}{value}{Style.RESET_ALL}'

    def format(self, record: LogRecord) -> str:
        """Formats a log record for console debugging and serializes the log 
        data to json
        
        Args:
            record: The log record to format.

        Returns:
            A log message.
        """
        message_dict = {}
        if isinstance(record.msg, dict):
            message_dict = record.msg
            record.message = None
        else:
            record.message = record.getMessage()
        record.asctime = self.formatTime(record, '%H:%M:%S')

        # Display formatted exception, but allow overriding it in the
        # user-supplied dict.
        if record.exc_info and not message_dict.get('exc_info'):
            message_dict['exc_info'] = self.formatException(record.exc_info)
        if not message_dict.get('exc_info') and record.exc_text:
            message_dict['exc_info'] = record.exc_text
        # Display formatted record of stack frames
        # default format is a string returned from :func:`traceback.print_stack`
        try:
            if record.stack_info and not message_dict.get('stack_info'):
                message_dict['stack_info'] = self.formatStack(record.stack_info)
        except AttributeError:
            # Python2.7 doesn't have stack_info.
            pass

        log_record: Dict
        try:
            log_record = OrderedDict()
        except NameError:
            log_record = {}

        message_dict.update(
            merge_record_extra(record, log_record, reserved=self._skip_fields)
        )
        self.add_fields(log_record, record, message_dict)

        if 'message' in log_record:
            del log_record['message']

        log_record = self.process_log_record(log_record)

        msg = record.message
        if message_dict:
            newline = '\n' if msg else ''
            msg += newline + self.serialize_log_record(log_record)
        
        correlation_id = ''
        if hasattr(record, 'correlation_id'):
            correlation_id = ' - ' + self.colorize(Fore.YELLOW,
                getattr(record, 'correlation_id'))

        return '%(asctime)s %(levelname)s %(name)s %(module)s.%(funcName)s:' \
            '%(lineno)s%(correlation_id)s\n%(message)s' % {
            'asctime': self.colorize(Fore.MAGENTA, record.asctime),
            'levelname': self.colorize(LEVEL_COLORS[record.levelname], 
                record.levelname),
            'name': self.colorize(Fore.CYAN, record.name),
            'module': self.colorize(Fore.YELLOW, record.module),
            'funcName': self.colorize(Fore.BLUE, record.funcName),
            'lineno': self.colorize(Fore.GREEN, record.levelno),
            'correlation_id': correlation_id,
            'message': msg,
        }

