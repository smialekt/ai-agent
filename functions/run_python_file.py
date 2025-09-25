import os
import subprocess
from config import PYTHON_RUN_TIMEOUT


def run_python_file(working_directory, filepath, args=[]):
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        file_abs_path = os.path.abspath(os.path.join(working_directory, filepath))

        if not file_abs_path.startswith(working_directory_abs_path):
            return f'Error: Cannot read "{file_abs_path}" as it is outside the permitted working directory'
        if not os.path.exists(file_abs_path):
            return f'Error: File "{file_abs_path}" not found.'
        if not file_abs_path.endswith(".py"):
            return f'Error: "{file_abs_path}" is not a Python file.'

        completed_process = subprocess.run(timeout=PYTHON_RUN_TIMEOUT)

    except Exception as e:
        return f"Error reading file content: {e}"
