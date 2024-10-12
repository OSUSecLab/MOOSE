
import re

import subprocess
import time
import sys
sys.path.append('../python3.8/site-packages')
import ntpath
from angr import sim_manager
from multiprocessing.managers import BaseManager
import compiler
import hash_fliter
import os.path
from os import path
from anytree import Node, RenderTree

index = 0
resultlist = []
root="./input/"
bin_path = root+"/Bins/"
source_path = root+"sourceFiles/"
fpath = root+"execute"
levels = ["-O2","-O1","-O0","-O3","-Os","-Og","-Ofast"]
def hasSym(path):
    sim_manager.constraint_number =0
    proj = angr.Project(path, auto_load_libs=False, use_sim_procedures=True,
                        default_analysis_mode='symbolic')

    init_state = proj.factory.entry_state()
  
    sm = proj.factory.simgr(init_state)
    while len(sm.active) > 0:
        sm.step()
        if sim_manager.constraint_number > 0:
        	return True
        #states = sm.active
        #for state in states:
        #    if len(state.solver.constraints) > 0:
        #        return True
    return False
 
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
                            if(hasSym(turnon_file) or hasSym(turnoff_file)):
                            
                            	os.system("cp " + turnon_file + " " + bin_path + "/" + flag + "/" + level + "/")
                            	os.system("cp " + turnoff_file + " " + bin_path + "/" + flag + "/" + level + "/")
                            	os.system("cp " + os.path.join(r,
                                                           file) + " " + source_path + "/" + flag + "/" + level + "/" + file)
                            treeflags.append(flag)
                            explore_flag_underlevel(filepath, level, treeflags, nexttree, validflags)


if __name__ == '__main__':

    print("Flag Slave")


    class QueueManager(BaseManager):
        pass

    QueueManager.register("get_task_queue")
    QueueManager.register("get_result_queue")
    server_addr = '127.0.0.1'
    print('Connect to server %s...' % server_addr)

    m = QueueManager(address=(server_addr, 1234), authkey=b'abc')
    m.connect()
    task = m.get_task_queue()
    result = m.get_result_queue()
    while True:
        try:
            start = time.time()
            cfile=task.get(timeout=10)
            r, file = ntpath.split(cfile)

            identifiedflags = []
            flags = compiler.loadallvalidflags()

            for level in levels:
                validflags = []
                for flag in flags:

                    compiler.complie(os.path.join(r, file), compiler.YES_CASE, level, flag)
                    turnon_file = os.path.join(r,
                                               "out" + level + flag + "+" + file.replace(".c", ".bin"))
                    turnoff_file = os.path.join(r, "out" + level + (
                            flag[:2] + 'no-' + flag[2:]) + "+" + file.replace(".c", ".bin"))
                    if (level_hashtest(turnon_file, turnoff_file)):
                        if flag not in validflags:
                            validflags.append(flag)

                    compiler.complie(os.path.join(r, file), compiler.NO_CASE, level, flag)
                    turnon_file = os.path.join(r,
                                               "out" + level + flag + "+" + file.replace(".c", ".bin"))
                    turnoff_file = os.path.join(r, "out" + level + (
                            flag[:2] + 'no-' + flag[2:]) + "+" + file.replace(".c", ".bin"))
                    if (level_hashtest(turnon_file, turnoff_file)):
                        if flag not in validflags:
                            validflags.append(flag)

                flagtrees = []
                roots = []
                rootsflag = []

                if len(set(validflags) - (set(identifiedflags) & set(validflags))) == 0:
                    print(validflags)
                    print(identifiedflags)
 
                    continue


                for flag in validflags:
                    compiler.complie(os.path.join(r, file), compiler.NO_CASE, level, flag)
                    turnon_file = os.path.join(r,
                                               "out" + level + flag + "+" + file.replace(".c", ".bin"))
                    turnoff_file = os.path.join(r, "out" + level + (
                            flag[:2] + 'no-' + flag[2:]) + "+" + file.replace(".c", ".bin"))
                    if (level_hashtest(turnon_file, turnoff_file)):
                        root = Node(flag)
                        roots.append(root)
                        rootsflag.append(flag)
                        os.system("mkdir -p " + bin_path + "/" + flag + "/" + level + "/")
                        os.system("mkdir -p " + source_path + "/" + flag + "/" + level + "/")
                        os.system("cp " + turnon_file + " " + bin_path + "/" + flag + "/" + level + "/")
                        os.system("cp " + turnoff_file + " " + bin_path + "/" + flag + "/" + level + "/")
                        os.system(
                            "cp " + os.path.join(r, file) + " " + source_path + "/" + flag + "/" + level + "/" + file)
                    #

                childrenflags = []
                for f in validflags:
                    if not f in rootsflag:
                        childrenflags.append(f)

 
                for root in roots:
                    explore_flag_underlevel(os.path.join(r, file), level, None, root, childrenflags)
                    flagtrees.append(root)

                print(len(flagtrees))
                for tree in flagtrees:
                    for pre, fill, node in RenderTree(tree.root):
                        print("%s%s" % (pre, node.name))
                        f = open(os.path.join(r, file.replace(".c", ".res")), "a")
                        f.write(level + ":" + str(node.path) + "\n")

                        f.close()
                        if not node.name in identifiedflags:
                            identifiedflags.append(node.name)
            end = time.time()
            finaltime = end - start
            outtime = str(finaltime)
            print(type(outtime))
            filepath = os.path.join(r, file)
            cfflags = len(identifiedflags)
            print(f"name=" + filepath + ", time=" + outtime)

            result.put("name=" + filepath + ", time=" + outtime + ", flags=" + str(cfflags))


        except BrokenPipeError:
                print("finished")
                break
        except Exception as e:
                print(e)
                continue





