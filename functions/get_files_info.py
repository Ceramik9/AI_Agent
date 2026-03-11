import os

def get_files_info(working_dir, dir="."):
    try:
        # Definitions of absolute path and normal path
        absolute_path = os.path.abspath(os.path.join("/home/ceramik/Workspace/AI_Agent/", working_dir))
        target_dir = os.path.normpath(os.path.join(absolute_path, dir))
    
        # Errors for invalid directory paths
        valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
        if valid_target_dir is not True:
            print(f'Error: Cannot list "{target_dir}" as it is outside the permitted working directory')
            return
        if os.path.isdir(target_dir) is not True:
            print(f'Error: "{target_dir}" is not a directory')
            return
    
        # Successful return result
        for item in os.listdir(target_dir):
            item_size = os.path.getsize(os.path.join(target_dir, item))
            item_type = os.path.isdir(os.path.join(target_dir, item))
            print(f"- {item}: file_size={item_size} bytes, is_dir={item_type}")
    except Exception as e:
            print(f"Error: {e}")
    return

