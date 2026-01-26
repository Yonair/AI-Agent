import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory.')
    if not os.path.isdir(target_dir):
        return (f'Error: "{directory}" is not a directory')

    

    try:
        target_file = []
        for items in os.listdir(target_dir):
            item_path = os.path.join(target_dir, items)
            is_dir = os.path.isdir(item_path)
            file_name = os.path.basename(item_path)
            file_size = os.path.getsize(item_path)
            target_file.append(f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}")
                
        return "\n".join(target_file)

    except Exception as e:
        return (f"Error: {e}")
