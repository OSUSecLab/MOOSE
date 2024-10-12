import datetime
import ntpath
import os.path

import sys
sys.path.append('./python3.8/site-packages/')
import signal
from os import path
import angr
from pathlib import Path
import logging
#import pysqlite3

from angr import sim_manager
from angr.engines.vex.light import light
import z3
from claripy.backends import backend_z3

from tracer import tracer

#logging.getLogger('angr.sim_manager').setLevel(logging.DEBUG)
from angr.exploration_techniques import LengthLimiter
from angr.storage.memory_mixins import testwapper_mixin, fastwapper_mixin
import angr.engines.vex.light.light
import symbolic_master
from result import result

EXPLORATION=True
TRACEING=False

def write_results_to_database(result):
    conn = sqlite3.connect('res.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS result (filename text, flag text, level text, exploration boolean, readattempts integer, writeattempts integer, reg_readattempts integer, reg_writeattempts integer, read_time real, write_time real, reg_read_time real, reg_write_time real, executed_insts integer, executed_stmts integer, possiblestates integer, total_time real, initializing_time real, state_forking_time real, solving_time real, constraint_number integer, variable_number integer, constraint_depth integer, constraints text, solving_attempts integer, transferring_time_cost real, transferring_number integer)''')
    c.execute("INSERT INTO result VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (result.filename, result.flag, result.level, result.Exploration, result.readattempts, result.writeattempts, result.reg_readattempts, result.reg_writeattempts, result.read_time, result.write_time, result.reg_read_time, result.reg_write_time, result.executed_insts, result.executed_stmts, result.possiblestates, result.total_time, result.initializing_time, result.state_forking_time, result.solving_time, result.constraint_number, result.variable_number, result.constraint_depth, str(result.constraints), result.solving_attempts, result.transferring_time_cost, result.transferring_number))
     
    conn.commit()
    conn.close()
    
    
    
def explore_one_bin_pair(filepath,exploration):
    enabled_path=filepath
    r, file = ntpath.split(filepath)


    disabled_path=os.path.join(r,"flaged/"+file)
     
    enabled_res=explore_single_file(enabled_path,"","",exploration)
    disabled_res=explore_single_file(disabled_path,"","",exploration)
    print(enabled_res.get_result())
    print(disabled_res.get_result())
    f = open(os.path.join(symbolic_master.root, file+".res"), "a")
    f.write(enabled_res.get_result() + "\n")
    f.write(disabled_res.get_result() + "\n")
    f.close()
    if not exploration:
        f = open(os.path.join(symbolic_master.root, "running.log"), "a")
        f.write(enabled_path + "\n")
        f.write(disabled_path + "\n")
        f.close()


def explore_one_pair(filepath,exploration):
    enabled_path=filepath
    r, file = ntpath.split(filepath)


    disabled_path=os.path.join(r,file[:8] + 'no-' + file[8:])
    if "-Ofast" in file:
        disabled_path = os.path.join(r, file[:11] + 'no-' + file[11:])
    path=Path(filepath)
    level=path.parent.name
    flag=path.parent.parent.name
    enabled_res=explore_single_file(enabled_path,flag,level,exploration)
    disabled_res=explore_single_file(disabled_path,flag,level,exploration)
    print(enabled_res.get_result())
    print(disabled_res.get_result())
    f = open(os.path.join(symbolic_master.root, flag+".res"), "a")
    if enabled_res.constraint_number > 0:
        f.write(enabled_res.get_result() + "\n")
        f.write(disabled_res.get_result() + "\n")
        f.close()
    
    #write_results_to_database(enabled_res)
    #write_results_to_database(disabled_res)
   
    if not exploration:
        f = open(os.path.join(symbolic_master.root, "running.log"), "a")
        f.write(enabled_path + "\n")
        f.write(disabled_path + "\n")
        f.close()



def explore_single_file(filepath,flag,level,exploration):
    start = datetime.datetime.now()
    angr.state_plugins.solver.Time_cost = 0
    sm = None
    start = datetime.datetime.now()
    angr.state_plugins.solver.Time_cost = 0
    testwapper_mixin.storetime=0
    testwapper_mixin.loadtime=0
    fastwapper_mixin.storetime=0
    fastwapper_mixin.loadtime=0
    testwapper_mixin.write_time_cost = 0
    testwapper_mixin.read_time_cost = 0
    fastwapper_mixin.write_time_cost = 0
    fastwapper_mixin.read_time_cost = 0
    backend_z3.transferring_time_cost=0
    backend_z3.transferring_number=0

     

    sim_manager.constraint_depth=0
    sim_manager.constraint_number =0
    sim_manager.variable_number =0
    sim_manager.constraints = []
    angr.state_plugins.solver.solving_attempts = 0


    solving_attempts = 0
    res = result(str(filepath), flag, level)


    sm = None
    try:

        start1 = datetime.datetime.now()

        proj = angr.Project(filepath, auto_load_libs=False, use_sim_procedures=True,
                            default_analysis_mode='symbolic')
        end1 = datetime.datetime.now()

        init_state = proj.factory.entry_state()
      
        if(exploration):
             
            sm = proj.factory.simgr(init_state)
            #sm.use_technique(angr.exploration_techniques.LoopSeer(cfg=cfg, bound=1000))
            sm.use_technique(angr.exploration_techniques.DFS())

            sm.run()
 
           
 
             
        else:
            t = tracer.Tracer(os.path.join(filepath), b"X33333333")
            result_state, crash_state = t.run()


    except Exception as e:
    
       
        print(e)
        pass

    end = datetime.datetime.now()

    total_time = (end - start).total_seconds()
    init_time = (end1 - start1).total_seconds()
    solving_time = abs(angr.state_plugins.solver.Time_cost)
    state_forking_time = abs(total_time - solving_time - init_time)

    
    res.Exploration = exploration

    res.solving_time = solving_time
    res.initializing_time = init_time
    res.state_forking_time = state_forking_time
    res.total_time = total_time
    res.possiblestates = 0

    res.readattempts= testwapper_mixin.loadtime
    res.writeattempts= testwapper_mixin.storetime
    res.reg_readattempts = fastwapper_mixin.loadtime
    res.reg_writeattempts = fastwapper_mixin.storetime

    res.read_time= testwapper_mixin.read_time_cost
    res.write_time= testwapper_mixin.write_time_cost
    res.reg_read_time = fastwapper_mixin.read_time_cost
    res.reg_write_time = fastwapper_mixin.read_time_cost



    res.constraint_number= sim_manager.constraint_number
    res.variable_number= sim_manager.variable_number
    res.constraint_depth = sim_manager.constraint_depth
    #res.constraints =  sim_manager.constraints
    res.solving_attempts = angr.state_plugins.solver.solving_attempts
    res.transferring_time_cost =backend_z3.transferring_time_cost
    res.transferring_number = backend_z3.transferring_number

    if exploration:
        for stash in sm.stashes:
            if not len(sm.stashes[stash]) == 0:
                for state in sm.stashes[stash]:
                    res.possiblestates = res.possiblestates + 1
                    res.descriptions = res.descriptions + len(state.history.descriptions)
                    
                     
                    for bbl_addr in state.history.bbl_addrs:
                        block = proj.factory.block(bbl_addr)
                        res.executed_insts = res.executed_insts + block.instructions
                        res.executed_stmts = res.executed_stmts + len(block.vex.statements)


    
    return res

 


