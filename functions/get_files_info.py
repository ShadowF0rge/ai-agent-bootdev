import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
           return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        print(f"Result for {target_dir} directory:")
        result = ""

        if not os.path.isdir(target_dir):
            result = f'Error: "{directory}" is not a directory'
            return result

        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            file_size = f"file_size={os.path.getsize(item_path)}"
            if os.path.isdir(item_path):
                is_dir = "is_dir=True"
            else:
                is_dir = "is_dir=False"
            result = f"- {item}: {file_size} bytes, {is_dir}"
            print(result)
        return ""
    except Exception as e:
        return f"Error: {str(e)}"

