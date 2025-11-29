from flask import Blueprint, request, jsonify
import subprocess
import os
import shutil

update_bp = Blueprint('update', __name__)

@update_bp.route('/pull', methods=['GET', 'POST'])
def pull_updates():
    """
    Pull updates from GitHub repository and copy files to specified locations.

    This endpoint pulls the latest changes from the GitHub repository and
    copies the updated files to the production locations as specified:
    - Source: /home/GoMangatarem/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan
    - Destination 1: /home/GoMangatarem/mysite (all folder and files)
    - Destination 2: /home/GoMangatarem (all files)

    Expects a JSON payload with:
    {
        "token": "webhook_token" (optional, for security)
    }

    Returns:
        JSON response with the result of the operation.
    """
    try:
        # For security, you might want to verify a token or check request headers
        # This is a basic implementation - add more security as needed
        
        # Define paths
        source_repo = "/home/GoMangatarem/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan"
        dest1 = "/home/GoMangatarem/mysite"
        dest2 = "/home/GoMangatarem"
        
        # Change directory to the source repository
        original_cwd = os.getcwd()
        os.chdir(source_repo)
        
        # Pull the latest changes from GitHub
        result = subprocess.run(['git', 'pull'], 
                                capture_output=True, 
                                text=True)
        
        if result.returncode != 0:
            return jsonify({
                'status': 'error',
                'message': f'Git pull failed: {result.stderr}'
            }), 500
        
        # Copy all files and folders to dest1 by updating existing files
        if not os.path.exists(dest1):
            os.makedirs(dest1)

        # Use rsync-like behavior: copy files and overwrite existing ones
        for root, dirs, files in os.walk(source_repo):
            # Skip .git directory to avoid copying git metadata
            dirs[:] = [d for d in dirs if d != '.git']

            for file in files:
                source_file = os.path.join(root, file)
                rel_path = os.path.relpath(source_file, source_repo)
                dest1_file = os.path.join(dest1, rel_path)

                # Create directory structure if it doesn't exist
                dest1_dir = os.path.dirname(dest1_file)
                if not os.path.exists(dest1_dir):
                    os.makedirs(dest1_dir)

                # Copy file to dest1
                shutil.copy2(source_file, dest1_file)

        # Copy only files (not folders) to dest2
        for item in os.listdir(source_repo):
            source_item = os.path.join(source_repo, item)
            dest2_item = os.path.join(dest2, item)
            if os.path.isfile(source_item):
                shutil.copy2(source_item, dest2_item)
        
        # Return to original directory
        os.chdir(original_cwd)
        
        return jsonify({
            'status': 'success',
            'message': 'Successfully pulled updates and copied files',
            'git_output': result.stdout
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500