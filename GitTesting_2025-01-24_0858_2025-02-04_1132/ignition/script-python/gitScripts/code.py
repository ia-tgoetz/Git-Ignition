import subprocess
import os
import tempfile
import urllib

logger = system.util.getLogger("GitHub")
def pull_git_repo(repo_url, branch='main', username=None, token=None):
	try:
		# Modify the URL to include credentials if provided
		if username and token:
		    repo_url = repo_url.replace("https://", "https://{}:{}@".format(username, token))
		
		# Create a temporary directory
		temp_dir = tempfile.mkdtemp()
		
		# Define the Git clone command
		git_clone_command = ['git', 'clone', '--branch', branch, repo_url, temp_dir]
		
		# Run the command
		ret_code = subprocess.call(git_clone_command)
		if ret_code != 0:
			logger.warn(Exception("Git clone failed with return code {}".format(ret_code)))
			raise Exception("Git clone failed with return code {}".format(ret_code))
		
		# Log success and return the path
		logger.info("Repository cloned successfully to {}".format(temp_dir))
		return temp_dir
	
	except Exception as ex:
		logger.warn("Error: {}".format(ex))
		return None
		

def set_git_remote(local_path, username, token, remote_url, email='tgoetz@inductiveautomation.com'):
    """
    Sets or updates the Git remote origin URL with authentication.
    
    :param local_path: Path to the local Git repository.
    :param username: GitHub username.
    :param token: Personal access token for authentication.
    :param repo_url: Remote repository URL without credentials.
    """
    try:
        # Ensure the local path exists
        if not os.path.isdir(local_path):
            raise ValueError("The specified path is not a directory: {}".format(local_path))

        # Step 1: Initialize a local Git repository (if not already a Git repo)
        if not os.path.exists(os.path.join(local_path, ".git")):
            subprocess.check_call(["git", "init"], cwd=local_path)
            logger.info("Initialized a new Git repository at '{}'".format(local_path))

        # Configure Git username and email if not already set
        try:
            subprocess.check_call(["git", "config", "--get", "user.name"], cwd=local_path)
        except subprocess.CalledProcessError:
            subprocess.check_call(["git", "config", "user.name", username], cwd=local_path)
            subprocess.check_call(["git", "config", "user.email", email], cwd=local_path)
            logger.info("Configured Git username and email.")

        # Step 4: Set up the remote
        if username and token:
            # Add authentication to the remote URL (e.g., for GitHub)
            username_encoded = urllib.quote(username, safe="")
            token_encoded = urllib.quote(token, safe="")
            remote_url = remote_url.replace("https://", "https://{}:{}@".format(username_encoded, token_encoded), 1)

        # Check if a remote already exists
        existing_remotes = subprocess.check_output(["git", "remote"], cwd=local_path).strip().splitlines()
        if "origin" not in existing_remotes:
            subprocess.check_call(["git", "remote", "add", "origin", remote_url], cwd=local_path)
            logger.info("Added remote repository: {}".format(remote_url))
            return True
        else:
            subprocess.check_call(["git", "remote", "set-url", "origin", remote_url], cwd=local_path)
            logger.info("Updated remote repository URL to: {}".format(remote_url))
            return True

    except subprocess.CalledProcessError as e:
        logger.warn("Failed to set remote URL: {}".format(e))
        return False
    except Exception as e:
    	logger.warn("Error: {}".format(e))
        return False

def create_gitignore_file(repo_path, patterns):
    """
    Creates a .gitignore file in the specified repository path with the given patterns.
    
    :param repo_path: Path to the local Git repository.
    :param patterns: List of patterns to include in the .gitignore file.
    """

    gitignore_path = os.path.join(repo_path, ".gitignore")
    
    try:
        with open(gitignore_path, "w") as gitignore_file:
            for pattern in patterns:
                gitignore_file.write(pattern + "\n")
        logger.info(".gitignore file created successfully at: {}".format(gitignore_path))
    except Exception as e:
        logger.warn("Failed to create .gitignore file: {}".format(e))


def push_to_main(local_repo_path, commit_message):
    try:
    	dateTimeString=system.date.format(system.date.now(),"YYYYMMddHHmmss")
        # Checkout branch
        subprocess.check_call(["git", "-C", local_repo_path, "checkout", "-b", dateTimeString])
        # Stage changes
        subprocess.check_call(["git", "-C", local_repo_path, "add", "."])
        # Commit changes
        subprocess.check_call(["git", "-C", local_repo_path, "commit", "-m", commit_message])
        # Force push to the main branch
        subprocess.check_call(["git", "-C", local_repo_path, "push", "-u", "origin", dateTimeString])
        logger.info("Changes pushed to main successfully!")
    except subprocess.CalledProcessError as e:
        logger.info("Error during Git operation: {}".format(e))
    except Exception as e:
        logger.info("Unexpected error: {}".format(e))













