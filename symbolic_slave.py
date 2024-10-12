import sys
import queue
import re
import signal

import subprocess
import time
import gc
import daemon

import ntpath
from multiprocessing.managers import BaseManager

import analyzer_maat
import compiler
import os.path
from os import path
from anytree import Node, RenderTree

import symbolic_master
 
            
def scanned(file):
    if not path.os.path.exists(os.path.join(root, "maatrunning.log")):
        return False
    f = open(os.path.join(root, "maatrunning.log"), "r")
    for line in f:
        if file in line:
            print("Scanned:"+file)
            return True
    return False

def handler(signum, stack):

    raise Exception
index = 0
resultlist = []
root="./Bins/"

#levels = ["-O3","-Os","-Og","-O2","-O1","-O0"]
# ,"-O2","-O3","-Os","-Og"
 

def is_timeout(file):
    if not path.os.path.exists(os.path.join(root, "timeout.log")):
        return False
    f = open(os.path.join(root, "timeout.log"), "r")
    for line in f:
        if file in line:
            print("timeout:"+file)
            return True
    return False



def main_body():

    print("Flag Slave")


    class QueueManager(BaseManager):
        pass

    QueueManager.register("get_task_queue")
    QueueManager.register("get_result_queue")
    server_addr = '127.0.0.1'
    print('Connect to server %s...' % server_addr)

    m = QueueManager(address=(server_addr, 5000), authkey=b'abc')
    m.connect()
    task = m.get_task_queue()
    result = m.get_result_queue()
    while True:
        try:

            cfile=task.get(timeout=60*60*2)
            print(cfile)

            for r, d, f in os.walk(cfile):
                for file in f:
                    if not file.endswith(".bin"):
                        continue
                    if "-fno-" in file:
                        continue
                    if scanned(file):
                        continue
 
                    try:
                    
                        print(os.path.join(r, file))
                        signal.signal(signal.SIGALRM, handler)
                        signal.alarm(60*10)
                        gc.collect()
                        analyzer_maat.explore_one_pair(os.path.join(r, file), analyzer_maat.EXPLORATION)
                        analyzer_maat.explore_one_pair(os.path.join(r, file), analyzer_maat.TRACEING)
                    except Exception as e:
                    	print(e)
                    	continue




            result.put("name="+cfile)
        except BrokenPipeError:
                print("finished")
                break
        except Exception as e:
                print(e)
                continue
 
 
if __name__ == "__main__":
	with daemon.DaemonContext():
		main_body()
   

