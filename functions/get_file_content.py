import os
from config import MAX_FILE_READ_CHARS
from google.genai import types


def get_file_content(working_directory, filepath):
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        file_abs_path = os.path.abspath(os.path.join(working_directory, filepath))

        if not file_abs_path.startswith(working_directory_abs_path):
            return f'Error: Cannot read "{file_abs_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_abs_path):
            return f'Error: File not found or is not a regular file: "{file_abs_path}"'

        file_content_string = ""
        with open(file_abs_path, "r") as file:
            file_content_string = file.read(MAX_FILE_READ_CHARS + 1)
        if len(file_content_string) > MAX_FILE_READ_CHARS:
            file_content_string = (
                file_content_string[:MAX_FILE_READ_CHARS]
                + f'[...File "{file_abs_path}" truncated at 10000 characters]'
            )

        return file_content_string
    except Exception as e:
        return f"Error reading file content: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns file content as a string. If file's content was larger than specified in the config, truncates it. (Adequate message provided at the end of returned string)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "filepath": types.Schema(
                type=types.Type.STRING,
                description="The file to read content from, relative to the working directory.",
            ),
        },
    ),
)
