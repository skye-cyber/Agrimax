import os

repo_url = "https://github.com/skye-cyber/AgriMax.git"
repo_dir = os.path.basename(repo_url).rsplit('.', 1)[0]
print(repo_dir)
