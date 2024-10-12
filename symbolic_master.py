from datetime import datetime
import queue
import re
import os

import subprocess
import time
import sys
sys.path.append('./python3.8/site-packages')
from multiprocessing.managers import BaseManager
import compiler
import os.path
from os import path
from anytree import Node, RenderTree

index = 0

root="./Bins/"
bin_path =  "./Bins/"


def scanned(file):
    if not path.os.path.exists(os.path.join(root, "overallres.res")):
        return False
    f = open(os.path.join(root, "overallres.res"), "r")
    for line in f:
        if file in line:
            return True
    return False

if __name__ == '__main__':
    task_queue = queue.Queue()
    result_queue = queue.Queue()

    class QueueManager(BaseManager):
        pass

    QueueManager.register('get_task_queue', callable=lambda: task_queue)
    QueueManager.register('get_result_queue', callable=lambda: result_queue)
    manager = QueueManager(address=('', 5000), authkey=b'abc')
    manager.start()
    task = manager.get_task_queue()
    result = manager.get_result_queue()
    filelist=[]

    print("Symbolic Tester Master")
    for f in os.listdir(root):

        if scanned(f):
            print("finished:"+f)
            continue
        else:
            if not f.endswith("res"):
                filelist.append(root+""+f)

    total = len(filelist)
    count = 0
    print(total)
    for cfile in filelist:
        task.put(cfile)
    while (count < total):
        data = result.get(timeout=200000)
        count += 1;
        print("{}/{}: {}".format(count, total, data))
        f = open(os.path.join(root, "overallres.res"), "a")
        f.write(data + "\n")
        f.close()

    manager.shutdown()











