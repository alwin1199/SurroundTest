"""
This module defines the tasks that can be executed using `surround run [task name]`
"""

import os
import sys
import subprocess
import re
import webbrowser
import logging

from pathlib import Path

from surround import Config
from surround.util import generate_docker_volume_path
from surround.experiment.util import get_surround_config

CONFIG = Config(os.path.dirname(__file__))

DOIT_CONFIG = {'verbosity':2}
PACKAGE_PATH = os.path.basename(CONFIG["package_path"])
IMAGE = "%s/%s:%s" % (CONFIG["company"], CONFIG["image"], CONFIG["version"])
LOGGER = logging.getLogger(__name__)

PARAMS = [
    {
        'name': 'args',
        'long': 'args',
        'type': str,
        'default': ""
    }
]

def task_status():
    """Show information about the project such as available runners and assemblers"""
    return {
        'actions': ["%s -m %s --status" % (sys.executable, PACKAGE_PATH)]
    }

def task_build():
    """Build the Docker image for the current project"""
    return {
        'actions': ['docker build --tag=%s .' % IMAGE],
        'params': PARAMS
    }

def task_remove():
    """Remove the Docker image for the current project"""
    return {
        'actions': ['docker rmi %s -f' % IMAGE],
        'params': PARAMS
    }

def task_dev():
    """Run the main task for the project"""
    cmd = [
        "docker",
        "run",
        "--volume",
        "\"%s/\":/app" % CONFIG["volume_path"],
        "%s" % IMAGE,
        "python3 -m %s %s" % (PACKAGE_PATH, "%(args)s")
    ]
    return {
        'actions': [" ".join(cmd)],
        'params': PARAMS
    }

def task_interactive():
    """Run the Docker container in interactive mode"""
    def run():
        cmd = [
            'docker',
            'run',
            '-it',
            '--rm',
            '-w',
            '/app',
            '--volume',
            '%s/:/app' % CONFIG['volume_path'],
            IMAGE,
            'bash'
        ]
        process = subprocess.Popen(cmd, encoding='utf-8')
        process.wait()

    return {
        'actions': [run]
    }

def task_prod():
    """Run the main task inside a Docker container for use in production """
    return {
        'actions': ["docker run %s python3 -m %s %s" % (IMAGE, PACKAGE_PATH, "%(args)s")],
        'task_dep': ["build"],
        'params': PARAMS
    }

def task_train():
    """Run training mode inside the container"""
    output_path = CONFIG["volume_path"] + "/output"
    data_path = CONFIG["volume_path"] + "/input"

    global_config = get_surround_config()

    # Inject user's name and email into the env variables of the container
    user_name = global_config.get_path("user.name")
    user_email = global_config.get_path("user.email")
    experiment_args = "-e \"SURROUND_USER_NAME=%s\" " % user_name
    experiment_args += "-e \"SURROUND_USER_EMAIL=%s\"" % user_email

    experiment_path = os.path.join(str(Path.home()), ".experiments")
    experiment_volume_path = generate_docker_volume_path(experiment_path)

    # Ensure experiments will work if using a local storage location (not in the cloud)
    if os.path.join(experiment_path, "local") == global_config.get_path("experiment.url"):
        experiment_args += " --volume \"%s\":/experiments " % experiment_volume_path
        experiment_args += "-e \"SURROUND_EXPERIMENT_URL=/experiments/local\""
    else:
        current_url = global_config.get_path("experiment.url")
        experiment_args += " -e \"SURROUND_EXPERIMENT_URL=%s\"" % current_url

    cmd = [
        "docker run %s" % experiment_args,
        "--volume \"%s\":/app/output" % output_path,
        "--volume \"%s\":/app/input" % data_path,
        IMAGE,
        "python3 -m linear --mode train --experiment %(args)s"
    ]

    return {
        'actions': [" ".join(cmd)],
        'params': PARAMS
    }

def task_batch():
    """Run batch mode inside the container"""
    output_path = CONFIG["volume_path"] + "/output"
    data_path = CONFIG["volume_path"] + "/input"

    global_config = get_surround_config()

    # Inject user's name and email into the env variables of the container
    user_name = global_config.get_path("user.name")
    user_email = global_config.get_path("user.email")
    experiment_args = "-e \"SURROUND_USER_NAME=%s\" " % user_name
    experiment_args += "-e \"SURROUND_USER_EMAIL=%s\"" % user_email

    experiment_path = os.path.join(str(Path.home()), ".experiments")
    experiment_volume_path = generate_docker_volume_path(experiment_path)

    # Ensure experiments will work if using a local storage location (not in the cloud)
    if os.path.join(experiment_path, "local") == global_config.get_path("experiment.url"):
        experiment_args += " --volume \"%s\":/experiments " % experiment_volume_path
        experiment_args += "-e \"SURROUND_EXPERIMENT_URL=/experiments/local\""
    else:
        current_url = global_config.get_path("experiment.url")
        experiment_args += " -e \"SURROUND_EXPERIMENT_URL=%s\"" % current_url

    cmd = [
        "docker run %s" % experiment_args,
        "--volume \"%s\":/app/output" % output_path,
        "--volume \"%s\":/app/input" % data_path,
        IMAGE,
        "python3 -m linear --mode batch %(args)s"
    ]

    return {
        'actions': [" ".join(cmd)],
        'params': PARAMS
    }

def task_train_local():
    """Run training mode locally"""
    cmd = [
        sys.executable,
        "-m %s" % PACKAGE_PATH,
        "--mode train",
        "%(args)s"
    ]

    return {
        'basename': 'trainLocal',
        'actions': [" ".join(cmd)],
        'params': PARAMS
    }

def task_batch_local():
    """Run batch mode locally"""
    cmd = [
        sys.executable,
        "-m %s" % PACKAGE_PATH,
        "--mode batch",
        "%(args)s"
    ]

    return {
        'basename': 'batchLocal',
        'actions': [" ".join(cmd)],
        'params': PARAMS
    }

def task_jupyter():
    # Allow for auto reload to be enabled and import modules from project package
    ipython_config = "c.InteractiveShellApp.extensions.append('autoreload')\n"
    ipython_config += "c.InteractiveShellApp.exec_lines = "
    ipython_config += "['%autoreload 2', 'import sys', 'sys.path.append(\\'../\\')']"

    # Build the command for running jupyter
    command = [
        "pip install -r /app/requirements.txt",
        "mkdir /etc/ipython",
        "echo \"%s\" > /etc/ipython/ipython_config.py" % ipython_config,
        "/usr/local/bin/start.sh jupyter notebook --NotebookApp.token=''"
    ]
    command = "; ".join(command)

    def run_command():
        process = subprocess.Popen(
            [
                "docker",
                "run",
                "--rm",
                "--name",
                "linear_surround_notebook",
                "--volume",
                "%s:/app" % CONFIG['volume_path'],
                "-p",
                "55910:8888",
                "--user",
                "root",
                "-w",
                "/app",
                "jupyter/base-notebook:307ad2bb5fce",
                "bash",
                "-c",
                command
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8')

        LOGGER.info("Starting jupyter notbook server...\n")

        # Get the IP address of the container, otherwise use localhost
        ip_process = subprocess.Popen(
            ['docker-machine', 'ip'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8')
        ip_process.wait()

        ip_output = ip_process.stdout.readline().rstrip()

        if re.match(r"^(\d{1,3}\.){3}\d{1,3}$", ip_output):
            host = ip_output
        else:
            host = "localhost"

        # Wait for the notebook server to be up before loading browser
        while True:
            line = process.stderr.readline().rstrip()
            if line and 'Serving notebooks from local directory' in line:
                break

            if process.poll():
                LOGGER.error("Failed to start the server, check if its not running somewhere else!")

                # Stop any containers that might be running
                process = subprocess.Popen(
                    [
                        'docker',
                        'stop',
                        'linear_surround_notebook'
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
                process.wait()
                return

        # Open the browser automatically
        webbrowser.open('http://%s:55910/tree' % host, new=2)

        LOGGER.info("Notebook URL: http://%s:55910/tree\n", host)
        LOGGER.info("Use CTRL+C to stop the server.")

        try:
            process.wait()
        except KeyboardInterrupt:
            pass
        finally:
            LOGGER.info("Closing server...")
            process = subprocess.Popen(
                [
                    'docker',
                    'stop',
                    'linear_surround_notebook'
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            process.wait()

    return {
        'actions': [run_command]
    }
