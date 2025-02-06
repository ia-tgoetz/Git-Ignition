import os
import subprocess

#def create_remote_repo(local_path, repo_url, repo_name, username, token, commit_message="Initial commit"):
#    try:
#        # Step 1: Create the local directory if it doesn't exist
#        if not os.path.exists(local_path):
#            os.makedirs(local_path)
#
#        # Step 2: Initialize the Git repository
#        subprocess.check_call(["git", "init"], cwd=local_path)
#
#        # Step 3: Add all files to the repository
#        subprocess.check_call(["git", "add", "."], cwd=local_path)
#        logger.info("Added files to the repository.")
#
#        # Step 4: Commit the README file
#        subprocess.check_call(["git", "commit", "-m", commit_message], cwd=local_path)
#
#        # Step 5: Set up the remote repository URL with authentication
#        authenticated_repo_url = "https://{}:{}@{}".format(username, token, repo_url.replace("https://", ""))
#        subprocess.check_call(["git", "remote", "add", "origin", authenticated_repo_url], cwd=local_path)
#
#        # Step 7: Push the initial commit to the remote repository
#        subprocess.check_call(["git", "branch", "-M", "main"], cwd=local_path)
#        subprocess.check_call(["git", "push", "-u", "origin", "main"], cwd=local_path)
#
#        logger.info("Repository '{}' created and pushed to '{}' successfully.".format(repo_name, repo_url))
#    except subprocess.CalledProcessError as e:
#        logger.warn("Error occurred during Git operations: {}".format(e))
#    except Exception as ex:
#        logger.warn("Unexpected error: {}".format(ex))
#
#
#
#
#


#def create_remote_repo(local_path, remote_url, username=None, token=None):
#    """
#    Create a remote Git repository from a local folder.
#    
#    :param local_path: Path to the local folder to initialize as a repo
#    :param remote_url: The URL of the remote repository (to push to)
#    :param username: Username for remote Git server (optional)
#    :param token: Personal access token for remote Git server (optional)
#    """
#    try:
#		# Ensure the local path exists
#		if not os.path.isdir(local_path):
#			raise ValueError("The specified path is not a directory: {}".format(local_path))
#		
#		# Step 1: Initialize a local Git repository (if not already a Git repo)
#		if not os.path.exists(os.path.join(local_path, ".git")):
#			subprocess.check_call(["git", "init"], cwd=local_path)
#			logger.info("Initialized a new Git repository at '{}'".format(local_path))
#		
#		# Step 2: Add all files to the repository
#		subprocess.check_call(["git", "add", "."], cwd=local_path)
#		
#		# Step 3: Commit the files
#		subprocess.check_call(["git", "commit", "-m", "Initial commit"], cwd=local_path)
#		
#		# Step 4: Set up the remote
#		if username and token:
#			# Add authentication to the remote URL (e.g., for GitHub)
#			remote_url = remote_url.replace("https://", "https://{}:{}@".format(username_encoded, token_encoded))
#		subprocess.check_call(["git", "remote", "add", "origin", remote_url], cwd=local_path)
#		
#		# Step 5: Push to the remote repository
#		subprocess.check_call(["git", "push", "-u", "origin", "main"], cwd=local_path)
#		logger.info("Pushed local repository to remote: {}".format(remote_url))
#    
#    except subprocess.CalledProcessError as e:
#		logger.info("Git command failed: {}".format(e))
#    except Exception as e:
#		logger.info("Error: {}".format(e))