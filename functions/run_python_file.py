import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python script file",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python file path, relative to the working directory"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Function arguments",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="An individual argument"
                )

            ),
        },
    ),
)

def run_python_file(working_dir, file_path, args=None):
    try:
        # Definitions of absolute path and target file 
        absolute_path = os.path.abspath(os.path.join("/home/ceramik/Workspace/AI_Agent/", working_dir))
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
    
        # Invalid directory and invalid file errors
        valid_target_file = os.path.commonpath([absolute_path, target_file]) == absolute_path
        if valid_target_file is not True:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_file) is not True:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        # Success - run subprocess
        command = ["python", target_file]
        if args != None:
            command.extend(args)
        p1 = subprocess.run(command, cwd=absolute_path, timeout=30, capture_output=True, text=True)
        output = []
        if p1.returncode != 0:
            return f"Process exited with code {p1.returncode}"
        if not p1.stdout and not p1.stderr:
            output.append("No output produced")
        if p1.stdout:
            output.append(f"STDOUT:\n{p1.stdout}")
        if p1.stderr:
            output.append(f"STDERR:\n{p1.stderr}")
        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"

