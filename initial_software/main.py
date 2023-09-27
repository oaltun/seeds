#!/usr/bin/env python3
import collections
import json
from snippets.loggers_get import loggers_get
from tools.file_read import file_read
import pydantic
import openai
import os
from pathlib import Path
from time import sleep
from tools.file_write import file_write
from schemas.Completion import Completion
from schemas.DirFilelistGet import DirFilelistGet
from tools.dir_filelist_get import dir_filelist_get
import datetime
from datetime import datetime
import instructor
import time
from subprocess import run





instructor.patch() # Enables the response_model 
openai.api_key = os.getenv("OPENAI_API_KEY")

def main():

    run(["/app/env1/venv/bin/python3","--version"])

    detailed_log, summary_log=loggers_get()

    readme_for_ai = file_read(Path('./readme_for_ai.md'))
    specific_goal = file_read(Path('./specific_goal.md'))
    name = file_read(Path('./name.md'))

    your_id = "1"
    twin_id = "2"
    if "2" in name:
        your_id="2"
        twin_id = "1"



    your_file_list = dir_filelist_get(DirFilelistGet(directory=f"/app/env{your_id}/software"))
    twin_file_list = dir_filelist_get(DirFilelistGet(directory=f"/app/env{twin_id}/software"))

    



    content = f"""
{readme_for_ai}

# Specific Goal

{specific_goal}

# Your name

Your name is {name}

# Your current directory structure

{your_file_list}

# Your twins current directory structure

{twin_file_list}

"""

    message_deque = collections.deque(maxlen=4)
    system_message = dict(role="system", content=content)
    message_deque.append(system_message)
    detailed_log.info(json.dumps(system_message))
    summary_log.info(json.dumps(system_message))

    iteration=0
    start_time = time.time()
    while time.time() - start_time  < 1800: # After 30 minutes (30 *60 =1800)we exit
        iteration=iteration+1
        sleep(1)
        print("Iteration",iteration,'.',end=' ')
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k", # Alternatives gpt-4-32k gpt-3.5-turbo-16k
                functions=[Completion.openai_schema],
                function_call = dict(name= Completion.openai_schema["name"]),
                messages=list(message_deque)
            )

            completion = Completion.from_response(response)

            assistant_message=dict(role="assistant", content=json.dumps(response))
            message_deque.append(assistant_message)
            detailed_log.info(json.dumps(assistant_message))
            summary_log.info(json.dumps(completion.model_dump_json()))
            print(f"Software {your_id} AI request: ",assistant_message)

            if completion.dir_filelist_get is not None:
                filelist = dir_filelist_get(completion.dir_filelist_get)
                filelist_message=dict(role="user", content=" ".join(str(path) for path in filelist))
                message_deque.append(filelist_message)
                detailed_log.info(json.dumps(filelist_message))

            if completion.file_to_read is not None:
                content = Path(completion.file_to_read).read_text()
                fileread_message=dict(role="user",content=content)
                message_deque.append(fileread_message)
                detailed_log.info(json.dumps(fileread_message))

            if completion.file_to_write is not None:
                file_write(completion.file_to_write)
                filewrite_message=dict(role="user",content="File written:"+completion.file_to_write.path)
                message_deque.append(filewrite_message)
                detailed_log.info(json.dumps(filewrite_message))

            message_deque.append(system_message)
            detailed_log.info(json.dumps(system_message))
            
        except FileNotFoundError:
            detailed_log.warning(f"Software {your_id}, FileNotFoundError occurred.")
            summary_log.warning(f"Software {your_id}, FileNotFoundError occurred.")
            error_message=dict(role="user", content=f"Software {your_id}, FileNotFoundError occurred.")
            message_deque.append(error_message)

            print(f"Software {your_id}, FileNotFoundError occurred.")
        except Exception as e:
            detailed_log.error(f"Software {your_id}, an exception occurred.", exc_info=True)
            summary_log.error(f"Software {your_id}, an exception occurred.", exc_info=True)
            print(f"Software {your_id}, an exception occurred: {e}")
            raise
        else:
            # This will run if no exception is raised in the try block
            pass
        finally:
            # This will always run, whether an exception is raised or not
            pass



if __name__ == '__main__':
    main()
