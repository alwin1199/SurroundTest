"""
This module defines the baseline estimator in the pipeline.
"""

import logging
from surround import Estimator

LOGGER = logging.getLogger(__name__)

class Baseline(Estimator):
    def estimate(self, state, config):
        state.output_data = state.input_data.upper()    #uppercase convertion

        # Print the output to the terminal (to check its working)
        LOGGER.info("Output: %s" % state.output_data)

    def fit(self, state, config):
        LOGGER.info("TODO: Train your model here")
