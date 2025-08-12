import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_full_path = os.path.abspath(full_path)
    abs_working_path = os.path.abspath(working_directory)
    
    if not abs_full_path.startswith(abs_working_path + os.sep):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(abs_full_path):
        return f'Error: File "{file_path}" not found.'
    elif not abs_full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        process_args = ["python", f"{file_path}"]
        completed_process = subprocess.run(process_args + args, timeout=30, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=abs_working_path)
        decoded_stdout = completed_process.stdout.decode('utf-8')
        decoded_stderr = completed_process.stderr.decode("utf-8")

        if completed_process.returncode != 0:
            return f'STDOUT: {decoded_stdout} STDERR: {decoded_stderr} Process exited with code {completed_process.returncode}'
        elif not decoded_stdout and not decoded_stderr:
            return "No output produced"
        else:
            return f'STDOUT: {decoded_stdout} STDERR: {decoded_stderr}'

    except Exception as e:
        return f"Error: executing Python file: {e}"
