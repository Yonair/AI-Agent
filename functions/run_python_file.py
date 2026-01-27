import os
import subprocess
  

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs

    try:
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]
        if args:
            command.extend(args)

        CompletedProcess = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=working_dir_abs)

        output = []

        if CompletedProcess.returncode != 0:
            output.append("Process exited with code X")

        if CompletedProcess.stdout and CompletedProcess.stderr == "":
            output.append("No output produced")

        if CompletedProcess.stdout:
            output.append(f"STDOUT:\n{CompletedProcess.stdout}")

        if CompletedProcess.stderr:
            output.append(f"STDERR:\n{CompletedProcess.stderr}")

        return "\n".join(output)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"