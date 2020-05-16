"""
This module defines the input validator which is executed
before all other stages in the pipeline and checks whether
the data contained in the State object is valid.
"""

from surround import Validator

class InputValidator(Validator):
    def validate(self, state, config):
        if not isinstance(state.input_data, str):       #Check if input is string
            raise ValueError('Input is not a string!')
