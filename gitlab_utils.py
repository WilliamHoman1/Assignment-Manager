import gitlab
import os


# Messing around with gitlab integration , still in progress
def get_gitlab_client():
    token = os.getenv("GITLAB_TOKEN")
    return gitlab.Gitlab("https://gitlab.com", private_token=token)

def list_problem_folders(project_path, repo_path='problems', ref='main'):
    """
    Returns folder entries under repo_path.
    Each entry contains:
    - name
    - path
    - type ('tree' for folder)
    """
    gl = get_gitlab_client()
    project = gl.projects.get(project_path)

    tree = project.repository_tree(path=repo_path, ref=ref)
    return tree