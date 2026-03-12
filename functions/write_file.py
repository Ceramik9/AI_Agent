import os

def write_file(working_dir, file_path, content):
    try:
        # Definitions of absolute path and target file 
        absolute_path = os.path.abspath(os.path.join("/home/ceramik/Workspace/AI_Agent/", working_dir))
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
    
        # Invalid directory and invalid file errors
        valid_target_file = os.path.commonpath([absolute_path, target_file]) == absolute_path
        if valid_target_file is not True:
            print(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
            return
        if os.path.isdir(target_file) is True:
            print(f'Error: Cannot write to "{file_path}" as it is a directory')
            return
    
        # Make directory if it doesn't exist in the file_path
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        # Read file in write mode and add content
        with open(target_file, "w") as f:
            f.write(content)
            print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
    except Exception as e:
        print(f"Error: {e}")
    return
