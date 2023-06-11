import os
from pathlib import Path

from datetime import datetime


class Logger:
    def __init__(self, log_file: str, service: str):
        assert os.path.exists(os.path.dirname(log_file)), 'the parent directory should exist'
        self.log_file: str = log_file
        self.service: str = service
        self.context: str = 'base'
    
    def set_context(self, context: str, msg: str = None):
        # assert self.context is None, 'cent set context 2 times in a row'
        self.context = context
        if msg is None:
            msg = 'start context'
        self._log('finish context')
    
    def reset_context(self, msg: str = None):
        # assert self.context is not None, 'cent reset context befor it is set'
        if msg is None:
            msg = 'finish context'
        self._log(msg)
        self.context = 'base'

    def log(self, msg: str):
        assert self.context is not None, 'set context first'
        self._log(msg)
    
    def _log(self, msg):
        time_now = datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")
        msg = f'[{time_now}][{self.service}][{self.context}] {msg}'
        with open(self.log_file, 'a') as f:
            f.write(msg+'\n')
