#!/usr/bin/env python3
import os
from time import sleep
import datetime

now = datetime.datetime.now

def main():
    start = now()
    print("Empty loop started.")
    while True:
        sleep(60)
        print(now()-start," ",)

main()