#!/usr/bin/env python3
import json
from snippets.loggers_get import loggers_get
from tools.file_read import file_read
import pydantic
import openai
import os
from pathlib import Path
from time import sleep
from tools.file_write import file_write
from schemas.AIRequests import AIRequests
from schemas.DirFilelistGet import DirFilelistGet
from tools.dir_filelist_get import dir_filelist_get
import datetime
from datetime import datetime
import instructor
instructor.patch() # Enables the response_model 
openai.api_key = os.getenv("OPENAI_API_KEY")

def main():

    detailed_log, summary_log=loggers_get()

    goal = file_read(Path('./goal.yaml'))
    system_message = dict(role="system", content=goal)
    messages=[
        system_message,
    ]
    detailed_log.info(json.dumps(system_message))
    summary_log.info(json.dumps(system_message))


    iteration=0
    while True:
        iteration=iteration+1
        sleep(1)
        print("Iteration",iteration,'.',end=' ')
        try:
            airequests: AIRequests = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                response_model=AIRequests,
                messages=messages
            )

            assistant_message=dict(role="assistant", content=airequests.json())
            messages.append(assistant_message)
            detailed_log.info(json.dumps(assistant_message))
            summary_log.info(json.dumps(assistant_message))
            print("assitant_message",assistant_message)

            if airequests.dir_filelist_get is not None:
                filelist = dir_filelist_get(airequests.dir_filelist_get)
                filelist_message=dict(role="user", content=" ".join(filelist))
                messages.append(filelist_message)
                detailed_log.info(json.dumps(filelist_message))

            if airequests.file_to_read is not None:
                content = Path(airequests.file_to_read).read_text()
                fileread_message=dict(role="user",content=content)
                messages.append(fileread_message)
                detailed_log.info(json.dumps(fileread_message))

            if airequests.file_to_write is not None:
                file_write(airequests.file_to_write)
                filewrite_message=dict(role="user",content="File written:"+airequests.file_to_write.path)
                messages.append(filewrite_message)
                detailed_log.info(json.dumps(filewrite_message))

            messages = messages.append(system_message)
            detailed_log.info(json.dumps(filewrite_message))
            
        except Exception as e:
            detailed_log.error("An exception occurred", exc_info=True)
            summary_log.error("An exception occurred", exc_info=True)
            print(f"An exception occured: {e}")
        else:
            # This will run if no exception is raised in the try block
            pass
        finally:
            # This will always run, whether an exception is raised or not
            pass



if __name__ == '__main__':
    main()
