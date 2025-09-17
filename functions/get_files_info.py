import os


def get_files_info(working_directory, directory="."):
    working_directory_abs_path = os.path.abspath(working_directory)

    directory = os.path.join(working_directory, directory)
    directory_abs_path = os.path.abspath(directory)

    directory_string = "current" if directory == "." else directory
    result = f"Result for '{directory_string}' directory:"

    if not directory_abs_path.startswith(working_directory_abs_path):
        result += f"\nError: Cannot list '{directory}' as it is outside the permitted working directory"
        return result

    if not os.path.isdir(directory_abs_path):
        result += f"\nError: '{directory}' is not a directory"
        return result

    def __process_dir_element(dir_element):
        return f"- {dir_element}: file_size:{os.path.getsize(dir_element)} bytes, is_dir={os.path.isfile(dir_element)}"

    dir_elements = os.listdir(directory_abs_path)
    for dir_element in dir_elements:
        result += "\n" + __process_dir_element(dir_element)

    return result
