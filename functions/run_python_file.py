import os
import subprocess
from config import PYTHON_RUN_TIMEOUT
from google.genai import types


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


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs specified file in working directory in a subprocess.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "filepath": types.Schema(
                type=types.Type.STRING,
                description="The path of a file that is supposed to be run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Arguments to run python file with. Is empty array if not provided",
            ),
        },
    ),
)
