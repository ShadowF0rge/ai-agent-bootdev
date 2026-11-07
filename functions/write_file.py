import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory = os.path.abspath(working_directory)

        if not os.path.isabs(file_path):
            file_path = os.path.join(working_directory, file_path)

        file_path = os.path.abspath(file_path)

        if os.path.commonpath([working_directory, file_path]) != working_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_directory = os.path.dirname(file_path)

        if parent_directory:
            os.makedirs(parent_directory, exist_ok=True)

        with open(file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: Failed to write to "{file_path}". Exception: {str(e)}'