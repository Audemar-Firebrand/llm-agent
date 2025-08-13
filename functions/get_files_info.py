import os
from google.genai import types

def get_files_info(
    working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_full_path = os.path.abspath(full_path)
    abs_working_path = os.path.abspath(working_directory)
    if not abs_full_path.startswith(abs_working_path + os.sep):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(abs_full_path):
        return f'Error: "{directory}" is not a directory'
    else:
        try:
            contents = [] 
            dir_list = os.listdir(abs_full_path)

            for item in dir_list:
                file_size = os.path.getsize(os.path.join(abs_full_path, item))
                is_dir = os.path.isdir(os.path.join(abs_full_path, item))
                file_string = f"- {item}: file_size={file_size}, is_dir={is_dir}"
                contents.append(file_string)
            return "\n".join(contents)
        except Exception as e:
            return f"Error: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
