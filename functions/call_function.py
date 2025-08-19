from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"
    
    if function_call_part.name == "get_files_info":
        if "directory" not in args:
            args["directory"] = "."
    elif function_call_part.name in {"get_file_content", "write_file", "run_python_file"}:
        if "file_path" not in args:
            args["file_path"] = "./calculator"

    func_dict = {
        "get_file_content": get_file_content, 
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
        }
     
    if function_call_part.name not in func_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
        )
    ],
)
    else:
        result = func_dict[function_call_part.name](**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result}
                )
            ]
        )