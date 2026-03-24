import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Opens a file in write mode and adds content text to the file_path",
    parameters=types.Schema(
        required=["file_path", "content"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write"
            ),
        },
    ),
)

def write_file(working_dir, file_path, content):
    try:
        # Definitions of absolute path and target file 
        absolute_path = os.path.abspath(os.path.join("/home/ceramik/Workspace/AI_Agent/", working_dir))
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
    
        # Invalid directory and invalid file errors
        valid_target_file = os.path.commonpath([absolute_path, target_file]) == absolute_path
        if valid_target_file is not True:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file) is True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'
    
        # Make directory if it doesn't exist in the file_path
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        # Open file in write mode and add content
        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

