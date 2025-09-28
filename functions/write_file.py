import os
from google.genai import types


def write_file(working_directory, filepath, content):
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        file_abs_path = os.path.abspath(os.path.join(working_directory, filepath))

        if not file_abs_path.startswith(working_directory_abs_path):
            return f'Error: Cannot read "{file_abs_path}" as it is outside the permitted working directory'

        with open(file_abs_path, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_abs_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error reading file content: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes given string into specified filepath. If there is no file present at given path, creates it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "filepath": types.Schema(
                type=types.Type.STRING,
                description="The filepath to write content to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that will be written to file",
            ),
        },
    ),
)
