import os
import shutil
import json 

logger = system.util.getLogger("GitHub")

def getProjectDirectory():
	from com.inductiveautomation.ignition.gateway import IgnitionGateway
	context = IgnitionGateway.get()
	projectParentFolder = '{}/projects'.format(context.systemManager.dataDir.absoluteFile).replace('\\','/')
#	projectParentFolder = '{}'.format(context.systemManager.dataDir.absoluteFile).replace('\\','/')
	return projectParentFolder
	
def copy_item(src, dest):
    """
    Copy a file or folder to the destination. If the destination already contains the file or folder,
    replace it; otherwise, copy it.
    """
    # Ensure the source exists
    if not os.path.exists(src):
        raise ValueError("Source path does not exist: {}".format(src))

    # Determine the destination path for the item
    dest_item_path = os.path.join(dest, os.path.basename(src))

    # If the item exists in the destination, remove it
    if os.path.exists(dest_item_path):
        if os.path.isfile(dest_item_path) or os.path.islink(dest_item_path):
            os.remove(dest_item_path)
        elif os.path.isdir(dest_item_path):
            shutil.rmtree(dest_item_path)

    # Copy the source to the destination
    if os.path.isfile(src) or os.path.islink(src):
        shutil.copy2(src, dest_item_path)  # Copy file or symlink with metadata
    elif os.path.isdir(src):
        shutil.copytree(src, dest_item_path)  # Copy directory recursively
    else:
        raise ValueError("Source is neither a file nor a directory: {}".format(src))

def list_directories(directory):
    """
    List directories in the given directory.
    """
    try:
        return [item for item in os.listdir(directory) if os.path.isdir(os.path.join(directory, item))]
    except OSError as e:
        print("Error listing directories: {}".format(e))
        return []

def save_file_to_directory(token, file_name='gitPAT.json',directory_path="/usr/local/bin/ignition/data/tmp"):
	logger = system.util.getLogger("FileSystemSave")
	data={'token':token}
	try:
	    if not os.path.exists(directory_path):
#	   		create_Base_Folders()
	   		os.mkdir(directory_path)
	except OSError as e:
	    logger.warn("Error Saving to Directory: {}".format(e))
	    return False
	# Specify the file path
	file_path = '{}/{}.json'.format(directory_path,file_name)
	# Write the data to a JSON file
	with open(file_path, 'w') as json_file:
		json.dump(data, json_file)
		logger.trace("{} saved".format(file_name))
		return [True, file_path]
		
def read_file(file_path="/usr/local/bin/ignition/data/tmp/gitPAT.json"):
	"""	Reads and retrieves the contents of a JSON file.
	Args:
	    file_path (str): Path to the JSON file.
	Returns:
	    str: Contents of the JSON file as a string. Returns None on failure.
	"""
	logger = system.util.getLogger("FileSystemOpen")
	try:
		with open(file_path, 'r') as file:
			file_content = file.read()
			data = file_content
			logger.trace('File Read Successfully: "{}"'.format(file_path))
			return data
	except IOError as e:
		logger.warn("Error reading file: {}".format(e))
		return None
	except ValueError as e:
		logger.warn("Error decoding JSON: {}".format(e))
		return None
		
def delete_directory(directory_path):
    logger = system.util.getLogger("FileSystemDeleteDirectory")
    try:
        # Check if the directory exists
        if os.path.exists(directory_path):
            # Remove the directory and all its contents
            shutil.rmtree(directory_path)
            logger.trace("Directory and all its contents deleted successfully: {}".format(directory_path))
        else:
            logger.trace("Directory does not exist: {}".format(directory_path))
    except OSError as e:
        logger.warn("Error deleting directory: {}".format(e))