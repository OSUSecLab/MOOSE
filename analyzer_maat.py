from maat import *
import datetime
import time
import ntpath
from pathlib import Path
import os
import symbolic_master
from result import result
reg_r_number=0
reg_r_time_before=0
reg_r_time_after=0
reg_r_time=0

reg_w_number=0
reg_w_time_before=0
reg_w_time_after=0
reg_w_time=0

mem_r_number=0
mem_r_time_before=0
mem_r_time_after=0
mem_r_time=0

mem_w_number=0
mem_w_time_before=0
mem_w_time_after=0
mem_w_time=0


path_number=0
instruction_number=0
constraint_number=0
solving_time=0
vars_number=0
save_next = True

endexplore=False
snapshot_next = True
EXPLORATION=True
TRACEING=False

def write_results_to_database(result):
    conn = sqlite3.connect('res.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS maat_result (filename text, flag text, level text, exploration boolean, readattempts integer, writeattempts integer, reg_readattempts integer, reg_writeattempts integer, read_time real, write_time real, reg_read_time real, reg_write_time real, executed_insts integer, executed_stmts integer, possiblestates integer, total_time real, initializing_time real, state_forking_time real, solving_time real, constraint_number integer, variable_number integer, constraint_depth integer, constraints text, solving_attempts integer, transferring_time_cost real, transferring_number integer)''')
    c.execute("INSERT INTO result VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (result.filename, result.flag, result.level, result.Exploration, result.readattempts, result.writeattempts, result.reg_readattempts, result.reg_writeattempts, result.read_time, result.write_time, result.reg_read_time, result.reg_write_time, result.executed_insts, result.executed_stmts, result.possiblestates, result.total_time, result.initializing_time, result.state_forking_time, result.solving_time, result.constraint_number, result.variable_number, result.constraint_depth, str(result.constraints), result.solving_attempts, result.transferring_time_cost, result.transferring_number))
     
    conn.commit()
    conn.close()
    
 
def reg_r_before(m: MaatEngine):
    global reg_r_number
    global reg_r_time_before
    reg_r_number=reg_r_number+1
    reg_r_time_before=time.time()


def reg_r_after(m: MaatEngine):
    global reg_r_time_after
    global reg_r_time
    reg_r_time_after=time.time()
    reg_r_time=reg_r_time+(reg_r_time_after-reg_r_time_before)


def reg_w_before(m: MaatEngine):
    global reg_w_number
    global reg_w_time_before
    reg_w_number=reg_w_number+1
    reg_w_time_before=time.time()


def reg_w_after(m: MaatEngine):
    global reg_w_time_after
    global reg_w_time
    reg_w_time_after=time.time()
    reg_w_time=reg_w_time+(reg_w_time_after-reg_w_time_before)


def mem_r_before(m: MaatEngine):
    global mem_r_number
    global mem_r_time_before
    mem_r_number=mem_r_number+1
    mem_r_time_before=time.time()


def mem_r_after(m: MaatEngine):
    global mem_r_time_after
    global mem_r_time
    mem_r_time_after=time.time()
    mem_r_time=mem_r_time+(mem_r_time_after-mem_r_time_before)


def mem_w_before(m: MaatEngine):
    global mem_w_number
    global mem_w_time_before
    mem_w_number=mem_w_number+1
    mem_w_time_before=time.time()


def mem_w_after(m: MaatEngine):
    global mem_w_time_after
    global mem_w_time
    mem_w_time_after=time.time()
    mem_w_time=mem_w_time+(mem_w_time_after-mem_w_time_before)

def calcins(m: MaatEngine):
    global instruction_number
    instruction_number=instruction_number+1



def solve2(m: MaatEngine):
    global path_number
    global constraint_number
    path_number=path_number+1

def symexplore(m: MaatEngine):
    global snapshot_next
    if snapshot_next:
        m.take_snapshot()
    # We can skip only one branch when we just inverted it, but then
    # we want to take snapshots for the next ones
 
    snapshot_next = True    
    

def explore(m: MaatEngine, exploration):

    global save_next
    global path_number
    global constraint_number
    global vars_number
    global solving_time
    
    global snapshot_next
    global endexplore

    # We keep trying new paths as long as execution is stopped by reaching
 
    while m.run() != STOP.HOOK and (not endexplore):
 
        # Otherwise, restore previous snapshots until we find a branch condition
        # that can successfuly be inverted to explore a new path 
        while True:
            # Use the solver to invert the branch condition, and find an
            # input that takes the other path
            if (not exploration):
            	endexplore=True
            	 
            path_number=path_number+1
            try:
 
            	m.restore_snapshot(remove=True)
            except:
            
            	endexplore=True
            	break
            s = Solver()
            # We start by adding all constraints that led to the current path.
            # Those constraints need to be preserved to ensure that the new input
            # we compute will still reach the current branch.
            # Since the snapshots are taken *before* branches are resolved,
            # m.path.constraints() doesn't contain the current branch as a constraint.
            for c in m.path.constraints():
                s.add(c)
                vars_number=vars_number+len(c.contained_vars())
                constraint_number=constraint_number+1
            if m.info.branch.taken:
                # If branch was previously taken, we negate the branch condition
                # so that this time it is not taken 
                s.add(m.info.branch.cond.invert())
            else:
                # If the branch was not previously taken, we solve the branch condition
                # so that this time it is taken
                s.add(m.info.branch.cond)
            # If the solver found a model that inverts the current branch, apply this model
            # to the current symbolic variables context and continue exploring the next path! 
            start =time.time()
            if s.check():
                m.vars.update_from(s.get_model())
                # When successfully inverting a branch, we set snapshot_next to False. We do
                # this to avoid taking yet another snapshot of the current branch when 
                # resuming execution. We just inverted the branch, which means that one of
                # both possibilities (taken and not taken) has been explored already, and
                # that the other will get explored now. So there is no need to take a 
                # snapshot to go back to that particular branch.
                snapshot_next = False
                break
            

            end = time.time()
            solving_time= solving_time + (end-start)

 
def init_global():
    global reg_r_number
    reg_r_number=0
    global reg_r_time_before
    reg_r_time_before=0
    global reg_r_time_after
    reg_r_time_after=0
    global reg_r_time
    reg_r_time=0
    
    global reg_w_number
    reg_w_number=0
    
    global reg_w_time_before
    reg_w_time_before=0
    
    global reg_w_time_after
    reg_w_time_after=0
    
    global reg_w_time
    reg_w_time=0
    global mem_r_number
    global mem_r_time_before
    global mem_r_time_after
    global mem_r_time

    global mem_w_number
    global mem_w_time_before
    global mem_w_time_after
    global mem_w_time

    global path_number
    global instruction_number
    global constraint_number
    global solving_time
    global vars_number
    mem_r_number=0
    mem_r_time_before=0
    mem_r_time_after=0
    mem_r_time=0

    mem_w_number=0
    mem_w_time_before=0
    mem_w_time_after=0
    mem_w_time=0


    path_number=0
    instruction_number=0
    constraint_number=0
    solving_time=0
    vars_number=0
    global endexplore
    endexplore=False
    global snapshot_next
    snapshot_next = True
    global save_next
    save_next = True


def explore_single_file(filepath,flag,level,exploration):
    start = datetime.datetime.now()
    m = MaatEngine(ARCH.X64, OS.LINUX)
    init_global()
 
    
 
    m.hooks.add(EVENT.EXEC, WHEN.BEFORE, name="instruction", callbacks=[calcins])
    m.hooks.add(EVENT.REG_R, WHEN.BEFORE, name="reg_r_before", callbacks=[reg_r_before])
    m.hooks.add(EVENT.REG_R, WHEN.AFTER, name="reg_r_after", callbacks=[reg_r_after])
    m.hooks.add(EVENT.REG_W, WHEN.BEFORE, name="reg_w_before", callbacks=[reg_w_before])
    m.hooks.add(EVENT.REG_W, WHEN.AFTER, name="reg_w_after", callbacks=[reg_w_after])
    m.hooks.add(EVENT.MEM_R, WHEN.BEFORE, name="mem_r_before", callbacks=[mem_r_before])
    m.hooks.add(EVENT.MEM_R, WHEN.AFTER, name="mem_r_after", callbacks=[mem_r_after])
    m.hooks.add(EVENT.MEM_W, WHEN.BEFORE, name="mem_w_before", callbacks=[mem_w_before])
    m.hooks.add(EVENT.MEM_W, WHEN.AFTER, name="mem_w_after", callbacks=[mem_w_after])
 
    m.load(filepath, BIN.ELF64,base=0x04000000,    libdirs=["."])
    m.hooks.add(EVENT.PATH, WHEN.BEFORE, name="path", callbacks=[symexplore])
    stdin = m.env.fs.get_fa_by_handle(0)
    buf = m.vars.new_concolic_buffer(
    	"input",
    	b'aaaaaaaa',
    	nb_elems=8,
    	elem_size=1,
    	trailing_value=ord('\n') # concrete new line at the end of the input
    	)
    stdin.write_buffer(buf)
    explore(m, exploration)
    
   
    end=datetime.datetime.now()
    re = result(str(filepath), flag, level)
    re.Exploration = endexplore
    re.readattempts =  mem_r_number
    re.writeattempts = mem_w_number
    re.read_time = mem_r_time
    re.write_time = mem_w_time
    re.reg_read_time = reg_r_time
    re.reg_write_time = reg_w_time
    re.reg_readattempts = reg_r_number
    re.reg_writeattempts = reg_w_number
    re.executed_insts = instruction_number
    re.variable_number = vars_number
    re.possiblestates = path_number
    re.solving_time = solving_time
    re.total_time = str(end-start)
    re.constraint_number = constraint_number
    return re
    
    
     

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
    f = open(os.path.join(symbolic_master.root, "maat-"+flag+".res"), "a")
    
    f.write(enabled_res.get_result() + "\n")
    f.write(disabled_res.get_result() + "\n")
    f.close()
    
 
   
    if not exploration:
        f = open(os.path.join(symbolic_master.root, "maatrunning.log"), "a")
        f.write(enabled_path + "\n")
        f.write(disabled_path + "\n")
        f.close()
