import os
MAX_CHARS = 10000 #I should move this value to config file

def get_file_content(working_dir, file_path):
    try:
        # Definitions of absolute path and target file
        absolute_path = os.path.abspath(os.path.join("/home/ceramik/Workspace/AI_Agent/", working_dir))
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))

        # Invalid directory and invalid file errors
        valid_target_file = os.path.commonpath([absolute_path, target_file]) == absolute_path
        if valid_target_file is not True:
            print(f'Error: Cannot read "{target_file}" as it is outside the permitted working directory')
            return
        if os.path.isfile(target_file) is not True:
            print(f'Error: File not found or is not a regular file: "{target_file}"')
            return

        # Read file and save content to string
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        print(file_content_string)
    except Exception as e:
        print(f"Error: {e}")
    return
