from datetime import datetime
import queue
import re

import subprocess
import time
import sys
sys.path.append('../python3.8/site-packages')
from multiprocessing.managers import BaseManager
import compiler
import hash_fliter
import os.path
from os import path
from anytree import Node, RenderTree

index = 0

root="./input/"
bin_path = root+"/Bins/"
source_path = root+"sourceFiles/"
fpath = root+"/source"

 

def level_hashtest(turnon_file, turnoff_file):
    if path.exists(turnoff_file) and path.exists(turnon_file):
        turnon_hash = hash_fliter.gethashcode(turnon_file)
        turnoff_hash = hash_fliter.gethashcode(turnoff_file)


        if not turnon_hash == turnoff_hash:
            return True
        else:
            return False
    else:
        return False


def explore_flag_underlevel(filepath, level, treeflags, currenttree, validflags):
    for pre, fill, node in RenderTree(currenttree.root):
        print("%s%s" % (pre, node.name))
    if treeflags == None:
        treeflags = []
    finalnodes = []
    for pre, fill, node in RenderTree(currenttree.root):

            finalnodes.append(node)
 

    for pre, fill, node in RenderTree(currenttree.root):
        if not node.name in treeflags:
            treeflags.append(node.name)

    for flag in validflags:
        if flag in treeflags:
            continue
        else:
            for node in finalnodes:

                flagpaths = str(node.path[len(node.path) - 1]).split("Node('/")[1].split("')")[0].split("/")
                compiler.complie_with_pflags(filepath, compiler.NO_CASE, level, flagpaths, flag)
                turnon_file = os.path.join(r,
                                           "out" + level + flag + "+" + file.replace(".c", ".bin"))
                turnoff_file = os.path.join(r, "out" + level + (
                        flag[:2] + 'no-' + flag[2:]) + "+" + file.replace(".c", ".bin"))
                if (level_hashtest(turnon_file, turnoff_file)):
                    if not node.name == flag:
                        if not flag in treeflags:
                            nexttree = Node(flag, parent=node)
                            os.system("mkdir -p " + bin_path + "/" + flag + "/" + level + "/")
                            os.system("mkdir -p " + source_path + "/" + flag + "/" + level + "/")
                            os.system("cp " + turnon_file + " " + bin_path + "/" + flag + "/" + level + "/")
                            os.system("cp " + turnoff_file + " " + bin_path + "/" + flag + "/" + level + "/")
                            os.system("cp " + os.path.join(r,
                                                           file) + " " + source_path + "/" + flag + "/" + level + "/" + file)
                            treeflags.append(flag)
                            explore_flag_underlevel(filepath, level, treeflags, nexttree, validflags)



if __name__ == '__main__':
    task_queue = queue.Queue()
    result_queue = queue.Queue()


    class QueueManager(BaseManager):
        pass


    QueueManager.register('get_task_queue', callable=lambda: task_queue)
    QueueManager.register('get_result_queue', callable=lambda: result_queue)
    manager = QueueManager(address=('', 1234), authkey=b'abc')
    manager.start()
    task = manager.get_task_queue()
    result = manager.get_result_queue()
    filelist=[]

    print("Flag Master")
    for r, d, f in os.walk(fpath):
        for file in f:

            if file.endswith(".c"):
                index = index + 1
                if path.exists(os.path.join(r, file.replace(".c", ".res"))):
                    continue
                print(os.path.join(r, file))
                filelist.append(os.path.join(r, file))

    total=len(filelist)
    print(total)
    count=0;
    for cfile in filelist:
        task.put(cfile)

    while(count<total):
        data = result.get(timeout=2000)
        count += 1;
        print("{}/{}: {}".format(count, total, data))
        f = open(os.path.join(root, "overallres.res"), "a")
        f.write(data + "\n")
        f.close()

    manager.shutdown()



