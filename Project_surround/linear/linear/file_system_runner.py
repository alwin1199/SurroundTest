"""
This module is responsible for loading the data and running the pipeline.
"""

import logging
from surround import Runner
from .stages import AssemblerState

logging.basicConfig(level=logging.INFO)

class FileSystemRunner(Runner):

    def load_data(self, mode, config):
        # Load data to be processed
        raw_data = "ckeck"
        return AssemblerState(raw_data)
