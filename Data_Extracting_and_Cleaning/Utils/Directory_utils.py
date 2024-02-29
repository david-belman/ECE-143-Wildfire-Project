import os


def Get_Parent_Directory():
    parent_directory = os.path.abspath('..')
    return parent_directory

def Get_current_directory():
    current_directory = os.getcwd()
    return current_directory

def To_directory(directory_path_from_main=None):
    assert directory_path_from_main is not None, "No directory path was inputted."
    assert isinstance(directory_path_from_main, str), "directory_path_from_main must be of type str."
    parent_dir = Get_Parent_Directory()
    os.chdir(parent_dir)
    directory = os.path.join(Get_current_directory(), directory_path_from_main)

    try:
        os.chdir(directory)
    except FileNotFoundError as e:
        print(f"Error: {e}")

# Used for troubleshooting directory movements
def Get_available_directory_files():
    current_directory = Get_current_directory(False)
    files_and_directories = os.listdir(current_directory)
    print("\tcurrent available files:", files_and_directories)
    return files_and_directories
