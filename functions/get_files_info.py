import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_dir, dir="."):
    try:
        # Definitions of absolute path and normal path
        absolute_path = os.path.abspath(os.path.join("/home/ceramik/Workspace/AI_Agent/", working_dir))
        target_dir = os.path.normpath(os.path.join(absolute_path, dir))
    
        # Errors for invalid directory paths
        valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
        if valid_target_dir is not True:
            return f'Error: Cannot list "{target_dir}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir) is not True:
            return f'Error: "{target_dir}" is not a directory'
    
        # Successful return result
        for item in os.listdir(target_dir):
            item_size = os.path.getsize(os.path.join(target_dir, item))
            item_type = os.path.isdir(os.path.join(target_dir, item))
            return f"- {item}: file_size={item_size} bytes, is_dir={item_type}"
    except Exception as e:
            return f"Error: {e}"
    return

