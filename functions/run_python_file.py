import os
import subprocess

def run_python_file(working_dir, file_path, args=None):
    try:
        # Definitions of absolute path and target file 
        absolute_path = os.path.abspath(os.path.join("/home/ceramik/Workspace/AI_Agent/", working_dir))
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
    
        # Invalid directory and invalid file errors
        valid_target_file = os.path.commonpath([absolute_path, target_file]) == absolute_path
        if valid_target_file is not True:
            print(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
            return
        if os.path.isfile(target_file) is not True:
            print(f'Error: "{file_path}" does not exist or is not a regular file')
            return
        if file_path[-3:] != ".py":
            print(f'Error: "{file_path}" is not a Python file')
            return

        # Success - run subprocess
        command = ["python", target_file]
        if args != None:
            command.extend(args)
        p1 = subprocess.run(command, cwd=absolute_path, timeout=30, capture_output=True, text=True)
        if p1.returncode != 0:
            print(f"Process exited with code {p1.returncode}")
        if p1.stdout == None and p1.stderr == None:
            print("No output produced")
        else:
            print(f"STDOUT: {p1.stdout}")
            print(f"STDERR: {p1.stderr}")

    except Exception as e:
        print(f"Error: executing Python file: {e}")
    return

