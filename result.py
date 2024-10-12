class result:


   
    filename=""
    flag=""
    level=""
    Exploration = False

 
    readattempts=0
    writeattempts=0
    reg_readattempts = 0
    reg_writeattempts = 0

    read_time = 0
    write_time = 0
    reg_read_time = 0
    reg_write_time = 0

 

    executed_insts=0
    executed_stmts=0
    descriptions = 0
 

    # stateforking
    possiblestates=0
    total_time = 0

    initializing_time=0
    state_forking_time=0

   
    # solving
    solving_time = 0
    constraint_number=0
    variable_number=0
    constraint_depth=0
    constraints= []
    solving_attempts=0
    transferring_time_cost=0
    transferring_number=0


    def __init__(self, filename,flag,level):
        self.filename=filename
        self.flag=flag
        self.level=level


    def get_result(self):
        return "filename={},flag={},level={},exploration={}," \
               "readattempts={}, writeattempts={},reg_readattempts={}, reg_writeattempts={}," \
               "read_time={}, write_time={},reg_read_time={}, reg_write_time={}," \
               "executed_insts={},executed_stmts={}," \
               "possiblestates={},total_time={}," \
               "initializing_time={}," \
               "state_forking_time={},solving_attempts={},transferring_time_cost={},transferring_number={}," \
               "solving_time={},constraint_number={},variable_number={},constraint_depth={},constraints={}".format(

                self.filename,self.flag,self.level,self.Exploration,
                self.readattempts,self.writeattempts,
                self.reg_readattempts, self.reg_writeattempts,
                self.read_time, self.write_time,
                self.reg_read_time, self.reg_write_time,
                self.executed_insts,self.executed_stmts,
                self.possiblestates, self.total_time,
                self.initializing_time,
                self.state_forking_time,self.solving_attempts,self.transferring_time_cost,self.transferring_number,
                self.solving_time,self.constraint_number,self.variable_number,self.constraint_depth, self.constraints)


