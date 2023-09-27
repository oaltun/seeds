from datetime import datetime
from pathlib import Path
import subprocess
import os
import shutil

from subprocess import run, CalledProcessError

def podman_cleanup():
    # Define the commands to clean up Podman
    commands = [
        "podman stop $(podman ps -aq)",  # Stop all running containers
        "podman rm $(podman ps -aq)",   # Remove all containers
        "podman volume rm $(podman volume ls -q)",  # Remove all volumes
        "podman pod rm $(podman pod ls -q)"  # Remove all pods
    ]

    # Run the commands
    for command in commands:
        try:
            run(command, shell=True, check=True)
            print(f"podman_cleanup: Successfully executed: {command}")
        except CalledProcessError as e:
            print(f"podman_cleanup: An error occurred while executing: {command}\nError: {e}")

    print("podman_cleanup: Podman clean-up completed.")

def main():

    podman_cleanup()

    print("podman_run: Generate the directory name and store it in a variable.",end=" ")
    current_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    dirname = Path(f"../runs/run_{current_time}")
    print(f"Done. Dirname: {dirname}.")

    print("podman_run: Use the variable to create the directory.",end=" ")
    dirname.mkdir(parents=True, exist_ok=True)
    print("Done.")

    print("podman_run: Copy initial_software to new locations.", end=" ")
    shutil.copytree("initial_software", dirname / "software1")
    shutil.copytree("initial_software", dirname / "software2")
    print("Done.")

    print("podman_run: Copy name.md files.", end=" ")
    shutil.copy("name1.md", dirname / "software1/name.md")
    shutil.copy("name2.md", dirname / "software2/name.md")
    print("Done.")


    print("podman_run: Copy specific_goal.md files", end=" ")
    shutil.copy("specific_goal_1.md", dirname / "software1/specific_goal.md")
    shutil.copy("specific_goal_2.md", dirname / "software2/specific_goal.md")

    print("podman_run: Run the podman command.", end=" ")
    software1_path = dirname / "software1"
    software2_path = dirname / "software2"
    print("Done.")

    openai_api_key = os.getenv("OPENAI_API_KEY")
    cmd = [
        "podman", "run",
        "-e", f"OPENAI_API_KEY={openai_api_key}",
        "-v", f"{software1_path}:/app/env1/software",
        "-v", f"{software2_path}:/app/env2/software",
        "-w", "/app",
        "evolver:latest", "python3", "-u","loop.py"
    ]
    print(f"Running {cmd}.")

    subprocess.run(cmd)


main()