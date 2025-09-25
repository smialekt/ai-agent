import os


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
