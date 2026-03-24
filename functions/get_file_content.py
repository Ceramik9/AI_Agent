import os
from google.genai import types

# Constants
MAX_CHARS = 10000

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads a specified file relative to the working directory, providing file contents",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read content from, relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_dir, file_path):
    try:
        # Definitions of absolute path and target file
        absolute_path = os.path.abspath(os.path.join("/home/ceramik/Workspace/AI_Agent/", working_dir))
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))

        # Invalid directory and invalid file errors
        valid_target_file = os.path.commonpath([absolute_path, target_file]) == absolute_path
        if valid_target_file is not True:
            return f'Error: Cannot read "{target_file}" as it is outside the permitted working directory'
        if os.path.isfile(target_file) is not True:
            return f'Error: File not found or is not a regular file: "{target_file}"'

        # Read file and save content to string
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            # Add message after reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"

