#!/usr/bin/env python3
import os
from pathlib import Path
import subprocess
from time import sleep
import itertools

class Runner:
    cwd = '.'
    capture_output=True
    text=True
    check=True
    result: subprocess.CompletedProcess[str] = None
    cmd = None
    name = ""

    def run(self):
        try:
            self.result = subprocess.run(
                self.cmd,
                capture_output=self.capture_output,
                text=self.text,
                check=self.check,
                cwd=self.cwd,
            )
            print(f"Loopy: {self.name} completed successfully. Command was: {self.cmd}.")
            Path(f"{self.cwd}/stdout.txt").write_text(self.result.stdout)
            return self.result

        except subprocess.CalledProcessError as e:
            print("Loopy: === Report Start ===")
            print(f"Loopy: {self.name} failed with error: {e}.")
            print("Loopy: === Output ===")
            print(e.stdout)
            print("Loopy: === Errors ===")
            print(e.stderr)
            print("Loopy: === Report End ===")
            raise  # or you could use 'raise e'
        
def main():
    cyclic_iterator = itertools.cycle(["/app/env1","/app/env2"])
    while True:
        sleep(1)
        env_dir = next(cyclic_iterator)
        


        
        pip_installer = Runner()
        pip_installer.cmd = [f"{env_dir}/venv/bin/pip3", "install","-r", f"{env_dir}/software/requirements.txt"]
        pip_installer.name = "pip_installer"
        pip_installer.run() 
        sleep(1)



        twin_runner = Runner()
        twin_runner.cmd = [f"{env_dir}/venv/bin/python3", f"{env_dir}/software/main.py"]
        twin_runner.cwd = f"{env_dir}/software"
        twin_runner.name = "twin_runner"
        twin_runner.run()
                


main()