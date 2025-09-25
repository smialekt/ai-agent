import os
import subprocess
from config import PYTHON_RUN_TIMEOUT


def run_python_file(working_directory, filepath, args=[]):
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        file_abs_path = os.path.abspath(os.path.join(working_directory, filepath))

        if not file_abs_path.startswith(working_directory_abs_path):
            return f'Error: Cannot execute "{filepath}" as it is outside the permitted working directory'
        if not os.path.exists(file_abs_path):
            return f'Error: File "{filepath}" not found.'
        if not file_abs_path.endswith(".py"):
            return f'Error: "{file_abs_path}" is not a Python file.'

        result = []
        completed_process = subprocess.run(
            ["python3", file_abs_path, *args],
            cwd=working_directory_abs_path,
            timeout=PYTHON_RUN_TIMEOUT,
            capture_output=True,
            text=True,
        )
        completed_process.check_returncode()

        if completed_process.stdout:
            result.append(f"STDOUT:\n{completed_process.stdout}")
        else:
            result.append("No output produced")

        if completed_process.stderr:
            result.append(f"STDERR:\n{completed_process.stderr}")

        if completed_process.returncode != 0:
            result.append(f"Process exited with code {completed_process.returncode}")

        return "\n".join(result)
    except Exception as e:
        return f"Error: executing Python file: {e}"
