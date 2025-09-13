import os
from google.genai import types

def write_file(working_directory, file_path, content):    
    full_path = os.path.join(working_directory, file_path)
    abs_full_path = os.path.abspath(full_path)
    abs_working_path = os.path.abspath(working_directory)
    if not abs_full_path.startswith(abs_working_path + os.sep):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        if not os.path.exists(os.path.dirname(abs_full_path)):
            os.makedirs(os.path.dirname(abs_full_path))
            
        with open(abs_full_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {str(e)}'
        

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes python code in an existing or new file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Contents to be written to the file."
            )
        },
    ),
)