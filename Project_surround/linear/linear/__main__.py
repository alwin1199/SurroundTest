"""
Main entry-point for the Surround project.
Runners and assemblies are defined in here.
"""

import os
import argparse
from surround import Surround, Assembler, has_config
from .stages import Baseline, InputValidator, ReportGenerator
from .file_system_runner import FileSystemRunner

RUNNERS = [
    FileSystemRunner()
]

ASSEMBLIES = [
    Assembler("baseline")
        .set_validator(InputValidator())
        .set_estimator(Baseline())
        .set_visualiser(ReportGenerator())
]

@has_config
def main(config=None):
    default_runner = config.get_path('runner.default')
    default_assembler = config.get_path('assembler.default')

    parser = argparse.ArgumentParser(
        prog='linear',
        description="Surround mode(s) available to run this module")

    parser.add_argument(
        '-r',
        '--runner',
        help="Runner for the Assembler (index or name)",
        default=default_runner if default_runner is not None else "0")
    parser.add_argument(
        '-a',
        '--assembler',
        help="Assembler to run (index or name)",
        default=default_assembler if default_assembler is not None else "0")
    parser.add_argument(
        '-ne',
        '--no-experiment',
        dest='experiment',
        help="Don't consider this run an experiment",
        action="store_false")
    parser.add_argument(
        '--status',
        help="Display information about the project such as available RUNNERS and assemblers",
        action="store_true")
    parser.add_argument('-n', '--note', help="Add a note to the experiment", type=str)
    parser.add_argument('--mode', help="Mode to run (train, batch)", default="batch")

    args = parser.parse_args()

    surround = Surround(
        RUNNERS,
        ASSEMBLIES,
        "linear",
        "linear eqaution",
        os.path.dirname(os.path.dirname(__file__))
    )

    if args.status:
        surround.show_info()
    else:
        surround.run(args.runner, args.assembler, args.mode, args.experiment, args)

if __name__ == "__main__":
    main()
