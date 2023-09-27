#!/usr/bin/env python3
import os
from pathlib import Path
import subprocess
from time import sleep
import itertools

import subprocess
from pathlib import Path


import subprocess
import sys
import threading

def stream_output(pipe, log_file, console):
    for line in iter(pipe.readline, b''):
        console.buffer.write(line)
        log_file.write(line)

def run_command_and_log_output(cmd, cwd, log_file_path):
    # Open the log file
    with open(log_file_path, 'wb') as log_file:
        # Start the subprocess with pipes enabled for stdout and stderr
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            cwd=cwd
        )

        # Create threads to read from stdout and stderr
        stdout_thread = threading.Thread(target=stream_output, args=(process.stdout, log_file, sys.stdout))
        stderr_thread = threading.Thread(target=stream_output, args=(process.stderr, log_file, sys.stderr))

        # Start threads
        stdout_thread.start()
        stderr_thread.start()

        # Wait for threads to finish
        stdout_thread.join()
        stderr_thread.join()

        # Wait for the subprocess to finish
        process.wait()



        
def main():
    print("Loopy: Started.")
    cyclic_iterator = itertools.cycle(["/app/env1","/app/env2"])
    while True:
        print("Loopy: In the start of while.")
        sleep(1)
        env_dir = next(cyclic_iterator)
        

        

        print("Loopy: calling pip installer.")
        cmd = [f"{env_dir}/venv/bin/pip3", "install","-r", f"{env_dir}/software/requirements.txt"]
        subprocess.run(cmd,check=True)

        sleep(1)

        print("Loopy: calling twin runner.")
        cmd = [f"{env_dir}/venv/bin/python3", "-u", f"{env_dir}/software/main.py"]
        cwd = f"{env_dir}/software"
        run_command_and_log_output(cmd, cwd, f"{env_dir}/software/output_of_last_run_of_main_py.txt")



                


main()
